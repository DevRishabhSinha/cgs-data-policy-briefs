const puppeteer = require('puppeteer');

async function scrapePlugShare(url) {
  const browser = await puppeteer.launch({ headless: true }); // Set to true for production
  const page = await browser.newPage();

  try {
    await page.goto(url, { waitUntil: 'networkidle0', timeout: 90000 });

    // Wait for the main content to load
    await page.waitForSelector('#location-details', { timeout: 90000 });

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

    console.log('Scraped data for', url, ':', JSON.stringify(data, null, 2));
    return data;
  } catch (error) {
    console.error('An error occurred during scraping:', url, error);
    return null;
  } finally {
    await browser.close();
  }
}

async function main() {
  const urls = [
    'https://www.plugshare.com/location/486341',
    'https://www.plugshare.com/location/486342',
    'https://www.plugshare.com/location/486343',
    'https://www.plugshare.com/location/486344',
    'https://www.plugshare.com/location/486345',
    'https://www.plugshare.com/location/486346',
    'https://www.plugshare.com/location/486347',
    'https://www.plugshare.com/location/486348',
    'https://www.plugshare.com/location/486349',
    'https://www.plugshare.com/location/486350',
  ];

  console.log('Starting parallel scraping of', urls.length, 'URLs');

  const scrapingPromises = urls.map(url => scrapePlugShare(url));
  const scrapedData = await Promise.all(scrapingPromises);

  console.log('All data scraped:');
  console.log(JSON.stringify(scrapedData.filter(Boolean), null, 2));
}

// Run the main function
main().catch(console.error);