from rembg import remove
from PIL import Image
import os

input_folder = r'C:\Users\dell\JeanTrail_AI\alibaba_scraper\results\portable_blender\images\filtered'
logo_path = r'C:\Users\dell\JeanTrail_AI\assets\jeantrail_logo.png'  # عدل حسب لوجو مشروعك

output_folder = os.path.join(input_folder, 'final')
os.makedirs(output_folder, exist_ok=True)

for file_name in os.listdir(input_folder):
    if not file_name.lower().endswith(('.jpg', '.png')): continue
    input_path = os.path.join(input_folder, file_name)

    with open(input_path, 'rb') as f:
        output_data = remove(f.read())

    with open('temp.png', 'wb') as f:
        f.write(output_data)

    img = Image.open('temp.png').convert("RGBA")
    logo = Image.open(logo_path).convert("RGBA")
    logo = logo.resize((80, 80))
    img.paste(logo, (10, 10), logo)
    img.save(os.path.join(output_folder, file_name))

os.remove("temp.png")
print("✅ تم إنهاء المعالجة")
