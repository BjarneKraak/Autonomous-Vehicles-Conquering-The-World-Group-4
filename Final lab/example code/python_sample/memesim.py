from time import sleep

# import code that is used
from lib.memegenome import MemeGenome
from lib.memesimcommand import MemeSimCommand
from lib.memesimresponse import MemeSimResponse
from lib.memesimclient import MemeSimClient

from lib.zigbee import Zigbee

# Global variables/constants that can be accessed from all functions should be defined below
x_pos = [None] * 3
y_pos = [None] * 3
angle = [None] * 3

# Create a Zigbee object for communication with the Zigbee dongle
# Make sure to set the correct COM port and baud rate!
# You can find the com port and baud rate in the xctu program.
ZIGBEE = Zigbee('COM12', 9600)

# set the simulator IP address
MEMESIM_IP_ADDR = "131.155.124.132"

# set the team number here
TEAM_NUMBER = 4

# create a MemeSimClient object that takes car of all TCP communication with the simulator
MEMESIM_CLIENT = MemeSimClient(MEMESIM_IP_ADDR, TEAM_NUMBER)

# dictionary to hold a collection of memes
MY_MEMES = dict()

# the setup function is called once at startup
# you can put initialization code here
def setup():

    # create a collection of random memes
    for i in range(0, 10):
        mg = MemeGenome.random_meme_genome()
        mg[0] = 'A'
        mg[99] = mg[0]
        MY_MEMES['Meme'+str(i)] = mg

    # connect to the simulator
    MEMESIM_CLIENT.connect()

    ZIGBEE.write(b'The program has started')

# the process_response function is called when a response is received from the simulator
def process_response(resp):
    if resp.cmdtype() == 'rq':
        if not resp.iserror():
            robot_id = int(resp.cmdargs()[1])
            print(robot_id)
            #save positions of robot
            x_pos[robot_id-10] = float(resp.cmdargs()[2])
            y_pos[robot_id-10] = float(resp.cmdargs()[3])
            angle[robot_id-10] = float(resp.cmdargs()[4])
    print("Received response: " + str(resp))
    ZIGBEE.write(b'The program has started')

    data = readZIGBEE()
    if len(data) is not 0:
        print(data)
#FUNCTIONS:_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#
# this function is called over and over again
def loop():
    # do something arbitray with the memes
    RQ1 = MemeSimCommand.RQ(4, 10)
    MEMESIM_CLIENT.send_command(RQ1)

#NEXT_FUNCTION:
def readZIGBEE():
    data = str(ZIGBEE.read()) #read data as non string (dunno what it is) and convert to string
    data = data[2:len(data)-1] # delete begin b' and '
    return data #return
#END_OF_FUNCTIONS_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#
# call the setup function for initialization
setup()

while True:
    # get new responses
    RESPONSES = MEMESIM_CLIENT.new_responses()

    # process new responses
    for r in RESPONSES:
        process_response(r)

    # call the loop function
    loop()

    # slow the loop down
    sleep(2.0)
