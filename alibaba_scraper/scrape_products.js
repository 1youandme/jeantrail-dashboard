const puppeteer = require('puppeteer');
const fs = require('fs-extra');
const path = require('path');

const KEYWORD = 'portable blender';
const OUTPUT_DIR = path.join(__dirname, 'results', KEYWORD.replace(/\s+/g, '_'));
fs.ensureDirSync(OUTPUT_DIR);

(async () => {
  const browser = await puppeteer.launch({ headless: false });
  const page = await browser.newPage();
  await page.goto(`https://www.alibaba.com/trade/search?SearchText=${KEYWORD}`, { timeout: 0 });

  await page.waitForSelector('.J-search-card-wrapper', { timeout: 10000 });

  const products = await page.evaluate(() => {
    const cards = document.querySelectorAll('.J-search-card-wrapper');
    return [...cards].map(card => {
      const name = card.querySelector('h2')?.innerText?.trim();
      const image_url = card.querySelector('img')?.src;
      const price = card.querySelector('.elements-offer-price-normal__price')?.innerText?.trim();
      const min_order = card.querySelector('.elements-offer-minOrder-normal__value')?.innerText?.trim();
      const supplier = card.querySelector('.seb-supplier__supplier-name')?.innerText?.trim();
      const product_link = card.querySelector('a')?.href;

      return { name, price, min_order, supplier, image_url, product_link };
    });
  });

  fs.writeJsonSync(path.join(OUTPUT_DIR, 'products.json'), products, { spaces: 2 });

  console.log(`✅ Saved ${products.length} products to products.json`);
  await browser.close();
})();
