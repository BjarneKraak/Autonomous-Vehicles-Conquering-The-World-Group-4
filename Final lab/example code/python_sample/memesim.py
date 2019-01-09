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

destination = "C1"

#Location of all cities and lab
#Contintent 1:
C1 = [2550, 250]
C2 = [3250, 250]
C3 = [3250, 950]
C4 = [2550, 1250]

#continent 2:
C5 = [3250, 2550]
C6 = [3250, 3250]
C7 = [2550, 3250]
C8 = [2250, 2250]

#continent 3:
C9 = [950, 3250]
C10 = [250, 3250]
C11 = [250, 2250]
C12 = [1250, 2250]

#lab (4):
LAB = [175, 1025]

#middle of continents
M1 = [1750, 875]
M2 = [4375, 4375]
M3 = [875, 1750]
MLAB = [875, 875]

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
    global x_pos
    global y_pos
    global angle
    if resp.cmdtype() == 'rq':
        if not resp.iserror():
            robot_id = int(resp.cmdargs()[1])
            #save positions of robot
            x_pos[robot_id - 10] = float(resp.cmdargs()[2])
            y_pos[robot_id - 10] = float(resp.cmdargs()[3])
            angle[robot_id - 10] = float(resp.cmdargs()[4])

    #print("Received response: " + str(resp))
    ZIGBEE.write(b'The program has started')

    data = readZIGBEE()
    if len(data) is not 0:
        print(data)

#FUNCTIONS:_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#

#NEXT_FUNCTION:
def navigate_to(x_goal, y_goal):
    RQ1 = MemeSimCommand.RQ(4, 10)
    MEMESIM_CLIENT.send_command(RQ1)
    sleep(1.0)
    update_responses()
    #continent = find_continent()
    read_pos(10)

#update responses
def update_responses():
    # get new responses
    RESPONSES = MEMESIM_CLIENT.new_responses()

    # process new responses
    for r in RESPONSES:
        process_response(r)

#find current continents
def find_continent():
    continent = None
    if x_pos<1450 and y_pos<1450:
        continent = "LAB"
    if x_pos>2100 and y_pos<1450:
        continent = "CON1"
    if x_pos<1450 and y_pos<1450:
        continent = "CON2"
    if x_pos<1450 and y_pos<1450:
        continent = "CON3"
    return continent

#read zigbee module
def readZIGBEE():
    data = str(ZIGBEE.read()) #read data as non string (dunno what it is) and convert to string
    data = data[2:len(data)-1] # delete begin b' and '
    return data #return

#Next function

def read_pos(robot_id):

    global x_pos
    global y_pos
    global angle

    print( x_pos[robot_id - 10] )
    print( y_pos[robot_id - 10] )
    print( angle[robot_id - 10] )
#END_OF_FUNCTIONS_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#
# call the setup function for initialization
setup()

while True:
    if (destination == 'C1'):
        navigate_to(C1[0], C1[1])
