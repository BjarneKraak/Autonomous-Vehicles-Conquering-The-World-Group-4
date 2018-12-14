""" Client to connect to a locatemarkers program to receive the marker data, do some computation on that data and show how to communicate on the Zigbee connection.
"""
import math # IMPORT MATH PACKAGE
import time # IMPORT TIME PACKAGE
import socket
import re
from time import sleep

from marker import Marker, MarkerCollection, MARKER_REGEX
from zigbee import Zigbee

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
DATA = b""

# loop forever
while True:

    # read new data (if any) from the TCP connection
    try:
        DATA += LMSOCKET.recv(BUFFER_SIZE)
    except socket.error:
        # no data is available on the socket, sleep for 100ms
        sleep(0.1)
        # try again
        continue

    # check the data against the marker regular expression to check if there is complete marker information in the received data
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
        ZIGBEE.write(b'Hello')


    if len(DATA) > BUFFER_SIZE:
        # something is going wrong, flush garbage data
        DATA = ""

    # use the results to get the position and orientation of one marker (robot) relative to another marker (origin)

    ORIGIN = MARKERS.get_marker('origin')
    ROBOTA = MARKERS.get_marker('robotA')
    OB1 = MARKERS.get_marker('ob1')
    OB2 = MARKERS.get_marker('ob2')
    OB3 = MARKERS.get_marker('ob3')
    FINISH = MARKERS.get_marker('finish')
    
    
    # if both are present
    if (not ORIGIN is None) and (not OB1 is None): ## distance between Origin and Object 1
        # compute and print the relative position
        coordinates_OB1 = OB1.relative_position(ORIGIN)
        D_OB1 = math.sqrt(math.pow(coordinates_OB1[0],2) + math.pow(coordinates_OB1[1],2))
        print('Distance between Origin and object 1 is {0:.2f}', D_OB1)
        # compute and print the relative orientation
        OA_OB1 = OB1.relative_angle(ORIGIN) * 180 / math.pi

        # Angle between Robot and object 1
        A_OB1 = math.atan2(coordinates_OB1[1], coordinates_OB1[0]) * 180 / math.pi
        print('Angle between Origin and obtject 1 is {0:.2f}', A_OB1)
        
    if (not ORIGIN is None) and (not OB2 is None): ## distance between Origin and Object 1
        # compute and print the relative position
        coordinates_OB2 = OB2.relative_position(ORIGIN)
        D_OB2 = math.sqrt(math.pow(coordinates_OB2[0],2) + math.pow(coordinates_OB2[1],2))
        print('Distance between Origin and object 2 is =', D_OB2)
        # compute and print the relative orientation
        OA_OB2 = OB2.relative_angle(ORIGIN) * 180 / math.pi
        
        # Angle between Robot and object 2
        A_OB2 = math.atan2(coordinates_OB2[1], coordinates_OB2[0]) * 180 / math.pi
        print('Angle between Origin and obtject 2 is =', A_OB2)
        
    if (not ORIGIN is None) and (not OB3 is None): ## distance between Origin and Object 1
        # compute and print the relative position
        coordinates_OB3 = OB3.relative_position(ORIGIN)
        D_OB3 = math.sqrt(math.pow(coordinates_OB3[0],2) + math.pow(coordinates_OB3[1],2))
        print('Distance between Origin and object 3 is =', D_OB3)
        # compute and print the relative orientation
        OA_OB3 = OB3.relative_angle(ORIGIN) * 180 / math.pi
        
        # Angle between Robot and object 3
        A_OB3 = math.atan2(coordinates_OB3[1], coordinates_OB3[0]) * 180 / math.pi
        print('Angle between Origin and obtject 3 is =', A_OB3)


    if (not ORIGIN is None) and (not FINISH is None): ## distance between Origin and Object 1
        # compute and print the relative position
        coordinates_FINISH = FINISH.relative_position(ORIGIN)
        D_FINISH = math.sqrt(math.pow(coordinates_FINISH[0],2) + math.pow(coordinates_FINISH[1],2))
        print('Distance between Origin and finish is =', D_FINISH)
        # compute and print the relative orientation
        OA_FINISH = FINISH.relative_angle(ORIGIN) * 180 / math.pi

        # Angle between Robot and Finish
        A_FINISH = math.atan2(coordinates_FINISH[1], coordinates_FINISH[0]) * 180 / math.pi
        print('Angle between Origin and finish is =', A_FINISH)
        
    if (not ORIGIN is None) and (not ROBOTA is None): ## distance between Origin and Object 1
        # compute and print the relative position
        coordinates_ROBOTA = ROBOTA.relative_position(ORIGIN)
        D_ROBOTA = math.sqrt(math.pow(coordinates_ROBOTA[0],2) + math.pow(coordinates_ROBOTA[1],2))
        print('Distance between Origin and ROBOTA is =', D_ROBOTA)
        # compute and print the relative orientation
        OA_ROBOTA = ROBOTA.relative_angle(ORIGIN) * 180 / math.pi

        # Angle between Robot and Finish
        A_ROBOTA = math.atan2(coordinates_ROBOTA[1], coordinates_ROBOTA[0]) * 180 / math.pi
        print('Angle between Origin and ROBOTA is =', A_ROBOTA)

        

    time.sleep(2)        
# close the socket (if we ever get here)
LMSOCKET.close()






