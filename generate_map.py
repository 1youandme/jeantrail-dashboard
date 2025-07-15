import os

def scan_directory(path, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for root, dirs, files in os.walk(path):
            f.write(f"\n📁 {root}\n")
            for file in files:
                filepath = os.path.join(root, file)
                f.write(f"\n📄 {file}\n")
                try:
                    if file.endswith(('.txt', '.csv', '.json', '.py', '.md', '.html', '.xml')):  # أنواع الملفات النصية
                        with open(filepath, 'r', encoding='utf-8') as content_file:
                            f.write(content_file.read()[:1000] + "...\n")  # أول 1000 حرف فقط
                except Exception as e:
                    f.write(f"[خطأ في القراءة: {str(e)}]\n")

# استبدل المسار بمسار مجلدك الحقيقي:
scan_directory("C:/Users/dell/JeanTrail_AI", "project_map.txt")