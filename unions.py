import requests
import json
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

def get_coordinates(api_key, location):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        'address': location,
        'key': api_key,
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if data['status'] == 'OK' and data['results']:
        location_data = data['results'][0]['geometry']['location']
        return location_data['lat'], location_data['lng']
    else:
        return None

def get_coordinates_for_upazilla_unions(api_key, input_file, output_file, max_workers=1):
    with open(input_file, 'r') as file:
        unions = file.read().splitlines()

    coordinates = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Use concurrent.futures.ThreadPoolExecutor for multithreading
        futures = {executor.submit(get_coordinates, api_key, f"{union}, Bangladesh"): union for union in unions}

        for future in concurrent.futures.as_completed(futures):
            union = futures[future]
            try:
                coords = future.result()
                if coords:
                    coordinates[union] = coords
            except Exception as e:
                print(f"Error fetching coordinates for {union}: {e}")

    with open(output_file, 'w') as file:
        for union, coords in coordinates.items():
            file.write(f"{union}: {coords[0]}, {coords[1]}\n")

if __name__ == "__main__":
    google_maps_api_key = "AIzaSyBh3zMkqNw5ffw3ZDloZgvm5yJOHUvTm9U"
    input_file_path = "input_unions.txt"
    output_file_path = "output_coordinates.txt"

    get_coordinates_for_upazilla_unions(google_maps_api_key, input_file_path, output_file_path)
