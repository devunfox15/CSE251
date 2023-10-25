"""
Course: CSE 251
Lesson Week: 06
File: assignment.py
Author: <Devun Durst>
Purpose: Processing Plant
Instructions:
- Implement the classes to allow gifts to be created.
"""
from multiprocessing import Process, Value, Array
import random
import multiprocessing as mp
import os.path
import time
import datetime

# Include cse 251 common Python files - Don't change
from cse251 import *

CONTROL_FILENAME = 'settings.txt'
BOXES_FILENAME   = 'boxes.txt'

# Settings consts
MARBLE_COUNT = 'marble-count'
CREATOR_DELAY = 'creator-delay'
NUMBER_OF_MARBLES_IN_A_BAG = 'bag-count'
BAGGER_DELAY = 'bagger-delay'
ASSEMBLER_DELAY = 'assembler-delay'
WRAPPER_DELAY = 'wrapper-delay'

# No Global variables

class Bag():
    """ bag of marbles - Don't change """

    def __init__(self):
        self.items = []

    def add(self, marble):
        self.items.append(marble)

    def get_size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)

class Gift():
    """ Gift of a large marble and a bag of marbles - Don't change """

    def __init__(self, large_marble, marbles):
        self.large_marble = large_marble
        self.marbles = marbles

    def __str__(self):
        marbles = str(self.marbles)
        marbles = marbles.replace("'", "")
        return f'Large marble: {self.large_marble}, marbles: {marbles[1:-1]}'


class Marble_Creator(mp.Process):
    """ This class "creates" marbles and sends them to the bagger """

    colors = ('Gold', 'Orange Peel', 'Purple Plum', 'Blue', 'Neon Silver', 
        'Tuscan Brown', 'La Salle Green', 'Spanish Orange', 'Pale Goldenrod', 'Orange Soda', 
        'Maximum Purple', 'Neon Pink', 'Light Orchid', 'Russian Violet', 'Sheen Green', 
        'Isabelline', 'Ruby', 'Emerald', 'Middle Red Purple', 'Royal Orange', 'Big Dip O’ruby', 
        'Dark Fuchsia', 'Slate Blue', 'Neon Dark Green', 'Sage', 'Pale Taupe', 'Silver Pink', 
        'Stop Red', 'Eerie Black', 'Indigo', 'Ivory', 'Granny Smith Apple', 
        'Maximum Blue', 'Pale Cerulean', 'Vegas Gold', 'Mulberry', 'Mango Tango', 
        'Fiery Rose', 'Mode Beige', 'Platinum', 'Lilac Luster', 'Duke Blue', 'Candy Pink', 
        'Maximum Violet', 'Spanish Carmine', 'Antique Brass', 'Pale Plum', 'Dark Moss Green', 
        'Mint Cream', 'Shandy', 'Cotton Candy', 'Beaver', 'Rose Quartz', 'Purple', 
        'Almond', 'Zomp', 'Middle Green Yellow', 'Auburn', 'Chinese Red', 'Cobalt Blue', 
        'Lumber', 'Honeydew', 'Icterine', 'Golden Yellow', 'Silver Chalice', 'Lavender Blue', 
        'Outrageous Orange', 'Spanish Pink', 'Liver Chestnut', 'Mimi Pink', 'Royal Red', 'Arylide Yellow', 
        'Rose Dust', 'Terra Cotta', 'Lemon Lime', 'Bistre Brown', 'Venetian Red', 'Brink Pink', 
        'Russian Green', 'Blue Bell', 'Green', 'Black Coral', 'Thulian Pink', 
        'Safety Yellow', 'White Smoke', 'Pastel Gray', 'Orange Soda', 'Lavender Purple',
        'Brown', 'Gold', 'Blue-Green', 'Antique Bronze', 'Mint Green', 'Royal Blue', 
        'Light Orange', 'Pastel Blue', 'Middle Green')

    def __init__(self, creator_conn,settings):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.creator_conn = creator_conn
        self.settings = settings
    def run(self):
        '''
        for each marble:
            send the marble (one at a time) to the bagger
              - A marble is a random name from the colors list above
            sleep the required amount
        Let the bagger know there are no more marbles
        '''
        for _ in range(self.settings[MARBLE_COUNT]):  # Repeat for the specified number of marbles
            random_marble = random.choice(Marble_Creator.colors)
            self.creator_conn.send(random_marble)
            time.sleep(self.settings[CREATOR_DELAY])
        
        # Signal to the bagger that there are no more marbles
        self.creator_conn.send(None)


class Bagger(mp.Process):
    """ Receives marbles from the marble creator, then there are enough
        marbles, the bag of marbles are sent to the assembler """
    def __init__(self, bagger_conn_rec, bagger_conn_send, settings):
        mp.Process.__init__(self)
        self.bagger_conn_rec = bagger_conn_rec
        self.bagger_conn_send = bagger_conn_send
        self.settings = settings

    def run(self):
        '''
        while there are marbles to process
            collect enough marbles for a bag
            send the bag to the assembler
            sleep the required amount
        tell the assembler that there are no more bags
        '''
        bag = []  # List to collect marbles for a bag
        while True:
            # Receive marbles from the marble creator
            marble = self.bagger_conn_rec.recv()
            # print("random marble recieved") #debugging tool

            if marble is None: #this send the list of marbles in a bag then shoots out a none
            
                self.bagger_conn_send.send(None) #tells assembler their are no bags
                break
            else: #
                bag.append(marble)
                if len(bag) >= self.settings[NUMBER_OF_MARBLES_IN_A_BAG]:
                    # We have enough marbles for a bag, send the bag to the assembler
                    self.bagger_conn_send.send(bag)
                    bag = []  # Clear the bag
                    time.sleep(self.settings[BAGGER_DELAY])
            

class Assembler(mp.Process):
    """ Take the set of marbles and create a gift from them.
        Sends the completed gift to the wrapper """
    marble_names = ('Lucky', 'Spinner', 'Sure Shot', 'Big Joe', 'Winner', '5-Star', 'Hercules', 'Apollo', 'Zeus')

    def __init__(self, assembler_conn_rec, assembler_conn_send, settings, gift_count:mp.Value):
        mp.Process.__init__(self)
        self.assembler_conn_rec = assembler_conn_rec
        self.assembler_conn_send = assembler_conn_send
        self.settings = settings
        self.gift_count = gift_count

    def run(self):
        '''
        while there are bags to process
            create a gift with a large marble (random from the name list) and the bag of marbles
            send the gift to the wrapper
            sleep the required amount
        tell the wrapper that there are no more gifts
        '''
        while True:
            # Receive bags from the bagger
            bag = self.assembler_conn_rec.recv()
            # print("bagger recieved")

            if bag is None:
                # No more bags to process, inform the wrapper and exit the loop
                self.assembler_conn_send.send(None)
                break
            else:
                # Create a gift with a large marble (random from the name list) and the bag of marbles
                large_marble = random.choice(Assembler.marble_names)
                gift = (f'Large marble: {large_marble}, marbles: {bag}')

                # Send the gift to the wrapper
                self.assembler_conn_send.send(gift)
                # print("gift sent")
                # Increment the item count
                self.gift_count.value += 1

                # Sleep for the required amount
                time.sleep(self.settings[ASSEMBLER_DELAY])


class Wrapper(mp.Process):
    """ Takes created gifts and wraps them by placing them in the boxes file """
    def __init__(self, wrapper_conn, boxes_filename, settings):
        mp.Process.__init__(self)
        self.wrapper_conn = wrapper_conn
        self.boxes_filename = boxes_filename
        self.settings = settings

    def run(self):
        '''
        open file for writing
        while there are gifts to process
            save gift to the file with the current time
            sleep the required amount
        '''
        with open(self.boxes_filename, 'w') as boxes_file:
            while True:
                # Receive gifts from the assembler
                # print("gift wrapped")
                gift = self.wrapper_conn.recv()

                if gift is None:
                    # No more gifts to process, exit the loop
                    break
                else:
                    # Save the gift to the file with the current time
                    current_time = datetime.now().time()
                    gift_str = f"Created - {current_time}: {gift}\n"
                    boxes_file.write(gift_str)

                    # Sleep for the required amount
                    time.sleep(self.settings[WRAPPER_DELAY])

def display_final_boxes(filename, log):
    """ Display the final boxes file to the log file -  Don't change """
    if os.path.exists(filename):
        log.write(f'Contents of {filename}')
        with open(filename) as boxes_file:
            for line in boxes_file:
                log.write(line.strip())
    else:
        log.write_error(f'The file {filename} doesn\'t exist.  No boxes were created.')



def main():
    """ Main function """

    log = Log(show_terminal=True)

    log.start_timer()

    # Load settings file
    settings = load_json_file(CONTROL_FILENAME)
    if settings == {}:
        log.write_error(f'Problem reading in settings file: {CONTROL_FILENAME}')
        return

    log.write(f'Marble count     = {settings[MARBLE_COUNT]}')
    log.write(f'Marble delay     = {settings[CREATOR_DELAY]}')
    log.write(f'Marbles in a bag = {settings[NUMBER_OF_MARBLES_IN_A_BAG]}') 
    log.write(f'Bagger delay     = {settings[BAGGER_DELAY]}')
    log.write(f'Assembler delay  = {settings[ASSEMBLER_DELAY]}')
    log.write(f'Wrapper delay    = {settings[WRAPPER_DELAY]}')

    # TODO: create Pipes between creator -> bagger -> assembler -> wrapper
    creator_conn_send, bagger_conn_rec = mp.Pipe()
    bagger_conn_send, assembler_conn_rec = mp.Pipe()
    assembler_conn_send, wrapper_conn = mp.Pipe()

    # TODO create variable to be used to count the number of gifts
    gift_count = mp.Value('i', 0)
    # delete final boxes file
    if os.path.exists(BOXES_FILENAME):
        os.remove(BOXES_FILENAME)

    log.write('Create the processes')

    # TODO Create the processes (ie., classes above)
    p1 = Marble_Creator(creator_conn_send, settings)
    p2 = Bagger(bagger_conn_rec, bagger_conn_send, settings)
    p3 = Assembler(assembler_conn_rec, assembler_conn_send, settings, gift_count)
    p4 = Wrapper(wrapper_conn, BOXES_FILENAME, settings)

    log.write('Starting the processes')
    # TODO add code here
    p1.start() 
    p2.start() 
    p3.start() 
    p4.start()

    log.write('Waiting for processes to finish')
    # TODO add code here
    p1.join() 
    p2.join() 
    p3.join() 
    p4.join()

    display_final_boxes(BOXES_FILENAME, log)
    
    # TODO Log the number of gifts created.
    log.write(f'Number of gifts created: {gift_count.value}')



if __name__ == '__main__':
    main()

