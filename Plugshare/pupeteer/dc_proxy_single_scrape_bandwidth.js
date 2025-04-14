const puppeteer = require('puppeteer');
const { setTimeout } = require('timers/promises');

async function setupPage(browser) {
  const page = await browser.newPage();
  
  // Set up proxy authentication
  await page.authenticate({
    username: 'brd-customer-hl_ddb16e2e-zone-datacenter_proxy1',
    password: 'uw7ek0nbxm3v'
  });
  
  // Intercept and block unnecessary requests
  await page.setRequestInterception(true);
  page.on('request', (request) => {
    if (['image', 'stylesheet', 'font', 'media'].includes(request.resourceType())) {
      request.abort();
    } else {
      request.continue();
    }
  });

  // Set a mobile user agent to potentially receive lighter content
  await page.setUserAgent('Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1');

  // Disable cache
  await page.setCacheEnabled(false);

  return page;
}

async function scrapePlugShare(url) {
  const browser = await puppeteer.launch({
    args: [
      `--proxy-server=http://brd.superproxy.io:33335`,
    ],
    headless: true
  });
  
  const page = await setupPage(browser);

  try {
    await page.goto(url, { waitUntil: 'networkidle0', timeout: 60000 });

    // Wait for key elements to be present
    await page.waitForSelector('#location-details', { timeout: 30000 });
    await page.waitForFunction(() => {
      const name = document.querySelector('#display-name h1');
      const plugs = document.querySelector('#ports');
      return name && plugs;
    }, { timeout: 30000 });
    
    // Short delay to ensure dynamic content is fully loaded
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

      // Get reviews with proper error handling
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

    console.log('Scraped data:', JSON.stringify(data, null, 2));
    return data;
  } catch (error) {
    console.error('An error occurred during scraping:', error);
    return null;
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