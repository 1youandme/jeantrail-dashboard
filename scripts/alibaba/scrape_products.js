// ✅ Alibaba Scraper – شامل جميع الصفحات
const puppeteer = require('puppeteer');
const fs = require('fs-extra');
const path = require('path');
const readline = require('readline');

const KEYWORD = process.env.KEYWORD || 'men shoes'; // 🧠 استخدم متغير خارجي لتحديد الكلمة المفتاحية
const RESULTS_FILE = path.resolve(__dirname, `../results/${KEYWORD.replace(/\s+/g, '_')}.json`);

(async () => {
  const browser = await puppeteer.launch({
    headless: false,
    executablePath: 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 800 });

  const searchUrl = `https://www.alibaba.com/trade/search?SearchText=${encodeURIComponent(KEYWORD)}`;
  await page.goto(searchUrl, { timeout: 0 });

  console.log('🧠 المتصفح مفتوح، حل الكابتشا يدويًا وانتظر ظهور المنتجات...');
  await waitForUserInput('⏳ اضغط Enter فقط بعد ظهور المنتجات على الصفحة...');

  const scrapedProducts = new Map();
  let currentPage = 1;

  while (true) {
    console.log(`📄 Scraping page ${currentPage}...`);
    await delay(3000);

    const productLinks = await page.$$eval(
      'a[href*="/product-detail/"]',
      (links) =>
        links.map((link) => link.href).filter((href, idx, arr) => arr.indexOf(href) === idx)
    );

    console.log(`🔗 Found ${productLinks.length} product links.`);

    for (const url of productLinks) {
      if (scrapedProducts.has(url)) continue;
      await delay(1500);
      try {
        const productPage = await browser.newPage();
        console.log(`🧭 فتح صفحة المنتج: ${url}`);
        await productPage.goto(url, { timeout: 0 });
        await delay(3000);

        const data = await productPage.evaluate(() => {
          const getText = (selector) => document.querySelector(selector)?.innerText?.trim() || '';
          const getImages = () => {
            return Array.from(document.querySelectorAll('img'))
              .map((img) => ({
                src: img.src,
                width: img.naturalWidth,
                height: img.naturalHeight,
              }))
              .filter((img) =>
                img.src.startsWith('https') &&
                (img.src.includes('.jpg') || img.src.includes('.png')) &&
                img.width > 100 &&
                img.height > 100
              )
              .map((img) => img.src);
          };

          const extractOptions = (keyword) => {
            const matches = Array.from(document.querySelectorAll('label, span, div')).filter(el =>
              el.innerText.toLowerCase().includes(keyword)
            );
            const values = new Set();
            matches.forEach(match => {
              const parent = match.closest('div');
              if (parent) {
                const options = parent.querySelectorAll('button, span, div');
                options.forEach(opt => {
                  const txt = opt.innerText?.trim();
                  if (txt && txt.length < 30) values.add(txt);
                });
              }
            });
            return [...values];
          };

          return {
            name: getText('h1'),
            price: getText('.price .value') || getText('.Price--priceText--2nLbV'),
            minOrder: getText('.MinOrder--value--1DLzJ'),
            shipping: getText('.shipping-price') || '',
            seller: getText('.store-name') || '',
            description: document.querySelector('.do-entry-sections')?.innerText?.slice(0, 500) || '',
            images: getImages(),
            colors: extractOptions('color'),
            sizes: extractOptions('size'),
            url: window.location.href,
          };
        });

        if (data.name && data.images.length) {
          scrapedProducts.set(url, data);
          console.log(`✅ تم استخراج بيانات من ${data.name}`);
        } else {
          console.warn(`⚠️ لم يتم العثور على بيانات كافية في: ${url}`);
        }

        await productPage.close();
      } catch (err) {
        console.error(`❌ فشل في استخراج المنتج: ${url}\n${err.message}`);
      }
    }

    const nextBtn = await page.$('button.next-pagination-item.next[title="Next Page"]');
    if (!nextBtn) break;

    await Promise.all([
      page.waitForNavigation({ timeout: 20000 }).catch(() => null),
      nextBtn.click(),
    ]);

    currentPage++;
  }

  const allProducts = Array.from(scrapedProducts.values());
  await fs.ensureFile(RESULTS_FILE);
  await fs.writeJson(RESULTS_FILE, allProducts, { spaces: 2 });

  console.log(`\n✅ تم استخراج ${allProducts.length} منتج`);
  console.log(`📁 تم حفظ البيانات في: ${RESULTS_FILE}`);
  await browser.close();
})();

function delay(ms) {
  return new Promise((res) => setTimeout(res, ms));
}

function waitForUserInput(promptText) {
  return new Promise((resolve) => {
    const rl = require('readline').createInterface({
      input: process.stdin,
      output: process.stdout,
    });
    rl.question(promptText + '\n', () => {
      rl.close();
      resolve();
    });
  });
}
