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
Robot=10
i =0

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

def eur():
    loop('eur')

def afr():
    loop('afr')

def ame():
    loop('ame')

def lab():
    loop('lab')

def set():
    loop("set")

def res():
    genomes.clear()
    Database.clear()
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



# set the function to be called when the GUI buttin is clicked. the function is defined above
MEMESIM_GUI.rq(rq)
MEMESIM_GUI.mq(mq)
MEMESIM_GUI.ip(ip)
MEMESIM_GUI.pi(pi)
MEMESIM_GUI.tm(tm)
MEMESIM_GUI.pc(pc)
MEMESIM_GUI.lc(lc)
MEMESIM_GUI.db(db)
MEMESIM_GUI.eur(eur)
MEMESIM_GUI.set(set)
MEMESIM_GUI.res(res)

MEMESIM_GUI.rob1(rob1)
MEMESIM_GUI.rob2(rob2)
MEMESIM_GUI.rob3(rob3)
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

genomes=[] #list of processed genomes
Database=[]# database of people inteviewed

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
                genomes.append(genX[1])

length =100
def ProduceGenome():
    genPerfect = []
    g = 0
    #print('in function ',genomes)
    while g < length:
        gens = 0
        occurences = [['A', 'C', 'T', 'G'],[0, 0, 0, 0]]
        while gens < len(genomes):
            o = 0
            while o < len(occurences[0]):
                if occurences[0][o] in genomes[gens][g]:
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

    for i in range(0,len(genomes)):
        print(genomes[i])

    FinalGen = ''.join(genPerfect)
    print(FinalGen)
    printgen=[FinalGen]
    MEMESIM_GUI.show_meme(printgen[0])
    return FinalGen



def loop(mode):
    '''This function is called over and over again.'''
    if mode=='rq':
        # create a list robot queries, one for each of the robots
        RQS = [MemeSimCommand.RQ(TEAM_NUMBER,Robot) ]

    elif mode=='mq':
        # add a request to check the account balance
        #res() so as to auto reset every market research
        number=input("How many individuals?")
        global nrofinterviews
        nrofinterviews = number
        RQS=[MemeSimCommand.MQ(TEAM_NUMBER,Robot,number)]
    elif mode=='ip':
        #print(People)
        pseudoID=int(input("Person to interview"))
        RQS= [MemeSimCommand.IP(TEAM_NUMBER,Robot,People[pseudoID][2])]
        Database.append(People[pseudoID])
        print(Database)
    elif mode=='pi':
        for i in range (0,len(Database)):
            print(i,"numero:",Database[i][1])
            RQS= [MemeSimCommand.PI(TEAM_NUMBER,Robot,Database[i][2])]
            for req in RQS:
                MEMESIM_CLIENT.send_command(req)
            sleep(1)
    elif mode=='tm':
        #genome=input("insert meme genome=")
        pseudoID=int(input("ID of the individual"))
        meme_gen=ProduceGenome()
        RQS= [MemeSimCommand.TM(TEAM_NUMBER,Robot,meme_gen,Database[pseudoID][2])]
    elif mode=='pc':
        memeName=input("insert meme name=")
        meme_gen=ProduceGenome()
        RQS= [MemeSimCommand.PC(TEAM_NUMBER,Robot,memeName,meme_gen)]
    elif mode=='lc':
        memeName=input("insert meme name=")
        budget=int(input("Whats the budeget"))
        RQS=[MemeSimCommand.LC(TEAM_NUMBER,Robot,memeName,budget)]
    elif mode=='db':
        RQS=[MemeSimCommand.DB(TEAM_NUMBER,'money')]

    elif mode=='set':
        xpos=int(input("xpos="))
        ypos=int(input("ypos="))
        angle=20
        RQS=[MemeSimCommand.RS(TEAM_NUMBER,Robot,xpos,ypos,20)]

    RQS.append(MemeSimCommand.CA(TEAM_NUMBER))
        #RQS.append(MemeSimCommand.MQ(4,10,20))
        #i=i+1
        # send the requests to the simulator
    if mode!='pi':
        for req in RQS:
            MEMESIM_CLIENT.send_command(req)


    # make a random mutation to some meme at a random position


    # show the meme in the GUI


# call the setup function for initialization
setup()

# as long as the user did not close the GUI window continue
while not MEMESIM_GUI.is_closing:

    # get new responses from the simulator
    RESPONSES = MEMESIM_CLIENT.new_responses()


    for r in RESPONSES:
        process_response(r)



    # slow the loop down, updating the GUI at a higher rate to improve responsiveness of the GUI
    for _ in range(0, 10):
        # update GUI
        ROOT.update()
        sleep(0.1)

# disconnect from the simulator
MEMESIM_CLIENT.disconnect()
