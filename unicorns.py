import requests
import json
import concurrent.futures
import pandas as pd
import threading  #
def get_coordinates(api_key, location):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        'address': location,
        'key': api_key,
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()

        if data['status'] == 'OK' and data['results']:
            location_data = data['results'][0]['geometry']['location']
            return location_data['lat'], location_data['lng']
        else:
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching coordinates for {location}: {e}")
        return None

def get_coordinates_for_upazilla_unions(api_key, input_file, output_file, max_workers=10):
    with open(input_file, 'r') as file:
        unions = file.read().splitlines()

    coordinates = {}
    lock = threading.Lock()  # Use threading.Lock instead of concurrent.futures.Lock

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(get_coordinates, api_key, f"{union}, Bangladesh"): union for union in unions}

        for future in concurrent.futures.as_completed(futures):
            union = futures[future]
            try:
                coords = future.result()
                if coords:
                    with lock:
                        coordinates[union] = coords
            except Exception as e:
                print(f"Error fetching coordinates for {union}: {e}")

    df = pd.DataFrame(list(coordinates.items()), columns=['Union', 'Coordinates'])
    df[['Latitude', 'Longitude']] = pd.DataFrame(df['Coordinates'].tolist(), index=df.index)
    df[['Union', 'Latitude', 'Longitude']].to_excel(output_file, index=False)

if __name__ == "__main__":
    google_maps_api_key = "AIzaSyBh3zMkqNw5ffw3ZDloZgvm5yJOHUvTm9U"
    input_file_path = "input_unions.txt"
    output_file_path = "output_coordinates.xlsx"

    get_coordinates_for_upazilla_unions(google_maps_api_key, input_file_path, output_file_path)
