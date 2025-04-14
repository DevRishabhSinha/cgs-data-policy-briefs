const puppeteer = require('puppeteer');

async function scrapePlugShare(url) {
  const browser = await puppeteer.connect({
    browserWSEndpoint: 'wss://brd-customer-hl_b827bb11-zone-scraping_browser1:28w6tqtvsb5e@brd.superproxy.io:9222'
  });
  const page = await browser.newPage();

  try {
    await page.goto(url, { waitUntil: 'networkidle0', timeout: 60000 });

    // Wait for the main content to load
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
  } finally {
    await page.close();
    await browser.disconnect();
  }
}

// Usage
async function main() {
  const START_ID = 483640;
  const END_ID = 483650;

  const scrapePromises = [];

  for (let id = START_ID; id <= END_ID; id++) {
    const url = `https://www.plugshare.com/location/${id}`;
    console.log(`Queuing URL for scraping: ${url}`);
    scrapePromises.push(scrapePlugShare(url));
  }

  try {
    const results = await Promise.all(scrapePromises);
    console.log('All scraping tasks completed');
    // You can process or save the results here if needed
  } catch (error) {
    console.error('An error occurred during parallel scraping:', error);
  }
}

main().catch(console.error);