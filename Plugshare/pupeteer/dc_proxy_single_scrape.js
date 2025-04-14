const puppeteer = require('puppeteer');

async function scrapePlugShare(url) {
  // Launch a new browser instance with proxy configuration
  const browser = await puppeteer.launch({
    args: [
      `--proxy-server=http://brd.superproxy.io:33335`,
    ],
    headless: true
  });

  const page = await browser.newPage();
  
  // Set up proxy authentication
  await page.authenticate({
    username: 'brd-customer-hl_ddb16e2e-zone-datacenter_proxy1',
    password: 'uw7ek0nbxm3v'
  });

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
    await browser.close();
  }
}

// Usage
async function main() {
  const urls = [
    'https://www.plugshare.com/location/486341',
    'https://www.plugshare.com/location/486342',
    // Add more URLs as needed
  ];

  for (const url of urls) {
    await scrapePlugShare(url);
  }
}

main().catch(console.error);