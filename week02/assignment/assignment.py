from cse251 import *
import requests
import json
from multiprocessing import Pool

# Const Values
TOP_API_URL = r'http://127.0.0.1:8790'
FILM_ID = 6

class Request_thread:
    def __init__(self, url):
        self.url = url

    def get_response(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            return response.json()
        else:
            print('RESPONSE = ', response.status_code)
            return {}

def retrieve_data(url):
    request_thread = Request_thread(url)
    return request_thread.get_response()

def format_data(results):
    # Extract data from results
    film_data, character_data, planet_data, starship_data, vehicle_data, species_data = results

    # Format and display data
    print(f"Title   : {film_data.get('title', '')}")
    print(f"Director: {film_data.get('director', '')}")
    print(f"Producer: {film_data.get('producer', '')}")
    print(f"Released: {film_data.get('release_date', '')}")
    print("")

    def display_info(category, data):
        category_name = category.capitalize()
        print(f"{category_name}s: {len(data)}")
        names = [item['name'] for item in data]
        names.sort()
        print(", ".join(names))
        print("")

    display_info("character", character_data)
    display_info("planet", planet_data)
    display_info("starship", starship_data)
    display_info("vehicle", vehicle_data)
    display_info("species", species_data)

if __name__ == "__main__":
    # Retrieve top-level API URLs
    top_api_request = Request_thread(TOP_API_URL)
    top_api_data = top_api_request.get_response()

    film_url = f'{TOP_API_URL}/films/{FILM_ID}'
    film_data = retrieve_data(film_url)

    # Retrieve URLs for characters, planets, starships, vehicles, and species
    character_urls = film_data.get('characters', [])
    planet_urls = film_data.get('planets', [])
    starship_urls = film_data.get('starships', [])
    vehicle_urls = film_data.get('vehicles', [])
    species_urls = film_data.get('species', [])

    # Create a process pool
    with Pool() as pool:
        # Retrieve data for characters, planets, starships, vehicles, and species using apply_async()
        character_data = pool.map(retrieve_data, character_urls)
        planet_data = pool.map(retrieve_data, planet_urls)
        starship_data = pool.map(retrieve_data, starship_urls)
        vehicle_data = pool.map(retrieve_data, vehicle_urls)
        species_data = pool.map(retrieve_data, species_urls)

        # Format and display the retrieved data
        format_data((film_data, character_data, planet_data, starship_data, vehicle_data, species_data))