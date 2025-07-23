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