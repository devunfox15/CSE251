"""
Course: CSE 251
Lesson Week: 02 - Team Activity
File: team.py
Author: Brother Comeau

Purpose: Playing Card API calls
"""

from datetime import datetime, timedelta
import threading
import requests
import json

# # Include cse 251 common Python files
from cse251 import *

class Request_thread(threading.Thread):

    def __init__(self, url):
        # Call the Thread class's init function
        threading.Thread.__init__(self)
        self.url = url
        self.response = {} #this is a dictionary

    def run(self):
        response = requests.get(self.url)
        # Check the status code to see if the request succeeded.
        if response.status_code == 200:
            self.response = response.json()
        else:
            print('RESPONSE = ', response.status_code)


class Deck:

    def __init__(self, deck_id):
        self.id = deck_id
        self.reshuffle()
        self.remaining = 52


    def reshuffle(self):
        req = Request_thread(rf'https://deckofcardsapi.com/api/deck/{self.id}/shuffle/')
        req.start()
        req.join()


    def draw_card(self):
        req = Request_thread(rf'https://deckofcardsapi.com/api/deck/{self.id}/draw/')
        req.start()
        req.join()
        if req.response != {}:
            self.remaining = req.response['remaining']
            return req.response['cards'][0]['code']
        else:
            return ''

    def cards_remaining(self):
        return self.remaining


    def draw_endless(self):
        if self.remaining <= 0:
            self.reshuffle()
        return self.draw_card()


if __name__ == '__main__':

    # TODO - run the program team_get_deck_id.py and insert
    #        the deck ID here.  You only need to run the 
    #        team_get_deck_id.py program once. You can have
    #        multiple decks if you need them

    deck_id = 'h0k2gue5dyzb'

    deck = Deck(deck_id)

    for i in range(55):
        card = deck.draw_endless()
        print(f'card {i + 1}: {card}', flush=True)

    print()




#     from datetime import datetime
# import requests
# import json
# import threading
# from cse251 import Log

# # Define the TOP_API_URL constant
# TOP_API_URL = 'http://127.0.0.1:8790'

# # Define a threaded class for making API requests
# class RequestThread(threading.Thread):
#     def __init__(self, url):
#         super().__init__()
#         self.url = url
#         self.response_data = None

#     def run(self):
#         # Inside the run method, make the API request
#         response = requests.get(self.url)
#         if response.status_code == 200:
#             self.response_data = response.json()
#         else:
#             print(f'Error in retrieving data from {self.url}')

# # Define a function to retrieve data for a specific category
# def retrieve_data(category):
#     url = f'{TOP_API_URL}/{category}/'
#     thread = RequestThread(url)
#     thread.start()
#     thread.join()
#     return thread.response_data or []  # Return an empty list if data is None


# # Define a function to display category data
# def display_category_data(current_time, category, data):
#     print(f'{current_time}| {category}: {len(data)}')
#     if data:
#         names = ', '.join(sorted([item['name'] for item in data]))
#         print(f'{current_time}| {names}')
#     else:
#         print(f'{current_time}| {category}: No data available')
#     print(f'{current_time}|')

# # Define the main function
# def main():
#     # Get the current time
#     current_time = datetime.now().strftime('%H:%M:%S')

#     # Print the starting message
#     print(f'{current_time}| Starting to retrieve data from the server')

#     # Retrieve the top API URLs
#     top_api_urls = retrieve_data('')

#     # Retrieve details on film 6
#     film_data = retrieve_data('films/6')

#     # Print film details
#     print(f'{current_time}| {"-" * 40}')
#     print(f'{current_time}| Title   : {film_data["title"]}')
#     print(f'{current_time}| Director: {film_data["director"]}')
#     print(f'{current_time}| Producer: {film_data["producer"]}')
#     print(f'{current_time}| Released: {film_data["release_date"]}')
#     print(f'{current_time}|')

#     # Retrieve and display data for other categories
#     categories = [
#         ('Characters', 'people'),
#         ('Planets', 'planets'),
#         ('Starships', 'starships'),
#         ('Vehicles', 'vehicles'),
#         ('Species', 'species')
#     ]

#     for category_name, category_key in categories:
#         category_data = retrieve_data(category_key)
#         display_category_data(current_time, category_name, category_data)

# # Entry point of the program
# if __name__ == "__main__":
#     main()