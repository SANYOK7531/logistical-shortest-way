import requests
from dotenv_read import API_KEY

def get_distance_matrix(all_points, matrix):

    n = len(all_points)
    
    for i in range(n):
        origin_coord = f"{all_points[i][1]},{all_points[i][2]}"
        destination_coords = [f"{point[1]},{point[2]}" for point in all_points]

        url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        params = {
            "origins": origin_coord,
            "destinations": "|".join(destination_coords),
            "key": API_KEY,
            "units": "metric",
            "mode": "driving",
        }

        response = requests.get(url, params=params)
        data = response.json()

        if data["status"] != "OK":
            print(f"❌ Запит API не спрацював для точки {all_points[i][0]}")
            continue

        elements = data["rows"][0]["elements"]
        for j in range(n):
            element = elements[j]
            if element["status"] == "OK":
                matrix[i][j] = element["distance"]["value"]  # у метрах
            else:
                matrix[i][j] = float("inf")  # недоступна точка

    return all_points, matrix
