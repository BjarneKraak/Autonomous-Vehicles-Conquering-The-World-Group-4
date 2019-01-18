""" Client to connect to a locatemarkers program to receive the marker data, do some computation on that data and show how to communicate on the Zigbee connection.
"""
import math # IMPORT MATH PACKAGE
import time # IMPORT TIME PACKAGE
import socket
import re
from time import sleep

from marker import Marker, MarkerCollection, MARKER_REGEX
from zigbee import Zigbee

#Create global vars
ORIGIN = 0
ROBOTA = 0
OB1 = 0
OB2 = 0
OB3 = 0
FINISH = 0

# forget markers after not seeing them for 10 seconds
MARKER_TIMEOUT = 0.5

# Create a marker collection and register known markers with their numbers.
MARKERS = MarkerCollection()
MARKERS.add_marker('origin', 0)
MARKERS.add_marker('finish', 1)
MARKERS.add_marker('ob1', 2)
MARKERS.add_marker('ob2', 3)
MARKERS.add_marker('ob3', 4)
MARKERS.add_marker('robotA', 5)

# connect to the locatemarkers program tcp server
# IP address for the connection '127.0.0.1' means 'this computer'
TCP_IP = '127.0.0.1'
# The program listens on port 4242
TCP_PORT = 4242
# create an IP socket for communication
LMSOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect the socket to the server
LMSOCKET.connect((TCP_IP, TCP_PORT))
# set the socket to non-blocking, so calls to 'recv' will not block when there is no information to receive from the connection
LMSOCKET.setblocking(0)

# Create a Zigbee object for communication with the Zigbee dongle
# Make sure to set the correct COM port and baud rate!
# You can find the com port and baud rate in the xctu program.
ZIGBEE = Zigbee('COM12', 9600)

# DATA holds the unprocessed data from the connection. Its length will be limited to BUFFER_SIZE
BUFFER_SIZE = 1024
DATA = b"" #also global

## FUNCTIONS

def updatemarker():
    # check the data against the marker regular expression to check if there is complete marker information in the received data
    global DATA
    MARKER_RE_MATCH = re.search(MARKER_REGEX, DATA)

    # as long as we still have more complete marker information...
    while MARKER_RE_MATCH != None:
        # find the first marker information from the received data
        MARKER = Marker(MARKER_RE_MATCH.group())
        # show that we have found something
        #print("Found marker {0}.".format(MARKER.number))
        # update information in the marker collection
        MARKERS.update_marker(MARKER)
        # remove outdated observations
        MARKERS.clean_outdated_markers(MARKER_TIMEOUT)
        # remove the processed data from the buffer
        DATA = DATA[MARKER_RE_MATCH.end():]
        # look for the next marker in the buffer
        MARKER_RE_MATCH = re.search(MARKER_REGEX, DATA)

        # send something arbitrary to the Zigbee dongle. This has no real function except to demonstrate how to send something.
        #ZIGBEE.write(b'Hello')

    if len(DATA) > BUFFER_SIZE:
        # something is going wrong, flush garbage data
        DATA = ""
    # indicate that the markers are global
    global ORIGIN
    global ROBOTA
    global OB1
    global OB2
    global OB3
    global FINISH

    # find all markers
    ORIGIN = MARKERS.get_marker('origin')
    ROBOTA = MARKERS.get_marker('robotA')
    OB1 = MARKERS.get_marker('ob1')
    OB2 = MARKERS.get_marker('ob2')
    OB3 = MARKERS.get_marker('ob3')
    FINISH = MARKERS.get_marker('finish')

def distancetoorigin(name):
    if(not ORIGIN is None) and (not name is None):
        coordinates = name.relative_position(ORIGIN)
        distance = math.sqrt(math.pow(coordinates[0],2) + math.pow(coordinates[1],2))
        return distance

def angletoorigin(name):
    if(not ORIGIN is None) and (not name is None):
        coordinates = name.relative_position(ORIGIN)
        angle = math.atan2(coordinates[1], coordinates[0]) * 180 / math.pi
        return angle

def relativeangle(name1, name2):
    if(not ORIGIN is None) and (not name1 is None) and (not name2 is None):
        angle1 = name1.relative_angle(name2) * 180 / math.pi
        return angle1

def alignment_distance( ):
        C_robotA = ROBOTA.relative_position(ORIGIN)
        C_finish = FINISH.relative_position(ORIGIN)
        difference_vector[0] = C_finish[0] - C_robotA[0]
        difference_vector[1] = C_finish[1] - C_robotA[1]

        distance_difference_vector = math.sqrt(math.pow(difference_vector[0],2) + math.pow(difference_vector[1],2))
        return distance_difference_vector
        print('Distance of difference vector is', distance_difference_vector)
        print()
        print()

def alignment_angle( ):
        C_robotA = ROBOTA.relative_position(ORIGIN)
        C_finish = FINISH.relative_position(ORIGIN)
        difference_vector[0] = C_finish[0] - C_robotA[0]
        difference_vector[1] = C_finish[1] - C_robotA[1]

        angle_difference_vector = math.atan2(difference_vector[1], difference_vector[0]) * 180 / math.pi
        return angle_difference_vector
        print('Angle of difference vector is', angle_difference_vector)
        print()
        print()

def distance_object(obj):
        C_robotA = ROBOTA.relative_position(ORIGIN)
        C_object = obj.relative_position(ORIGIN)
        difference_vector[0] = C_object[0] - C_robotA[0]
        difference_vector[1] = C_object[1] - C_robotA[1]
        distance_difference_vector = math.sqrt(math.pow(difference_vector[0],2) + math.pow(difference_vector[1],2))
        return distance_difference_vector

def slope_object(obj):
        C_robotA = ROBOTA.relative_position(ORIGIN)
        C_object = obj.relative_position(ORIGIN)
        slope = (C_object[1] - C_robotA[1])/ (C_object[0] - C_robotA[0])
        perpendicular_slope = - slope
        return perpendicular_slope


arrived = False
temp = None
first_iteration = False
# loop forever
while (arrived == False):

    # read new data (if any) from the TCP connection
    try:
        DATA += LMSOCKET.recv(BUFFER_SIZE)
    except socket.error:
        # no data is available on the socket, sleep for 100ms
        sleep(0.1)
        # try again
        continue


    updatemarker()

    # Define empty vectors
    difference_vector = [None] * 3
    right_coordinates = [None] * 3
    left_coordinates = [None] * 3

    if (not ORIGIN is None) and (not FINISH is None):
        D_finish = distancetoorigin(FINISH)
        A_finish = angletoorigin(FINISH)
        AO_finish = relativeangle(FINISH, ORIGIN)


    if (not ORIGIN is None) and (not ROBOTA is None):
        D_robotA = distancetoorigin(ROBOTA)
        A_robotA = angletoorigin(ROBOTA)
        AO_robotA = relativeangle(ROBOTA, ORIGIN)


    if (not ORIGIN is None) and (not FINISH is None):
        if (temp == None):
            coordinates_finish = FINISH.relative_position(ORIGIN)
            temp = 1;
    '''
    if (not ORIGIN is None) and (not ROBOTA is None) and (not FINISH is None):
        angle_difference_vector = alignment_angle()
        distance_difference_vector = alignment_distance()
        #print('Relative angle between Origin and ROBOTA is ', AO_robotA)
        #print('Angle between RobotA and finish is ', angle_difference_vector)
        print('Distance between RobotA and finish is ', distance_difference_vector)
        if (abs(angle_difference_vector - AO_robotA) > 5):
            #while (abs(angle_difference_vector - AO_robotA) > 2):
                #angle_difference_vector = alignment_angle()

            if (angle_difference_vector - AO_robotA < 0):
                ZIGBEE.write(b'r')
                time.sleep(0.05)
                ZIGBEE.write(b's')

            elif (angle_difference_vector - AO_robotA > 0):
                ZIGBEE.write(b'l')
                time.sleep(0.05)
                ZIGBEE.write(b's')

        elif (distance_difference_vector > 12):
            ZIGBEE.write(b'f')
            time.sleep(0.05)

        elif(istance_difference_vector < 12):
            ZIGBEE.write(b's')
            arrived = True
            print('Arrived at destination')

        '''
    if (not ORIGIN is None) and (not ROBOTA is None) and (not FINISH is None):
        '''
        if (not OB1 is None) and (distance_object(OB1) <= 45): #within safety margin around object
            C_robotA = ROBOTA.relative_position(ORIGIN)
            C_finish = FINISH.relative_position(ORIGIN)

            print(distance_object(OB1))

            slope = slope_object(OB1)
            b = C_robotA[1] + slope * C_robotA[0] # determine new b coordinate
            dx1 = C_robotA[0] - (- b / slope)
            beta = math.atan2(C_robotA[1] ,dx1) * 180 / math.pi

            dx = math.sin(beta) * 15
            dy = math.cos(beta) * 15
            right_coordinates[0] = C_robotA[0] + dx
            right_coordinates[1] = C_robotA[1] + dy

            left_coordinates[0] = C_robotA[0] - dx
            left_coordinates[1] = C_robotA[1] - dy

            right_distance = math.sqrt(math.pow(C_finish[0] - right_coordinates[0],2) + math.pow(C_finish[1] - right_coordinates[1],2))
            left_distance = math.sqrt(math.pow(C_finish[0] - left_coordinates[0],2) + math.pow(C_finish[1] - left_coordinates[1],2))

            if (right_distance < left_distance):
                #ZIGBEE.write(b't') # send a t do tell the robot that has encountered an object
                print('Right')
                #ZIGBEE.write(b'r')
            else:
                #ZIGBEE.write(b't') # send a t do tell the robot that has encountered an object
                print('Left')
                #ZIGBEE.write(b'l')
            '''
        if True: ## when not within safety margin around object
            if (not ORIGIN is None) and (not ROBOTA is None) and (not FINISH is None):
                first_iteration = True
                angle_difference_vector = alignment_angle()
                distance_difference_vector = alignment_distance()
                #print('Relative angle between Origin and ROBOTA is ', AO_robotA)
                #print('Angle between RobotA and finish is ', angle_difference_vector)
                print('Distance between RobotA and finish is ', distance_difference_vector)
                if (abs(angle_difference_vector - AO_robotA) > 8):
                    #while (abs(angle_difference_vector - AO_robotA) > 2):
                    #angle_difference_vector = alignment_angle()
                    if (angle_difference_vector - AO_robotA < 0):
                        while (angle_difference_vector - AO_robotA < 0):
                            ZIGBEE.write(b'r')
                            updatemarker()
                            print(angle_difference_vector)
                            print(AO_robotA)
                            angle_difference_vector = alignment_angle()
                            AO_robotA = relativeangle(ROBOTA, ORIGIN)
                    elif (angle_difference_vector - AO_robotA > 0):
                        while (angle_difference_vector - AO_robotA > 0):
                            ZIGBEE.write(b'l')
                            updatemarker()
                            print(angle_difference_vector)
                            print(AO_robotA)
                            angle_difference_vector = alignment_angle()
                            AO_robotA = relativeangle(ROBOTA, ORIGIN)
                    ZIGBEE.write(b's')

                elif (distance_difference_vector > 12):
                    ZIGBEE.write(b'f')
                    time.sleep(0.05)

            elif (not ORIGIN is None) and (not ROBOTA is None) and (FINISH is None) and (first_iteration == True):
                ZIGBEE.write(b'f')
                time.sleep(2)
                ZIGBEE.write(b's')
                arrived = True
                print('Arrived at destination')

# close the socket (if we ever get here)
LMSOCKET.close()
