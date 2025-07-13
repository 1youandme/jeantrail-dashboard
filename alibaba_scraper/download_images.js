const axios = require('axios');
const fs = require('fs-extra');
const path = require('path');

const PRODUCT_DIR = path.join(__dirname, 'results', 'portable_blender');
const OUTPUT_IMG_DIR = path.join(PRODUCT_DIR, 'images');
fs.ensureDirSync(OUTPUT_IMG_DIR);

const products = fs.readJsonSync(path.join(PRODUCT_DIR, 'products.json'));

(async () => {
  for (const product of products) {
    if (!product.image_url) continue;
    const fileName = product.name.replace(/[^\w]/g, '_').slice(0, 30) + '.jpg';
    const imagePath = path.join(OUTPUT_IMG_DIR, fileName);
    try {
      const response = await axios.get(product.image_url, { responseType: 'arraybuffer' });
      fs.writeFileSync(imagePath, response.data);
      console.log(`✅ Downloaded: ${fileName}`);
    } catch (err) {
      console.warn(`❌ Failed to download: ${fileName}`);
    }
  }
})();
