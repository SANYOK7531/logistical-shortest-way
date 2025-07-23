def format_full_distance_table(all_points, matrix):
    headers = [name for name, _, _ in all_points]
    lines = []

    # Заголовок
    header_line = f"{'':<12}" + "".join([f"{h:<12}" for h in headers])
    lines.append(header_line)
    lines.append("-" * len(header_line))

    # Рядки
    for i, (from_name, _, _) in enumerate(all_points):
        row = f"{from_name:<12}"
        for j in range(len(all_points)):
            dist_m = matrix[i][j]
            dist_km = f"{dist_m / 1000:.1f} km" if dist_m != float("inf") else "—"
            row += f"{dist_km:<12}"
        lines.append(row)

    return "\n".join(lines)

def generate_maps_url(route, all_points):
    coords = []

    for idx in route:
        lat = all_points[idx][1]
        lon = all_points[idx][2]
        coords.append(f"{lat},{lon}")

    # 🧭 Перевіряємо: чи маршрут вже закінчується на START?
    if route[-1] != 0:
        coords.append(f"{all_points[0][1]},{all_points[0][2]}")

    url = "https://www.google.com/maps/dir/" + "/".join(coords)
    return url
