"""
Course: CSE 251 
Lesson Week: 02
File: assignment.py 
Author: Brother Comeau

Purpose: Retrieve Star Wars details from a server

Instructions:

- Each API call must only retrieve one piece of information
- You are not allowed to use any other modules/packages except for the ones used
  in this assignment.
- Run the server.py program from a terminal/console program.  Simply type
  "python server.py"
- The only "fixed" or hard coded URL that you can use is TOP_API_URL.  Use this
  URL to retrieve other URLs that you can use to retrieve information from the
  server.
- You need to match the output outlined in the decription of the assignment.
  Note that the names are sorted.
- You are requied to use a threaded class (inherited from threading.Thread) for
  this assignment.  This object will make the API calls to the server. You can
  define your class within this Python file (ie., no need to have a seperate
  file for the class)
- Do not add any global variables except for the ones included in this program.

The call to TOP_API_URL will return the following Dictionary(JSON).  Do NOT have
this dictionary hard coded - use the API call to get this.  Then you can use
this dictionary to make other API calls for data.

{
   "people": "http://127.0.0.1:8790/people/", 
   "planets": "http://127.0.0.1:8790/planets/", 
   "films": "http://127.0.0.1:8790/films/",
   "species": "http://127.0.0.1:8790/species/", 
   "vehicles": "http://127.0.0.1:8790/vehicles/", 
   "starships": "http://127.0.0.1:8790/starships/"
}
"""

from cse251 import *

import requests
import json
import threading
import time  # Import time for sleep
import multiprocessing as mp

# Const Values
TOP_API_URL = r'http://127.0.0.1:8790'

# Global Variables
call_count = 0


class Request_thread(threading.Thread):
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.response = {}

    def run(self):
        global call_count
        call_count += 1
        response = requests.get(self.url)
        if response.status_code == 200:
            self.response = response.json()
        else:
            print('RESPONSE = ', response.status_code)
# init work symatanouesly 
#this class holds all the starwar related things and displays them
class StarWarsObject:
    def __init__(self, film_id):
        self.film_id = film_id
        self.data = {}
        self.retrieve_data()
        

    def retrieve_data(self):
        # Retrieve film details
        film_url = f'{TOP_API_URL}/films/{self.film_id}'
        self.data['film'] = self.get_response(film_url)

        # Create and start threads 
        threads = []
        characters_urls = self.data['film'].get('characters', [])
        characters_responses = self.retrieve_concurrent(characters_urls)
        self.data['characters'] = characters_responses

        planets_urls = self.data['film'].get('planets', [])
        planets_responses = self.retrieve_concurrent(planets_urls)
        self.data['planets'] = planets_responses

        starships_urls = self.data['film'].get('starships', [])
        starships_responses = self.retrieve_concurrent(starships_urls)
        self.data['starships'] = starships_responses

        vehicles_urls = self.data['film'].get('vehicles', [])
        vehicles_responses = self.retrieve_concurrent(vehicles_urls)
        self.data['vehicles'] = vehicles_responses

        species_urls = self.data['film'].get('species', [])
        species_responses = self.retrieve_concurrent(species_urls)
        self.data['species'] = species_responses

    # def retrieve_concurrent(self, urls):
    #     responses = []

    #     def fetch_data(url):
    #         response = self.get_response(url)
    #         responses.append(response)

    #     # Create and start threads for concurrent data retrieval
    #     threads = [threading.Thread(target=fetch_data, args=(url,)) for url in urls]
    #     for thread in threads:
    #         thread.start()

    #     # Wait for all threads to finish
    #     for thread in threads:
    #         thread.join()

    #     return responses
    
    def retrieve_concurrent(self, urls):
      responses = []

      def fetch_data(url):
           response = requests.get(url)
           return response

      # Create a multiprocessing Pool with the desired number of processes
      pool = mp.Pool(2)  # You can specify the number of processes you want to use

      # Use pool.map to parallelize the data retrieval
      pool.map(fetch_data, [(url, responses) for url in urls])

      # Close and join the pool to wait for all processes to finish
      pool.close()
      pool.join()

      return responses
    
    def get_response(self, url):
      
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print('RESPONSE = ', response.status_code)
            return {}
            
def format(star_wars_object):
    film_data = star_wars_object.data['film']
    character_urls = film_data.get('characters', [])
    planets_urls = film_data.get('planets', [])
    starships_urls = film_data.get('starships', [])
    vehicles_urls = film_data.get('vehicles', [])
    species_urls = film_data.get('species', [])

    # Get the current time
    current_time = time.strftime("%H:%M:%S")
    # Display character names
    print(f"{current_time}| Characters: {len(character_urls)}")
    character_names = [star_wars_object.data['characters'][i]['name'] for i in range(len(character_urls))]
    character_names.sort()  # Sort the names alphabetically
    character_names_str = ', '.join(character_names)
    print(f"{current_time}| {character_names_str}")
    print(f"{current_time}|")

    # Display planet names
    print(f"{current_time}| Planets: {len(planets_urls)}")
    planet_names = [star_wars_object.data['planets'][i]['name'] for i in range(len(planets_urls))]
    planet_names.sort()  # Sort the names alphabetically
    planet_names_str = ', '.join(planet_names)
    print(f"{current_time}| {planet_names_str}")
    print(f"{current_time}|")
    
    # Display starship names
    print(f"{current_time}| Starships: {len(starships_urls)}")
    starship_names = [star_wars_object.data['starships'][i]['name'] for i in range(len(starships_urls))]
    starship_names.sort()  # Sort the names alphabetically
    starship_names_str = ', '.join(starship_names)
    print(f"{current_time}| {starship_names_str}")
    print(f"{current_time}|")
    
    # Display vehicle names
    print(f"{current_time}| Vehicles: {len(vehicles_urls)}")
    vehicle_names = [star_wars_object.data['vehicles'][i]['name'] for i in range(len(vehicles_urls))]
    vehicle_names.sort()  # Sort the names alphabetically
    vehicle_names_str = ', '.join(vehicle_names)
    print(f"{current_time}| {vehicle_names_str}")
    print(f"{current_time}|")
    
    # Display species names
    print(f"{current_time}| Species: {len(species_urls)}")
    species_names = [star_wars_object.data['species'][i]['name'] for i in range(len(species_urls))]
    species_names.sort()  # Sort the names alphabetically
    species_names_str = ', '.join(species_names)
    print(f"{current_time}| {species_names_str}")
    print(f"{current_time}|")
    
    # Print total time and call count
    print(f"{current_time}| Total Time To complete = {time.time() - start_time:.8f}")
    print(f"{current_time}| There were {call_count} calls to the server")

def main():
    global start_time
    start_time = time.time()
    # Retrieve Top API URLs
    top_api_request = Request_thread(TOP_API_URL)
    top_api_request.start()
    top_api_request.join()
    # Retrieve details for film 6
    film_id = 6
    star_wars_object = StarWarsObject(film_id)
    # Format and display results
    film_data = star_wars_object.data['film']
    # formats the main layout
    print("Starting to retrieve data from the server")
    print("-----------------------------------------")
    print(f"Title   : {film_data.get('title', '')}")
    print(f"Director: {film_data.get('director', '')}")
    print(f"Producer: {film_data.get('producer', '')}")
    print(f"Released: {film_data.get('release_date', '')}")
    print("")
    # Call the format_output function to display names instead of URLs
    format(star_wars_object)

    print(f"Total Time To complete = {time.time() - start_time:.8f}")
    print(f"There were {call_count} calls to the server")

if __name__ == "__main__":
    main()

    # log.write(f'character: {len(responses ["character"])})
    # log.write()