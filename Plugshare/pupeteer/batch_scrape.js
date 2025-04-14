const { Cluster } = require('puppeteer-cluster');

async function scrapePlugShare(page, url) {
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

    console.log('Scraped data for', url, ':', JSON.stringify(data, null, 2));
    return data;
  } catch (error) {
    console.error('An error occurred during scraping:', url, error);
  }
}

async function main() {
  const cluster = await Cluster.launch({
    concurrency: Cluster.CONCURRENCY_CONTEXT,
    maxConcurrency: 2, // Adjust this number based on your needs and system capabilities
    monitor: true,
    puppeteerOptions: {
      headless: false, // Set to true for production
    }
  });

  // Define the task
  await cluster.task(async ({ page, data: url }) => {
    return scrapePlugShare(page, url);
  });

  // Error handling
  cluster.on('taskerror', (err, data) => {
    console.log(`Error crawling ${data}: ${err.message}`);
  });

  // Queue URLs
  const urls = [
    'https://www.plugshare.com/location/486341',
    'https://www.plugshare.com/location/486342',
    // Add more URLs as needed
  ];

  for (const url of urls) {
    await cluster.queue(url);
  }

  // Wait for all tasks to complete
  await cluster.idle();
  // Close the cluster
  await cluster.close();
}

// Run the main function
main().catch(console.error);