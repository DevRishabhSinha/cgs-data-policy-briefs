const { Worker } = require('worker_threads');
const os = require('os');
const path = require('path');
const fs = require('fs').promises;
const { Queue } = require('./queue.js');

async function main() {
    const START_ID = 486400;
    const END_ID = 486500;
    const CONCURRENT_WORKERS = Math.max(os.cpus().length - 1, 1); // Leave one CPU free
    const OUTPUT_FILE = 'scraped_plugshare_data.json';
    
    // Get the absolute path to the worker script
    const workerPath = path.join(__dirname, 'scraper-worker.js');
    
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
        const worker = new Worker(workerPath);  // Use the resolved path

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