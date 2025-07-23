import os

def cleanup_temp_xml_files():
    temp_dir = "temp"
    for filename in os.listdir(temp_dir):
        if filename.endswith(".xml"):
            os.remove(os.path.join(temp_dir, filename))
            print(f"🧺 Видалено файл: {filename}")
