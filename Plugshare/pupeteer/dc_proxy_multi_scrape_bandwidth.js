const puppeteer = require('puppeteer');
const { setTimeout } = require('timers/promises');
const { Worker, isMainThread, parentPort, workerData } = require('worker_threads');
const os = require('os');
const path = require('path');
const fs = require('fs').promises;
const { Queue } = require('./queue.js'); // We'll create this helper class below

// First, let's create a separate file called queue.js for our thread-safe queue
const queueCode = `
class Queue {
    constructor() {
        this.items = [];
        this.processing = false;
    }

    async enqueue(task) {
        this.items.push(task);
        if (!this.processing) {
            await this.process();
        }
    }

    async process() {
        if (this.processing) return;
        this.processing = true;
        
        while (this.items.length > 0) {
            const task = this.items.shift();
            try {
                const currentData = await fs.readFile(task.filePath, 'utf8')
                    .then(data => JSON.parse(data))
                    .catch(() => ({}));
                
                Object.assign(currentData, task.data);
                
                await fs.writeFile(
                    task.filePath,
                    JSON.stringify(currentData, null, 2),
                    'utf8'
                );
            } catch (error) {
                console.error('Error processing file write task:', error);
            }
        }
        
        this.processing = false;
    }
}

module.exports = { Queue };
`;

// Save the queue code
await fs.writeFile('queue.js', queueCode, 'utf8');

// Worker code for scraping
const workerCode = `
const puppeteer = require('puppeteer');
const { setTimeout } = require('timers/promises');
const { parentPort, workerData } = require('worker_threads');

async function setupPage(browser) {
    const page = await browser.newPage();
    
    await page.authenticate({
        username: 'brd-customer-hl_ddb16e2e-zone-datacenter_proxy1',
        password: 'uw7ek0nbxm3v'
    });
    
    await page.setRequestInterception(true);
    page.on('request', (request) => {
        if (['image', 'stylesheet', 'font', 'media'].includes(request.resourceType())) {
            request.abort();
        } else {
            request.continue();
        }
    });

    await page.setUserAgent('Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1');
    await page.setCacheEnabled(false);

    return page;
}

async function scrapePlugShare(url) {
    const browser = await puppeteer.launch({
        args: [
            \`--proxy-server=http://brd.superproxy.io:33335\`,
        ],
        headless: true
    });
    
    const page = await setupPage(browser);

    try {
        await page.goto(url, { waitUntil: 'networkidle0', timeout: 60000 });
        await page.waitForSelector('#location-details', { timeout: 30000 });
        await page.waitForFunction(() => {
            const name = document.querySelector('#display-name h1');
            const plugs = document.querySelector('#ports');
            return name && plugs;
        }, { timeout: 30000 });
        
        await setTimeout(2000);

        const data = await page.evaluate(() => {
            const getText = (selector) => {
                const element = document.querySelector(selector);
                return element ? element.innerText.trim() : null;
            };

            const getMultipleTexts = (selector) => {
                const elements = document.querySelectorAll(selector);
                return Array.from(elements).map(el => el.innerText.trim()).filter(text => text);
            };

            const getReviews = () => {
                const reviews = [];
                const reviewElements = document.querySelectorAll('#checkins .checkin:not(.cta)');
                
                reviewElements.forEach(review => {
                    const date = review.querySelector('.date')?.innerText.trim();
                    const user = review.querySelector('.user span')?.innerText.trim();
                    const vehicle = review.querySelector('.car')?.innerText.trim();
                    const rating = review.querySelector('.success') ? 'Positive' : 
                                review.querySelector('.fail') ? 'Negative' : 'Neutral';
                    const comment = review.querySelector('.comment')?.innerText.trim();
                    
                    if (date || user || vehicle || comment) {
                        reviews.push({ date, user, vehicle, rating, comment });
                    }
                });
                return reviews;
            };

            return {
                locationName: getText('#display-name h1'),
                address: getText('.info-entry a[property="v:address"]'),
                plugTypes: getMultipleTexts('#ports span'),
                networkProvider: getText('#ports .networks span'),
                chargingSpeed: getText('.plug-power'),
                numberOfChargers: getText('.connector .plug-count'),
                poiType: getText('.poi-name'),
                amenities: getMultipleTexts('.info-entry .content span[ng-repeat="amenity in maps.location.amenities"]'),
                hours: getText('.info-entry [ng-if="maps.location.open247"]') || getText('.info-entry [ng-bind-html="maps.location.hours"]'),
                pricing: {
                    paymentRequired: getText('.info-entry .content div[ng-if="maps.location.cost"]'),
                    rate: getText('.info-entry .content .ng-binding:not(.parking-type)')
                },
                parking: getText('.info-entry .parking-type'),
                reviews: getReviews(),
                photos: Array.from(document.querySelectorAll('#photos .photo a')).map(photo => photo.href)
            };
        });

        return { url, data };
    } catch (error) {
        console.error(\`Error scraping \${url}:\`, error);
        return { url, data: null };
    } finally {
        await browser.close();
    }
}

parentPort.on('message', async ({ url }) => {
    try {
        const result = await scrapePlugShare(url);
        parentPort.postMessage(result);
    } catch (error) {
        parentPort.postMessage({ url, data: null, error: error.message });
    }
});
`;

// Save the worker code
await fs.writeFile('scraper-worker.js', workerCode, 'utf8');

// Main script
async function main() {
    const START_ID = 486400;
    const END_ID = 486500;
    const CONCURRENT_WORKERS = Math.max(os.cpus().length - 1, 1); // Leave one CPU free
    const OUTPUT_FILE = 'scraped_plugshare_data.json';
    
    // Initialize queue for safe file writing
    const writeQueue = new Queue();
    
    // Create array of URLs
    const urls = Array.from(
        { length: END_ID - START_ID + 1 },
        (_, i) => `https://www.plugshare.com/location/${START_ID + i}`
    );

    // Initialize results object
    await fs.writeFile(OUTPUT_FILE, '{}', 'utf8');

    // Create worker pool
    const workers = new Set();
    const urlQueue = [...urls];
    let completed = 0;

    console.log(`Starting scraping with ${CONCURRENT_WORKERS} workers...`);

    // Function to create and start a new worker
    const createWorker = async () => {
        if (urlQueue.length === 0) return;

        const url = urlQueue.shift();
        const worker = new Worker('./scraper-worker.js');

        workers.add(worker);

        worker.on('message', async (result) => {
            if (result.data) {
                // Queue the write operation
                await writeQueue.enqueue({
                    filePath: OUTPUT_FILE,
                    data: { [result.url]: result.data }
                });
            }

            completed++;
            workers.delete(worker);

            // Log progress
            console.log(`Completed ${completed} of ${urls.length} (${((completed/urls.length)*100).toFixed(1)}%)`);

            // Create a new worker if there are more URLs to process
            if (urlQueue.length > 0) {
                await createWorker();
            }
        });

        worker.on('error', (error) => {
            console.error(`Worker error for ${url}:`, error);
            workers.delete(worker);
            
            // Retry failed URL
            urlQueue.push(url);
            
            if (urlQueue.length > 0) {
                createWorker();
            }
        });

        worker.postMessage({ url });
    };

    // Start initial batch of workers
    const initialWorkers = Math.min(CONCURRENT_WORKERS, urls.length);
    await Promise.all(Array(initialWorkers).fill().map(createWorker));

    // Wait for all workers to complete
    while (workers.size > 0 || urlQueue.length > 0) {
        await new Promise(resolve => setTimeout(resolve, 1000));
    }

    console.log('All scraping completed!');
}

main().catch(console.error);