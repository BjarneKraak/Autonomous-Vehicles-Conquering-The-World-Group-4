import math

from time import sleep
from random import randint
from tkinter import Tk

# import code that is used
from lib.memegenome import MemeGenome
from lib.memesimcommand import MemeSimCommand
from lib.memesimresponse import MemeSimResponse
from lib.memesimclient import MemeSimClient
from lib.memesimresponse import MemeSimResponse
from lib.gui.memesimgui import MemeSimGUI
from lib.zigbee import Zigbee

# Global variables/constants that can be accessed from all functions should be defined below
x_pos = [None] * 3
y_pos = [None] * 3
angle = [None] * 3

genomes=[[]]*3
#genomes.append([])#list of processed genomes
Database=[[]]*3
#Database.append([])# database of people inteviewed

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
M1 = [2750, 750]
M2 = [2750, 2750]
M3 = [750, 2750]
MLAB = [750, 750]

# Create a Zigbee object for communication with the Zigbee dongle
# Make sure to set the correct COM port and baud rate!
# You can find the com port and baud rate in the xctu program.
ZIGBEE = Zigbee('COM12', 9600)

# set the simulator IP address
MEMESIM_IP_ADDR = "131.155.124.132"

# set the team number here
TEAM_NUMBER = 4
Robot=10
i = 0

# create a MemeSimClient object that takes car of all TCP communication with the simulator
MEMESIM_CLIENT = MemeSimClient(MEMESIM_IP_ADDR, TEAM_NUMBER)

# dictionary to hold a collection of memes
MY_MEMES = dict()

# create the GUI window
ROOT = Tk()
MEMESIM_GUI = MemeSimGUI(ROOT)
'''


'''
def rq():
    loop('rq')

def mq():
    loop('mq')

def ip():
    loop('ip')

def pi():
    loop('pi')

def tm():
    loop('tm')

def pc():
    loop('pc')

def lc():
    loop('lc')

def db():
    loop('db')

def set():
    loop("set")

def res():
    genomes[Robot-10].clear()
    Database[Robot-10].clear()
    People.clear()
    print("Reset done!")
    return

def rob1():
    global Robot
    Robot=10
    print("Robot 1 ready to be instructed")
    loop("rq")

def rob2():
    global Robot
    Robot=11
    print("Robot 2 ready to be instructed")
    loop("rq")

def rob3():
    global Robot
    Robot=12
    print("Robot 3 ready to be instructed")
    loop("rq")

def eur():
    drive_to(M1[0], M1[0], Robot)

def afr():
    drive_to(M2[0], M2[0], Robot)

def ame():
    drive_to(M3[0], M3[0], Robot)

def lab():
    drive_to(MLAB[0], MLAB[0], Robot)

def ein():
    drive_to(C1[0], C1[1], Robot)

def lon():
    drive_to(C2[0], C2[1], Robot)

def mad():
    drive_to(C3[0], C3[1], Robot)

def mil():
    drive_to(C4[0], C4[1], Robot)

def joh():
    drive_to(C5[0], C5[1], Robot)

def lag():
    drive_to(C6[0], C6[1], Robot)

def kha():
    drive_to(C7[0], C7[1], Robot)

def cai():
    drive_to(C8[0], C8[1], Robot)

def was():
    drive_to(C9[0], C9[1], Robot)

def bog():
    drive_to(C10[0], C10[1], Robot)

def atl():
    drive_to(C11[0], C11[1], Robot)

def lim():
    drive_to(C12[0], C12[1], Robot)

def lab4():
    drive_to(LAB[0], LAB[1], Robot)

# set the function to be called when the GUI buttin is clicked. the function is defined above
MEMESIM_GUI.rq(rq)
MEMESIM_GUI.mq(mq)
MEMESIM_GUI.ip(ip)
MEMESIM_GUI.pi(pi)
MEMESIM_GUI.tm(tm)
MEMESIM_GUI.pc(pc)
MEMESIM_GUI.lc(lc)
MEMESIM_GUI.db(db)
MEMESIM_GUI.set(set)
MEMESIM_GUI.res(res)

MEMESIM_GUI.rob1(rob1)
MEMESIM_GUI.rob2(rob2)
MEMESIM_GUI.rob3(rob3)

#continents:
MEMESIM_GUI.eur(eur)
MEMESIM_GUI.afr(afr)
MEMESIM_GUI.ame(ame)
MEMESIM_GUI.lab(lab)

#Contintent 1: Europe cities
MEMESIM_GUI.ein(ein)
MEMESIM_GUI.lon(lon)
MEMESIM_GUI.mad(mad)
MEMESIM_GUI.mil(mil)

#Contintent 2: africa cities
MEMESIM_GUI.joh(joh)
MEMESIM_GUI.lag(lag)
MEMESIM_GUI.kha(kha)
MEMESIM_GUI.cai(cai)

#Contintent 3: america cities
MEMESIM_GUI.was(was)
MEMESIM_GUI.bog(bog)
MEMESIM_GUI.atl(atl)
MEMESIM_GUI.lim(lim)

#Contintent labland
MEMESIM_GUI.lab4(lab4)

# the setup function is called once at startup
# you can put initialization code here
def setup():
    ''' The setup function is called once at startup. You can put initialization code here. '''

    # create a collection of random memes
#    for i in range(1, 11):
        #mgen = MemeGenome.random_meme_genome()
        # do some arbitrary things to it
        #mgen[0] = 'A'
        #mgen[99] = mgen[0]
        # store the meme in the dictionary MY_MEMES under a name as a string
        #MY_MEMES['Meme'+str(i)] = mgen

    # try to connect to the simulator
    if not MEMESIM_CLIENT.connect():
        print("Could not connect to the simulator.")
        exit()

    #ZIGBEE.write(b'The program has started')

    #set virtual position of robot 10;
    #RQS = [MemeSimCommand.RQ(TEAM_NUMBER,Robot) ]
    #update_loc(RQS,10, C4[0], C4[1],0)
    #send_commands(RQS)

    x_pos[0] = 100
    y_pos[0] = 100
    angle[0] = 30
    x_pos[1] = 2500
    x_pos[1] = 2500
    angle[1] = 50
    x_pos[2] = 1000
    x_pos[2] = 1000
    angle[2] = 300

# the process_response function is called when a response is received from the simulator
def process_response(resp):
    print("Received response: " + str(resp))
    global x_pos
    global y_pos
    global angle
    if not resp.iserror():
        if resp.cmdtype() == 'rq':
            robot_id = int(resp.cmdargs()[1])
            #save positions of robot
            x_pos[robot_id - 10] = float(resp.cmdargs()[2])
            y_pos[robot_id - 10] = float(resp.cmdargs()[3])
            angle[robot_id - 10] = ( float(resp.cmdargs()[4])/(2*math.pi) )*360 #find angle and convert radians to degrees
            if angle[robot_id - 10] < 0:
                angle[robot_id - 10] = angle[robot_id - 10] + 360
            MEMESIM_GUI.show_location(robot_id, x_pos[robot_id - 10], y_pos[robot_id - 10], angle[robot_id - 10]*(2*math.pi)/360)
        elif resp.cmdtype() == 'ca':
            # extract the data from the request
            balance = int(resp.cmdargs()[1])
            MEMESIM_GUI.show_balance(balance)
        #print("Received response: " + str(resp))
        #ZIGBEE.write(b'The program has started')
        elif resp.cmdtype() == 'mq':
            z = 0
            p = 0

            #print(nrofinterviews)
            global People
            size=50
            People=[0]*size

            for i in range(0,(int(nrofinterviews)+int(p))):
                try:
                    individual_id = int(resp.cmdargs()[3+i])
                except:
                    #print("No.. input string is not a number. It's a string")
                    #print((str(resp.cmdargs()[3+i])))
                    interview = resp.cmdargs()[3+i]
                    #interview = interview.replace(',',' ')
                    y = len(interview)
                    #print("person id",interview[0])
                    #print("meme one",interview[1])
                    #print("meme level",interview[2])
                    c = int((y-1)/2)
                    meme=[0]*c
                    level=[0]*c
                    meme[0]=interview[1]
                    level[0]=float(interview[2])
                    #print(c)
                    for x in range(1,int(c)):
                        meme[x]=interview[1+2*x]# number of memes for this person
                        level[x]=float(interview[2+2*x])
                    print
                    People[z]=[meme,level,interview[0]]

                    p = p+1
                    z += 1

            for x in range (0, z):
                print(x,'.',People[x])
            z=size-z
            People=People[:-z]
            #print(People)

        elif resp.cmdtype() == 'pi':
                genX = resp.cmdargs()[2]
                #print(genX)
                genomes[Robot-10].append(genX[1])

length =100
def ProduceGenome():
    genPerfect = []
    g = 0
    #print('in function ',genomes)
    while g < length:
        gens = 0
        occurences = [['A', 'C', 'T', 'G'],[0, 0, 0, 0]]
        while gens < len(genomes[Robot-10]):
            o = 0
            while o < len(occurences[0]):
                if occurences[0][o] in genomes[Robot-10][gens][g]:
                    occurences[1][o] += 1
                o += 1
            gens += 1
        often = 0
        howoften = 0
        mostoften = 0
        while often < len(occurences[0]):
            if occurences[1][often] > howoften:
                howoften = occurences[1][often]
                mostoften = often
            often += 1
        #print(g, occurences, mostoften)
        genPerfect.append(occurences[0][mostoften])
        g += 1

    text_file = open("Genomes.txt", "w")

    for i in range(0,len(genomes[Robot-10])):
        text=''.join(genomes[Robot-10][i])
        text_file.write(str(i))
        text_file.write(".  ")
        text_file.write(text)
        text_file.write("\n")




    FinalGen = ''.join(genPerfect)
    test_file.write(FinalGen)
    text_file.close()
    #print(FinalGen)
    printgen=[FinalGen]
    MEMESIM_GUI.show_meme(printgen[0])

    return FinalGen

#FUNCTIONS:_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#

#update responses
def update_responses():
    # get new responses
    RESPONSES = MEMESIM_CLIENT.new_responses()

    # process new responses
    for r in RESPONSES:
        process_response(r)

#drive to
def drive_to(x_goal, y_goal, robot_id):
    print("entered drive_to function") #debug message

    align_robot(x_goal, y_goal, robot_id)
    move_robot_x(x_goal, y_goal, robot_id)
    align_robot(x_goal, y_goal, robot_id)
    move_robot_y(x_goal, y_goal, robot_id)

#move aligned robot towards goal
def move_robot_x(x_goal, y_goal, robot_id):
    print("Entered move_robot function")
    update_position(robot_id)

    while (abs(x_goal - x_pos[robot_id - 10])  > 30 ): #or (abs(y_goal - y_pos[robot_id - 10]) ) > 100 ):
        send_zigbee_forward()

        #for updating virtual position of robot
        print("x_goal, y_goal =", x_goal, y_goal)
        print("x_loc, y_loc=",x_pos[robot_id-10], y_pos[robot_id-10])
        update_position(robot_id)

        print("move forward")
        sleep(0.3) #wait for stability


    send_zigbee_stop()
    print("stop driving, robot on right x")

def move_robot_y(x_goal, y_goal, robot_id):
    print("Entered move_robot function")
    update_position(robot_id)

    while (abs(y_goal - y_pos[robot_id - 10])  > 30 ): #or (abs(y_goal - y_pos[robot_id - 10]) ) > 100 ):
        send_zigbee_forward() #send: move forward

        #for updating virtual position of robot
        print("x_goal, y_goal =", x_goal, y_goal)
        print("x_loc, y_loc=",x_pos[robot_id-10], y_pos[robot_id-10])
        update_position(robot_id)

        print("move forward")
        sleep(0.3) #wait for stability

    send_zigbee_stop()
    print("stop driving, robot on right y")

def align_robot(x_goal, y_goal, robot_id):

#request positon robot 10
    update_position(robot_id)

    angle_difference_vector = alignment_angle(x_goal, y_goal, robot_id)
    print('Angle of difference vector is', angle_difference_vector)
    print('Angle of robot is', angle[robot_id - 10])

    while ( (abs(angle_difference_vector - angle[robot_id - 10]) ) > 5): # 5 is foutmarge
        if (angle_difference_vector - angle[robot_id - 10] >= 0):
            while (angle_difference_vector - angle[robot_id - 10] >= 0):

                #update_position(robot_id) #update position
                print('Angle of difference vector is', angle_difference_vector)
                print('Angle of robot is', angle[robot_id - 10])
                send_zigbee_left()

                print("turn to left")
                sleep(0.2)
                send_zigbee_stop()
                #sleep(0.5) #wait for stability
                update_position(robot_id) #update position
        elif (angle_difference_vector - angle[robot_id - 10] < 0):
            while (angle_difference_vector - angle[robot_id - 10] < 0):
                #update_position(robot_id) #update position
                print('Angle of difference vector is', angle_difference_vector)
                print('Angle of robot is', angle[robot_id - 10])
                send_zigbee_right()

                print("turn to right")
                sleep(0.2)
                send_zigbee_stop()
                #sleep(0.5)
                update_position(robot_id) #update position

            send_zigbee_stop()
            print("stop turning, robot aligned")

def send_zigbee_forward():
    if (Robot == 10):
        ZIGBEE.write(b'f')
    if (Robot == 11):
        ZIGBEE.write(b'x')
    if (Robot == 12):
        ZIGBEE.write(b'm')

def send_zigbee_backward():
    if (Robot == 10):
        ZIGBEE.write(b'b')
    if (Robot == 11):
        ZIGBEE.write(b'y')
    if (Robot == 12):
        ZIGBEE.write(b'n')

def send_zigbee_left():
    if (Robot == 10):
        ZIGBEE.write(b'l')
    if (Robot == 11):
        ZIGBEE.write(b'z')
    if (Robot == 12):
        ZIGBEE.write(b'o')

def send_zigbee_right():
    if (Robot == 10):
        ZIGBEE.write(b'r')
    if (Robot == 11):
        ZIGBEE.write(b'a')
    if (Robot == 12):
        ZIGBEE.write(b'p')

def send_zigbee_stop():
    if (Robot == 10):
        ZIGBEE.write(b's')
    if (Robot == 11):
        ZIGBEE.write(b'c')
    if (Robot == 12):
        ZIGBEE.write(b'q')

#update position of robots: find x, y, and angle of robot
def update_position(robot_id):
    RQ1 = MemeSimCommand.RQ(4, robot_id) #make a request
    MEMESIM_CLIENT.send_command(RQ1) #send request
    sleep(0.2) #wait a bit
    update_responses() #find answers to responses: to x, y and angle

#find alginment angle of robot with goal
def alignment_angle(x_goal, y_goal, robot_id):
    difference_vector = [None] * 2
    difference_vector[0] = x_goal - x_pos[robot_id - 10]
    difference_vector[1] = y_goal - y_pos[robot_id - 10]

    angle_difference_vector = math.atan2(difference_vector[1], difference_vector[0]) * 180 / math.pi
    if angle_difference_vector < 0:
        angle_difference_vector = angle_difference_vector + 360
    return angle_difference_vector

def send_commands(RQS):
    # send the requests to the simulator
    for req in RQS:
        MEMESIM_CLIENT.send_command(req)

def update_loc(RQS, robot_id,x,y,angle):
    global i
    RQS.append(MemeSimCommand.RS(TEAM_NUMBER,robot_id,x,y,(angle/360)*2*math.pi))

def loop(mode):
    '''This function is called over and over again.'''
    if mode=='rq':
        # create a list robot queries, one for each of the robots
        RQS = [MemeSimCommand.RQ(TEAM_NUMBER,Robot) ]
    elif mode=='mq':

        # add a request to check the account balance
        #so as to auto reset every market research
        number=input("How many individuals?")
        #number=int(MEMESIM_GUI.input.get())
        global nrofinterviews
        nrofinterviews = number
        RQS=[MemeSimCommand.MQ(TEAM_NUMBER,Robot,number)]
    elif mode=='ip':
        #print(People)
        pseudoID=int(input("Person to interview:"))
        RQS= [MemeSimCommand.IP(TEAM_NUMBER,Robot,People[pseudoID][2])]
        if len(Database[Robot-10])==0:
            Database[Robot-10]=[People[pseudoID]]
        else:
            Database[Robot-10].append(People[pseudoID])
            #print(Database[0][1][1])
        print(Database[0])
        print(Database[1])
        print(Database[2])
        #print(Database)
    elif mode=='pi':
        for i in range (0,len(Database[Robot-10])):
            print(i,"numero:",Database[Robot-10][i][1])
            RQS= [MemeSimCommand.PI(TEAM_NUMBER,Robot,Database[Robot-10][i][2])]
            for req in RQS:
                MEMESIM_CLIENT.send_command(req)
            sleep(1)
    elif mode=='tm':
        #genome=input("insert meme genome=")
        pseudoID=int(input("ID of the individual:"))
        meme_gen=ProduceGenome()
        meme_gen=input("Provide genome:")
        RQS= [MemeSimCommand.TM(TEAM_NUMBER,Robot,meme_gen,Database[Robot-10][pseudoID][2])]
    elif mode=='pc':
        memeName=input("Insert meme name:")
        meme_gen=ProduceGenome()
        RQS= [MemeSimCommand.PC(TEAM_NUMBER,Robot,memeName,meme_gen)]
        res()
    elif mode=='lc':
        memeName=input("Insert meme name:")
        budget=int(input("Budeget:"))
        RQS=[MemeSimCommand.LC(TEAM_NUMBER,Robot,memeName,budget)]
    elif mode=='db':
        RQS=[MemeSimCommand.DB(TEAM_NUMBER,'reset')]
        RQS=[MemeSimCommand.DB(TEAM_NUMBER,'reset')]
    elif mode=='set':
        xpos=int(input("Position x-axis:"))
        ypos=int(input("Position y-axis:"))
        angle=int(input("Angle:"))
        RQS=[MemeSimCommand.RS(TEAM_NUMBER,Robot,xpos,ypos,angle)]

    RQS.append(MemeSimCommand.CA(TEAM_NUMBER))
    if mode!='pi':
        for req in RQS:
            MEMESIM_CLIENT.send_command(req)

#END_OF_FUNCTIONS_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#
# call the setup function for initialization
setup()

# as long as the user did not close the GUI window continue
while not MEMESIM_GUI.is_closing:

    # get new responses from the simulator
    RESPONSES = MEMESIM_CLIENT.new_responses()

    # process the new responses
    for r in RESPONSES:
        process_response(r)

    # slow the loop down, updating the GUI at a higher rate to improve responsiveness of the GUI
    for _ in range(0, 10):
        # update GUI
        ROOT.update()
        sleep(0.1)

# disconnect from the simulator
MEMESIM_CLIENT.disconnect()
