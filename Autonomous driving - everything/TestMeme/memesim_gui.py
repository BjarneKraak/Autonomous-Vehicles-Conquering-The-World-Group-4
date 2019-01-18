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
Robot=11
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
    print("RQ.")
    loop('rq')

def mq():
    print("mq")
    loop('mq')

def ip():
    print("ip.")
    loop('ip')

def pi():
    print("pi.")
    loop('pi')

def tm():
    print("tm")
    loop('tm')


def pc():
    print("pc")
    loop('pc')

def lc():
    print("lc")
    loop('lc')

def db():
    print("db")
    loop('db')

def eur():
    print("db")
    loop('eur')

def afr():
    print("db")
    loop('afr')

def ame():
    print("db")
    loop('ame')

def lab():
    print("db")
    loop('lab')

def set():
    print("set")
    loop("set")

def ein():
    print("db")
    loop('db')

def lon():
    print("db")
    loop('db')





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

            print(nrofinterviews)
            global People
            People=[0]*20

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
                print(People[x])




            coolmeme=DankestMemes(People) #start computing meme levels
            cooldude=CoolestDude(People,coolmeme) #start computing id with highest level
            print("end") #to know the script had made it to the end, can be removed later


def DankestMemes(dudes): #look for the most popular memes, by computing the total level of a meme
    memes = [[],[]] #start with an empty list of memes known to console
    d = 0 #reset the iteration for id's
    print(dudes)
    while d < len(dudes): #iterate through all found id's
        i = 0 #reset iteration of memes known by id
        while i < len(dudes[d][0][0]): #iterate through memes known by id
            m = 0 #reset iteration of memes known to console
            state = 0 #the meme known by this id is not known by the console untill proven otherwise
            while m < len(memes[0]): #iterate through memes known to console
                if memes[0][m] == dudes[d][0][i]: #if the meme of the id is known by the console, do:
                    memes[1][m] = memes[1][m]+dudes[d][1][i] #add level of id to known level
                    state = 1 #the meme is known by the console
                m+=1 #iterate to next meme known by console
            if state == 0: #if the meme is not known, add it to the list of known memes
                memes[0].append(dudes[d][0][i]) #add meme name to end of list
                memes[1].append(dudes[d][1][i]) #add meme level to end of list
            i+=1 #iterate to next meme known to id
        d+=1 #iterate to next id
    return memes#end function

def CoolestDude(dudes,memes):
    d = 0 #reset the iteration for id's
    print(dudes)
    coolness = [[],[]] #reset list of id level
    while d < len(dudes): #iterate through all found id's
        coolness[0].append(dudes[d]) #add id name to end of list
        coolness[1].append(0) #add id level (which begins at 0) to end of list
        i = 0 #reset iteration of memes known by id
        while i < len(dudes[d][0]): #iterate through memes known by id
            m = 0 #reset iteration of memes known to console
            while m < len(memes[0]): #iterate through memes known by console
                if memes[0][m] == dudes[d][0][i]: #if the meme names from the id and console compare, do:
                    #add total meme level multiplied by the id specific meme level to the id's total level
                    coolness[1][d] = coolness[1][d]+(memes[1][m]*dudes[d][1][i])
                m+=1 #iterate to next meme known by console
            i+=1 #iterate to next meme known by id
        d+=1 #iterate to next id
    highest = 0 #reset counter for the highest id level
    c = 0 #reset iteration of id levels
    while c < len(coolness[1]): #iterate through id levels
        if coolness[1][c] > highest: #if a level is higher than the previous highest, do:
            highest = coolness[1][c] #set highest level to the level of the current id
            highestid = c #set id with highest level
        c+=1 #iterate to next id level
    print(dudes[highestid][2]) #return id with the highest level
    return dudes[highestid][2]#end of function



def loop(mode):
    '''This function is called over and over again.'''
    if mode=='rq':
        # create a list robot queries, one for each of the robots
        RQS = [MemeSimCommand.RQ(TEAM_NUMBER,Robot) ]
    elif mode=='mq':
        # add a request to check the account balance
        number=input("How many individuals?")
        global nrofinterviews
        nrofinterviews = number
        RQS=[MemeSimCommand.MQ(TEAM_NUMBER,Robot,number)]
    elif mode=='ip':
        ID=input("ID of the individual to interview")
        RQS= [MemeSimCommand.IP(TEAM_NUMBER,Robot,ID)]
    elif mode=='pi':
        ID=input("ID of the individual to interview")
        RQS= [MemeSimCommand.PI(TEAM_NUMBER,Robot,ID)]
    elif mode=='tm':
        #genome=input("insert meme genome=")
        ID=input("ID of the individual")
        meme_gen='CCCTTTAAACCCTTTAAACCCTTTAAACCCTTTAAACCCTTTAAACCCTTTAAACCCTTTAAACCCTTTAAACCCTTTAAACCTTTAAACCCTTTAAACC'
        RQS= [MemeSimCommand.TM(TEAM_NUMBER,Robot,meme_gen,ID)]
    elif mode=='pc':
        memeN=input("insert meme name=")
        meme_gen='CCCTTTAAACCCTTTAAACCCTTTAAACCCTTTAAACCCTTTAAACCCTTTAAACCCTTTAAACCCTTTAAACCCTTTAAACCTTTAAACCCTTTAAACC'
        RQS= [MemeSimCommand.PC(TEAM_NUMBER,Robot,memeN,meme_gen)]
    elif mode=='lc':
        memeN=input("insert meme name=")
        RQS=[MemeSimCommand.LC(TEAM_NUMBER,Robot,memeN,100)]
    elif mode=='db':
        RQS=[MemeSimCommand.DB(TEAM_NUMBER,'reset')]
    elif mode=='eur':
        RQS=[MemeSimCommand.DB(TEAM_NUMBER,'reset')]
    elif mode=='set':
        xpos=int(input("xpos="))
        ypos=int(input("ypos="))
        angle=20
        RQS=[MemeSimCommand.RS(TEAM_NUMBER,Robot,xpos,ypos,20)]

    RQS.append(MemeSimCommand.CA(TEAM_NUMBER))
        #RQS.append(MemeSimCommand.MQ(4,10,20))
        #i=i+1
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
    #loop()


    # slow the loop down, updating the GUI at a higher rate to improve responsiveness of the GUI
    for _ in range(0, 10):
        # update GUI
        ROOT.update()
        sleep(0.1)

# disconnect from the simulator
MEMESIM_CLIENT.disconnect()
