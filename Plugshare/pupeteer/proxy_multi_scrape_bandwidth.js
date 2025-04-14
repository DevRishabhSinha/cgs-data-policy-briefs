const puppeteer = require('puppeteer');
const fs = require('fs').promises;

async function setupPage(browser) {
  const page = await browser.newPage();
  
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
  const browser = await puppeteer.connect({
    browserWSEndpoint: 'wss://brd-customer-hl_b827bb11-zone-scraping_browser1:28w6tqtvsb5e@brd.superproxy.io:9222'
  });
  const page = await setupPage(browser);

  try {
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForSelector('#location-details', { timeout: 10000 });

    const data = await page.evaluate(() => {
      const getText = (selector) => {
        const element = document.querySelector(selector);
        return element ? element.innerText.trim() : null;
      };

      const getMultipleTexts = (selector) => {
        return Array.from(document.querySelectorAll(selector)).map(el => el.innerText.trim());
      };

      return {
        url: window.location.href,
        locationName: getText('#display-name h1'),
        address: getText('.info-entry a[property="v:address"]'),
        plugTypes: getMultipleTexts('#ports span'),
        networkProvider: getText('.networks span'),
        chargingSpeed: getText('.plug-power'),
        numberOfChargers: getText('.connector .plug-count'),
        poiType: getText('.poi-name'),
        amenities: getMultipleTexts('.info-entry .content span[ng-repeat="amenity in maps.location.amenities"]'),
        hours: getText('.info-entry [ng-if="maps.location.open247"]') || getText('.info-entry [ng-bind-html="maps.location.hours"]'),
        pricing: {
          paymentRequired: getText('.info-entry .content div[ng-if="maps.location.cost"]'),
          rate: getText('.info-entry .content .ng-binding:not([ng-if])')
        },
        parking: getText('.info-entry .parking-type'),
        reviews: Array.from(document.querySelectorAll('.checkin')).map(review => ({
          date: getText('.date', review),
          user: getText('.user span', review),
          vehicle: getText('.car', review),
          rating: review.querySelector('.success') ? 'Positive' : (review.querySelector('.fail') ? 'Negative' : 'Neutral'),
          comment: getText('.comment', review)
        })),
        photos: Array.from(document.querySelectorAll('#photos .photo a')).map(photo => photo.href)
      };
    });

    console.log('Scraped data:', JSON.stringify(data, null, 2));
    return data;
  } catch (error) {
    console.error('An error occurred during scraping:', error);
    return null;
  } finally {
    await page.close();
    await browser.disconnect();
  }
}

async function saveToJson(data, filename) {
  await fs.writeFile(filename, JSON.stringify(data, null, 2));
  console.log(`Data saved to ${filename}`);
}

async function main() {
  const START_ID = 486400;
  const END_ID = 486500;
  const BATCH_SIZE = 10;
  const allScrapedData = [];

  for (let batchStart = START_ID; batchStart <= END_ID; batchStart += BATCH_SIZE) {
    const batchEnd = Math.min(batchStart + BATCH_SIZE - 1, END_ID);
    const batchPromises = [];

    for (let id = batchStart; id <= batchEnd; id++) {
      const url = `https://www.plugshare.com/location/${id}`;
      console.log(`Queuing URL for scraping: ${url}`);
      batchPromises.push(scrapePlugShare(url));
    }

    try {
      const batchResults = await Promise.all(batchPromises);
      allScrapedData.push(...batchResults.filter(result => result !== null));
      console.log(`Batch completed: ${batchStart} to ${batchEnd}`);
    } catch (error) {
      console.error(`An error occurred during batch scraping (${batchStart} to ${batchEnd}):`, error);
    }
  }

  console.log('All scraping tasks completed');
  await saveToJson(allScrapedData, 'scraped_plugshare_data_486400_486500.json');
}

main().catch(console.error);