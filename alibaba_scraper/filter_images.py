import pytesseract
from PIL import Image
import os
import shutil

input_folder = r'C:\Users\dell\JeanTrail_AI\alibaba_scraper\results\portable_blender\images'
output_folder = os.path.join(input_folder, 'filtered')
os.makedirs(output_folder, exist_ok=True)

def has_text(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return len(text.strip()) > 10

all_images = os.listdir(input_folder)
text_count = 0

for file in all_images:
    full_path = os.path.join(input_folder, file)
    if os.path.isdir(full_path): continue
    if has_text(full_path):
        text_count += 1

# اقبل الصور التي بها نص فقط إن كانت كلها بها نصوص
accept_all = text_count == len([f for f in all_images if os.path.isfile(os.path.join(input_folder, f))])

for file in all_images:
    full_path = os.path.join(input_folder, file)
    if os.path.isdir(full_path): continue
    if accept_all or not has_text(full_path):
        shutil.copy(full_path, os.path.join(output_folder, file))
