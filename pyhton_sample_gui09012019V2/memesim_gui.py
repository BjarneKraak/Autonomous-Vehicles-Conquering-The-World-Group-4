from math import pi

# imports from standard modules
from time import sleep
from random import randint
from tkinter import Tk

# import code that is used from our own modules
from lib.memegenome import MemeGenome
from lib.memesimcommand import MemeSimCommand
from lib.memesimresponse import MemeSimResponse
from lib.memesimclient import MemeSimClient
from lib.gui.memesimgui import MemeSimGUI


# Global variables/constants that can be accessed from all functions should be defined below

# set the simulator IP address
MEMESIM_IP_ADDR = "131.155.124.132"

# set the team number here
TEAM_NUMBER = 4
i = 0

# create a MemeSimClient object that takes car of all TCP communication with the simulator
MEMESIM_CLIENT = MemeSimClient(MEMESIM_IP_ADDR, TEAM_NUMBER)

# dictionary to hold a collection of memes
MY_MEMES = dict()

# create the GUI window
ROOT = Tk()
MEMESIM_GUI = MemeSimGUI(ROOT)

def button_function():
    '''this function will be executed when the user clicks the button in the GUI'''
    print("Button clicked.")

# set the function to be called when the GUI buttin is clicked. the function is defined above
MEMESIM_GUI.set_button_callback(button_function)

def setup():
    ''' The setup function is called once at startup. You can put initialization code here. '''

    # create a collection of random memes
    for i in range(1, 11):
        mgen = MemeGenome.random_meme_genome()
        # do some arbitrary things to it
        mgen[0] = 'A'
        mgen[99] = mgen[0]
        # store the meme in the dictionary MY_MEMES under a name as a string
        MY_MEMES['Meme'+str(i)] = mgen

    # try to connect to the simulator
    if not MEMESIM_CLIENT.connect():
        print("Could not connect to the simulator.")
        exit()

    # create a list robot queries, one for each of the robots
    RQS = [MemeSimCommand.RQ(TEAM_NUMBER, (TEAM_NUMBER-1)*3+r) for r in range(1, 2)]

    # add a request to check the account balance
    RQS.append(MemeSimCommand.CA(TEAM_NUMBER))
    RQS.append(MemeSimCommand.RS(TEAM_NUMBER,10,150,150,2*pi))
    RQS.append(MemeSimCommand.RS(TEAM_NUMBER,11,150,150,2*pi))
    RQS.append(MemeSimCommand.RS(TEAM_NUMBER,12,150,150,2*pi))

    # send the requests to the simulator
    for req in RQS:
        MEMESIM_CLIENT.send_command(req)

    RESPONSES = MEMESIM_CLIENT.new_responses()

def process_response(resp):
    '''The process_response function is called when a response is received from the simulator.'''
    print("Received response: " + str(resp))

    # process robot query requests
    # if it is a vlid response only
    if not resp.iserror():
        if resp.cmdtype() == 'rq':
            # extract the data from the request
            robot_id = int(resp.cmdargs()[1])
            xpos = float(resp.cmdargs()[2])
            ypos = float(resp.cmdargs()[3])
            angle = float(resp.cmdargs()[4])
            # show the received data in the GUI window
            MEMESIM_GUI.show_location(robot_id, xpos, ypos, angle)
        elif resp.cmdtype() == 'ca':
            # extract the data from the request
            balance = int(resp.cmdargs()[1])
            MEMESIM_GUI.show_balance(balance)


def loop():
    '''This function is called over and over again.'''

    global i
    # do something arbitray. To be adapted.

    # create a list robot queries, one for each of the robots
    RQS = [MemeSimCommand.RQ(TEAM_NUMBER, (TEAM_NUMBER-1)*3+r) for r in range(1, 2)]

    # add a request to check the account balance
    RQS.append(MemeSimCommand.CA(TEAM_NUMBER))
    RQS.append(MemeSimCommand.RS(TEAM_NUMBER,10,150,150,(i/360)*2*pi))
    i=i+5
    # send the requests to the simulator

    for req in RQS:
        MEMESIM_CLIENT.send_command(req)



    # make a random mutation to some meme at a random position
    MY_MEMES['Meme1'][randint(0, 99)] = MemeGenome.Nucleotides[randint(0, 3)]

    # show the meme in the GUI
    MEMESIM_GUI.show_meme(MY_MEMES['Meme1'])


# call the setup function for initialization
setup()

# as long as the user did not close the GUI window continue
while not MEMESIM_GUI.is_closing:

    # get new responses from the simulator
    RESPONSES = MEMESIM_CLIENT.new_responses()

    # process the new responses
    for r in RESPONSES:
        process_response(r)

    # call the loop function
    loop()

    # slow the loop down, updating the GUI at a higher rate to improve responsiveness of the GUI
    for _ in range(0, 10):
        # update GUI
        ROOT.update()
        sleep(0.1)

# disconnect from the simulator
MEMESIM_CLIENT.disconnect()
