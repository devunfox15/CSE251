class StarWarsThread(threading.Thread):
    def __init__(self, url, data_type):
        super().__init__()
        self.url = url
        self.data_type = data_type

    def run(self):
        start_time = time.time()
        response = requests.get(self.url)
        end_time = time.time()
        
        if response.status_code == 200:
            try:
                data = response.json()
                self.process_data(data, start_time, end_time)
            except json.JSONDecodeError as e:
                print(f'Error decoding JSON from {self.url}: {e}')
        else:
            print(f'Error in requesting {self.url}')

    def process_data(self, data, start_time, end_time):
        Log.log(f'-----------------------------------------')
        Log.log(f'Title   : {data["title"]}')
        Log.log(f'Director: {data["director"]}')
        Log.log(f'Producer: {data["producer"]}')
        Log.log(f'Released: {data["release_date"]}')
        Log.log()

        if isinstance(data, dict):
            if 'characters' in data:
                Log.log(f'Characters: {len(data["characters"])}')
                characters = sorted([character["name"] for character in data["characters"]])
                Log.log(', '.join(characters))
                Log.log()

            if 'planets' in data:
                Log.log(f'Planets: {len(data["planets"])}')
                planets = sorted([planet["name"] for planet in data["planets"]])
                Log.log(', '.join(planets))
                Log.log()

            if 'starships' in data:
                Log.log(f'Starships: {len(data["starships"])}')
                starships = sorted([starship["name"] for starship in data["starships"]])
                Log.log(', '.join(starships))
                Log.log()

            if 'vehicles' in data:
                Log.log(f'Vehicles: {len(data["vehicles"])}')
                vehicles = sorted([vehicle["name"] for vehicle in data["vehicles"]])
                Log.log(', '.join(vehicles))
                Log.log()

            if 'species' in data:
                Log.log(f'Species: {len(data["species"])}')
                species = sorted([specie["name"] for specie in data["species"]])
                Log.log(', '.join(species))
                Log.log()

        Log.log(f'Total Time To complete = {end_time - start_time:.8f}')
        Log.log(f'There were {len(threads)} calls to the server')

if __name__ == '__main__':
    print(f'{datetime.now().strftime("%H:%M:%S")} | Starting to retrieve data from the server')
    
  # Start logging to a file

    response = requests.get(TOP_API_URL)
    
    if response.status_code == 200:
        top_data = response.json()
        film_url = top_data.get('films') + '6'  # Use get() to handle missing keys gracefully
        response = requests.get(film_url)

        if response.status_code == 200:
            try:
                film_data = response.json()

                # Create threads for retrieving data
                threads = []
                threads.append(StarWarsThread(film_url, 'film'))

                for character_url in film_data.get('characters', []):
                    threads.append(StarWarsThread(character_url, 'character'))

                for planet_url in film_data.get('planets', []):
                    threads.append(StarWarsThread(planet_url, 'planet'))

                for starship_url in film_data.get('starships', []):
                    threads.append(StarWarsThread(starship_url, 'starship'))

                for vehicle_url in film_data.get('vehicles', []):
                    threads.append(StarWarsThread(vehicle_url, 'vehicle'))

                for specie_url in film_data.get('species', []):
                    threads.append(StarWarsThread(specie_url, 'species'))

                # Start and wait for all threads to finish
                for thread in threads:
                    thread.start()

                for thread in threads:
                    thread.join()

                print(f'There were {len(threads)} calls to the server')
            except json.JSONDecodeError as e:
                print(f'Error decoding JSON from {film_url}: {e}')
        else:
            print(f'Error in requesting film data from {film_url}')
    else:
        print(f'Error in requesting top API data from {TOP_API_URL}')