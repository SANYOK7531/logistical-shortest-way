import os
from collections import defaultdict
from read_xml_file import fetch_xml_from_mail, parse_xml
from full_matrix_creation import build_full_matrix_with_start
from tsp import tsp_nearest_neighbor, extract_route_info
from url_generation import generate_maps_url
from all_distances import format_full_distance_table
from email_sender import send_result_email
from clean_temp import cleanup_temp_xml_files

messages = fetch_xml_from_mail()

# 📦 Групуємо файли по листах
grouped = defaultdict(list)
for filepath, sender, subject in messages:
    grouped[(sender, subject)].append(filepath)

for (sender, subject), xml_files in grouped.items():
    
    body = f"📬 Ви надіслали {len(xml_files)} XML-файл(ів).\n\n"
    body += f"📦 Нижче наведено маршрути для кожного з них:\n\n"
    
    for i, xml_file in enumerate(xml_files, start=1):
        try:
            delivery_points = parse_xml(xml_file)
            all_points, matrix = build_full_matrix_with_start(delivery_points)
            route = tsp_nearest_neighbor(matrix)
            route_info = extract_route_info(route, all_points, matrix)
            maps_url = generate_maps_url(route, all_points)
            full_table = format_full_distance_table(all_points, matrix)

            body += "📊 Відстані між точками:\n\n" + full_table + "\n\n"
            body += f"🧭 Маршрут №{i}: {os.path.basename(xml_file)}\n\n"

            body += f"{'Точка':<40} | {'Відстань':<12} | {'Час в дорозі'}\n"
            body += "-" * 55 + "\n"
            for name, distance, duration in route_info:
                body += f"{name:<40} | {distance:<12} | {duration}\n"

            body += f"\n🗺️ Візуалізувати маршрут: {maps_url}\n"

        except Exception as e:
            body += f"\n⚠️ Не вдалося обробити файл {os.path.basename(xml_file)}: {e}\n"

        body += "\n" + "=" * 60 + "\n\n"

    send_result_email(sender, subject, body)

cleanup_temp_xml_files()