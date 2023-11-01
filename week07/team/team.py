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

from datetime import datetime, timedelta
import requests
import json
import threading
import multiprocessing as mp

# Include cse 251 common Python files
from cse251 import *

# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'

# Global Variables
call_count = 0


# TODO Add your threaded class definition here
class ServerRequest(threading.Thread):
    def __init__(self, url:str) -> None:
        threading.Thread.__init__(self)
        self.url = url
        self.response = {}

    def run(self):
        global call_count
        call_count += 1
        response = requests.get(self.url)
        if response.ok:
            self.response = response.json()

# TODO Add any functions you need here
def sync_request(url) -> dict:
    request = ServerRequest(url)
    request.start()
    request.join()
    return request.response

def start_request(url:str) -> ServerRequest:
    request = ServerRequest(url)
    request.start()
    return request

def get_name_from_request(request:ServerRequest) -> str:
    request.join()
    return request.response['name']

def new_request(url, category) -> dict:
    request = ServerRequest(url)
    request.start()
    print(os.getpid())
    request.join()
    return (request.response, category)

def increase_count(response):
    (json_data, category) = response
    global call_count
    call_count += 1

class StarWarsResult():
    def __init__(self):
        self.server_results = {}
        self.call_counts = 0

    def process_json(self, response):
        (json_data, category) = response
        if category not in self.server_results:
            self.server_results[category] = []
        self.server_results[category].append(json_data['name'])
        self.call_counts += 1
        print(f'process_json: {os.getpid()}')

def main():
    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from the server')

    pool = mp.Pool(7)
    sw_results = StarWarsResult()

    # TODO Retrieve Top API urls
    detail_urls = sync_request(TOP_API_URL)

    # TODO Retrieve Details on film 6
    film_details = sync_request(detail_urls['films'] + '6')
    server_requests = {}
    server_results = {}

    for key, detail in film_details.items():
        if isinstance(detail, list):
            [pool.apply_async(new_request, args=(x, key), callback=sw_results.process_json) for x in detail]

    pool.close()
    pool.join()

    for key, detail in film_details.items():
        if isinstance(detail, list):
            # server_results[key] = [x.get()[0]['name'] for x in server_requests[key]]
            sw_results.server_results[key].sort()

    # TODO Display results
    log.write('----------------------------------------')
    log.write(f'Title   : {film_details["title"]}')
    log.write(f'Director: {film_details["director"]}')
    log.write(f'Producer: {film_details["producer"]}')
    log.write(f'Released: {film_details["release_date"]}')
    log.write_blank_line()

    for key, detail in film_details.items():
        if isinstance(detail, list):
            log.write(f'{key.title()}: {len(sw_results.server_results[key])}')
            log.write(', '.join(sw_results.server_results[key]))
            log.write_blank_line()

    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count + sw_results.call_counts} calls to the server')
    

if __name__ == "__main__":
    main()