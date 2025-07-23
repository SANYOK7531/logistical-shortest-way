from dotenv_read import START_COORD
from api_conncetions import get_distance_matrix

def build_full_matrix_with_start(locations):
    # Всі точки: [START] + решта
    all_points = [("START", float(START_COORD.split(",")[0]), float(START_COORD.split(",")[1]))] + locations
    
    n = len(all_points)

    # Побудова матриці n x n
    matrix = [[0.0] * n for _ in range(n)]

    return get_distance_matrix(all_points, matrix)