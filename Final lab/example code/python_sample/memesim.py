import math

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

#suggestion: make different destination for every robot so a array with 3 variables
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
            angle[robot_id - 10] = ( float(resp.cmdargs()[4]) / (2*math.pi) )*360 #find angle and convert radians to degrees

    #print("Received response: " + str(resp))
    ZIGBEE.write(b'The program has started')

    data = readZIGBEE()
    if len(data) is not 0:
        print(data)

#FUNCTIONS:_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#

#NEXT_FUNCTION:
def navigate_to(destination, robot_id):
    update_position(robot_id)

    continent = find_continent(robot_id)
    if (continent == 'CON1'):
        drive_to(M1[0],M1[1], robot_id)
    if (continent == 'CON2'):
        drive_to(M2[0],M2[1], robot_id)
    if (continent == 'CON3'):
        drive_to(M3[0],M3[1], robot_id)
    if (continent == 'LAB'):
        drive_to(LAB[0],LAB[1], robot_id)
    #read_pos(10)

#update responses
def update_responses():
    # get new responses
    RESPONSES = MEMESIM_CLIENT.new_responses()

    # process new responses
    for r in RESPONSES:
        process_response(r)

#find current continents
def find_continent(robot_id):
    continent = None
    if x_pos[robot_id - 10]<1450 and y_pos[robot_id - 10]<1450:
        continent = "LAB"
    if x_pos[robot_id - 10]>2100 and y_pos[robot_id - 10]<1450:
        continent = "CON1"
    if x_pos[robot_id - 10]>2100 and y_pos[robot_id - 10]>2100:
        continent = "CON2"
    if x_pos[robot_id - 10]<1450 and y_pos[robot_id - 10]>2100:
        continent = "CON3"
    #print('continent = ', continent) #debug message
    return continent

def drive_to(x_goal, y_goal, robot_id):
    #print("entered drive_to function") #debug message
    update_position(robot_id)
    angle_difference_vector = alignment_angle(x_goal, y_goal, robot_id)

    if (abs(angle_difference_vector - angle[robot_id - 10]) > 8): # 8 is foutmarge
        if (angle_difference_vector - angle[robot_id - 10] < 0):
            while (angle_difference_vector - angle[robot_id - 10] < 0):
                print('Angle of difference vector is', angle_difference_vector)
                print('Angle of robot is', angle[robot_id - 10])
                ZIGBEE.write(b'r') #send: turn to right
                update_position(robot_id) #update position
                print("turn to right")
                sleep(0.3) #wait for stability

        elif (angle_difference_vector - angle[robot_id - 10] > 0):
            while (angle_difference_vector - angle[robot_id - 10] > 0):
                print('Angle of difference vector is', angle_difference_vector)
                print('Angle of robot is', angle[robot_id - 10])
                ZIGBEE.write(b'l') #send: turn to left
                update_position(robot_id) #update position
                print("turn to left")
                sleep(0.3) #wait for stability

        ZIGBEE.write(b's')
        print("stop turning")

#update position of robots: find x, y, and angle of robot
def update_position(robot_id):
    RQ1 = MemeSimCommand.RQ(4, robot_id) #make a request
    MEMESIM_CLIENT.send_command(RQ1) #send request
    sleep(1.0) #wait a bit
    update_responses() #find answers to responses: to x, y and angle

#find alginment angle of robot with goal
def alignment_angle(x_goal, y_goal, robot_id):
    difference_vector = [None] * 2
    difference_vector[0] = x_goal - x_pos[robot_id - 10]
    difference_vector[1] = y_goal - y_pos[robot_id - 10]

    angle_difference_vector = math.atan2(difference_vector[1], difference_vector[0]) * 180 / math.pi
    return angle_difference_vector

#read info from zigbee module
def readZIGBEE():
    data = str(ZIGBEE.read()) #read data as non string (dunno what it is) and convert to string
    data = data[2:len(data)-1] # delete begin b' and '
    return data #return

#read position of robot
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
    if (destination == 'C1' or destination == 'C2' or destination == 'C3' or destination == 'C4'):
        navigate_to(destination, 10)
    if (destination == 'C5' or destination == 'C6' or destination == 'C7' or destination == 'C8'):
        navigate_to(destination, 11)
    if (destination == 'C9' or destination == 'C10' or destination == 'C11' or destination == 'C12'):
        navigate_to(destination, 12)
