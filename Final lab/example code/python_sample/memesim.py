from time import sleep

# import code that is used
from lib.memegenome import MemeGenome
from lib.memesimcommand import MemeSimCommand
from lib.memesimresponse import MemeSimResponse
from lib.memesimclient import MemeSimClient

# Global variables/constants that can be accessed from all functions should be defined below

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


# the process_response function is called when a response is received from the simulator
def process_response(resp):
    if resp.cmdtype() == 'rq':
        if not resp.iserror():
            robot_id = int(resp.cmdargs()[1])
            xpos = float(resp.cmdargs()[2])
            ypos = float(resp.cmdargs()[3])
            angle = float(resp.cmdargs()[4])
    print("Received response: " + str(resp))

# this function is called over and over again
def loop():
    # do something arbitray with the memes
    RQ1 = MemeSimCommand.RQ(1, 1)
    MEMESIM_CLIENT.send_command(RQ1)

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
