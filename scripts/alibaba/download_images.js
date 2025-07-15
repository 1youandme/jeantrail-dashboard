const fs = require("fs-extra");
const path = require("path");
const axios = require("axios");

const INPUT_JSON = path.join(__dirname, "..", "results", "portable_blender.json");
const IMAGES_DIR = path.join(__dirname, "..", "images", "portable_blender");

(async () => {
  await fs.ensureDir(IMAGES_DIR);
  const products = await fs.readJson(INPUT_JSON);

  for (const [i, product] of products.entries()) {
    const imageUrl = product.image_url;
    if (!imageUrl) continue;

    const filename = path.join(IMAGES_DIR, `product_${i + 1}.jpg`);
    const writer = fs.createWriteStream(filename);

    try {
      const response = await axios({
        url: imageUrl,
        method: "GET",
        responseType: "stream",
      });

      response.data.pipe(writer);
      console.log(`✔️ Downloaded image: ${filename}`);
    } catch (error) {
      console.warn(`❌ Failed to download ${imageUrl}`);
    }
  }
})();
