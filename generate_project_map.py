import os

def generate_project_map(start_path='.', indent=0, ignore_dirs=None, output_lines=None):
    if ignore_dirs is None:
        ignore_dirs = {'.git', '__pycache__', 'node_modules', '.venv', 'env'}

    if output_lines is None:
        output_lines = []

    for item in sorted(os.listdir(start_path)):
        full_path = os.path.join(start_path, item)
        relative_path = os.path.relpath(full_path, start_path)

        if os.path.isdir(full_path):
            if item not in ignore_dirs:
                output_lines.append('  ' * indent + f'📁 {item}/')
                generate_project_map(full_path, indent + 1, ignore_dirs, output_lines)
        else:
            output_lines.append('  ' * indent + f'📄 {item}')
            try:
                if os.path.getsize(full_path) < 30 * 1024:  # فقط الملفات الصغيرة < 30KB
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if content.strip():
                            lines = content.strip().splitlines()
                            preview = "\n".join("    " + line for line in lines[:10])
                            output_lines.append('    ── محتوى مختصر:')
                            output_lines.append(preview)
                            if len(lines) > 10:
                                output_lines.append('    ...')
            except Exception as e:
                output_lines.append(f'    ⚠️ Error reading file: {e}')

    return output_lines


if __name__ == '__main__':
    print("🧭 Generating full project map...")
    lines = ["🧭 Project Map:", "=" * 50]
    lines += generate_project_map(start_path='.')

    with open("project_map.txt", "w", encoding='utf-8') as f:
        f.write("\n".join(lines))

    print("✅ Done. Saved to project_map.txt")
