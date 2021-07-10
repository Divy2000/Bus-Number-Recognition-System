import os                                    #imports os to change the enviornment variable to run multipule threads simultaneously
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"    #Changing enviornment variable to run multiple threads simultaneously
import cv2                                   #Open-CV to show the live usb feed and print the number on it when detected
from threading import Thread                 #Imports Tread for running function in the background

from Client import getNum    #Function to get number from the image frame
from Client import getBno    #Function to get bus stop number from Client.py
from Capture import get_f    #Function to get current frame from te usb cam 

from Client import BusNoSpeak       #Thread to speak bus number from API
from Client import BusArriveSpeak   #Thread to speak alert about arrival of the bus
from Capture import myClassA        #Thread to start the usb cam feed

gnum = 0                #Declaring global Number to 0
gboolean = True         #Declaring global boolean to True
busStopNum = getBno()   #Function to get bus stop number


#Thread to detect the bus number and change the gboolean false when output is arrived
class GetNum(Thread):

    #Default initialization function of thread
    def __init__(self, busStopNo):
        Thread.__init__(self)
        self.daemon = True
        self.busStopNo = busStopNo
        self.start()

    #Run function of the thread
    def run(self):
        global gboolean, gnum       #Global variables are called to manipulate  
        while True:                 #Infinite while loop to get frame and detect number
            framed = get_f()        #Gets current frame from usb cam
            gnum = getNum(framed)   #Dectects number from the frame and stores in gnum
            gboolean = False        #Set gboolean to False so that function knows that computation is done


#Main function to call all threads and show the live cam feed with overllay if the number is detected
def show():
    global gboolean, gnum       #Global variables are called to manipulate  
    myClassA()#Thread to start the usb cam and get frames from it continuously
    BusNoSpeak(busStopNum)#Thread to print current bus number from API
    BusArriveSpeak(busStopNum)#Thread to print arriving bus number from API
    GetNum(busStopNum)#Thread to strat detection of bus number from webcam

    while True:#Infininte loop to show the live feed
        if gboolean and (gnum=="" or gnum==0):      #Checks if any number is not detected(False if there is a number)
            frame = get_f()                         #Gets the frame of the usb cam
            cv2.imshow("frame",frame)               #Show the live feed in a window named "frame"
            if cv2.waitKey(1) & 0xFF == ord('q'):   #Check to exit the loop if we press "q" key on the keyboard
                break                               #Break statment to stop the loop
        else:                                       #if the number is detected
            frame1 = get_f().copy()                 #make a copy of current frame
            #Draws or put the detected number on the current frame
            cv2.putText(frame1, gnum, (50,100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 2)
            gboolean = True                         #Sets global boolean to True so if condition satisfies till next detection
            cv2.imshow("frame",frame1)              #Show the live feed in a window named "frame" with overlay of the detected number
            if cv2.waitKey(1) & 0xFF == ord('q'):   #Check to exit the loop if we press "q" key on the keyboard
                break                               #Break statment to stop the loop
    cv2.destroyAllWindows()                         #Closes the window "frame"

show()   #Calls the show function to start the detection from laptopS
