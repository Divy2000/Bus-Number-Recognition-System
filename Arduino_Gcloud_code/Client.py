import requests                 #Library to post request to Flask API on google cloud to detect number
import io                       #This helps to create a buffer to compress the frame before sending
import numpy as np              #Numpy library to save the frame in compressed format before sending
from espeak import espeak       #Library to get audio output from raspberryPi
from threading import Thread    #Imports Tread for running function in the background

from Capture import get_f                               #Function to get current frame from the webcan feed call Capture.py to start the webcam feed
from BusNumberAPI import getArrivingBus, getCurrentBus  #Functions to get arriving and current bus numbers respectively


url = 'http://104.197.35.208:8080/extractinfo'      #URL of API deployed in the google cloud in format 'http://<External_IP>:8080/extractinfo'
busStopNo = int(input("Enter Bus Stop Number: "))   #Takes bus stop number as input from user


#Function to compress the frame before sending to cloud to reduce the latency
def compress(image):
    buf = io.BytesIO()                     #create our buffer
    np.savez_compressed(buf, a = image)    #compresses the buffer as image
    buf.seek(0)                            #Sets the buffer pointer back to 0 to read the frame when function is called again
    return buf                             #Returns the buffer


#Checks the number given to the current bus number for a given Bus Stop
def checkCurrentNum(num,busStopNo):
        l, d = getCurrentBus(busStopNo)    #Function to get current bus numbers called from BusNumberAPI.py
        if l == None and d == None:        #Checks if the return values is none(True means no bus is there)
            return None, None, d           #Returns None values if there is no bus currently at the Bus Stop
        if len(l)>0:                       #Checks if the number of busses at bus stop is more than 0
            boolean = False                #Boolean to check if the detected number os true or not
            for e in l:                    #Iterates through list of numbers of the busses at the bus stop
                try:
                    e = int(e)             #Tries to convert the bus number to the string (works in case of 807, 901, etc.)
                except:
                    e = int(e[:-1])        #If it fails mmeans it should be anding with character(like 811T) do it removes the "T" and converts to integer
                if e == num:               #Checks if the number detected is same as the bus present there according to the API
                    boolean = True         #Sets boolean to True if that's the case
                    break                  #Breaks the loop
            return boolean, l, d           #Returns the values of there are buses at the bus stop
        return None, None, d               #Or else returns None value


#Thread to run in background to speak the correct bus number present there for validation
class BusNoSpeak(Thread):

    #Default initialization function of thread but this one takes Bus Stop Number as input
    def __init__(self, busStopNo):
        Thread.__init__(self)
        self.daemon = True
        self.busStopNo = busStopNo
        self.start()

    #Run function of the thread
    def run(self):
        nume = 0                                                   #Sets initial value of external number variable to 0
        de = None                                                  #Sets initial value of external dictionary variable to None
        while True:                                                #Infinite loop to speak to corrected bus number(from API)
            correct, _num, d = checkCurrentNum(123,busStopNo)      #Returns current bus number
            #Checks if the following operation is done only once for a bus
            if (_num != None and nume != _num) or (nume == _num and _num!=None and de != d):
               nume = _num                                         #Sets external number list to current ones for checks
               de = d                                              #Sets external {num: time} dictionary to current ones for checks
               for e in _num:                                      #Itherates through the list 
                    espeak.synth(f"corected bus number {_num}")    #Prints current bus number to console
                    print(f"corrected bus number {e}")             #Speaks current bus number to earphones


#Thread to run in background to speak the arriving bus numbers
class BusArriveSpeak(Thread):

    #Default initialization function of thread but this one takes Bus Stop Number as input
    def __init__(self, busStopNo):
        Thread.__init__(self)
        self.daemon = True
        self.busStopNo = busStopNo
        self.start()

    #Run function of the thread
    def run(self):
        le = None                                           #Sets initial value of external list variable to None
        de = None                                           #Sets initial value of external dictionary variable to None
        while True:                                         #Infinite loop to speak to arriving bus number(from API)
            l, d = getArrivingBus(busStopNo)                #Returns arriving bus number
            #Checks if the following operation is done only once for a bus
            if (le == l and de == d) or (l==None and d==None):
                continue                                    #Skips the following statments if the condition satisfies(i.e., operation is repeated)
            le = l                                          #Sets external number list to arriving ones for checks
            de = d                                          #Sets external {num: time} dictionary to arriving ones for checks
            for e in l:                                     #Itherates through the list 
                espeak.synth(f"bus number {e} is approaching in a few second")  #Prints arriving bus number to console
                print(f"bus number {e} is arriving soon")   #Speaks arriving bus number to earphones


#Main driver function at client side to detect and verify the bus number taking Bus Stop Number as input
def detect(busStopNo):
    BusArriveSpeak(busStopNo)                                           #Calls the Bus arrival speaking thread  
    BusNoSpeak(busStopNo)                                               #Calls the current Bus sopeaking thread
    nume = 0                                                            #Sets the external bus number to 0
    while True:                                                         #Infinite loop to get frames and detect the number
        frame = 0                                                       #Declares frame variable of frame to check if we get access to the carema in other codes
        while isinstance(frame,int):                                    #Checks if variable type is int we dont have access and continues to check
            frame = get_f()                                             #Get the value of global frame variable from Capture.py
        #Out of loop when there is a frame captures from the usb cam
        buf = compress(frame)                                           #Compresses the frame to send to the Flask API in cloud for processing
        r = requests.post(url, data=buf)                                #Request sent to the Flask API and returns detected number as json format
        num = r.json()["busNo"]                                         #The number is extracted from json by converting it to dictionary and passing the key
        try:
            num = int(num)                                              #Tries to convert to integer
            if num == "":                                               #If its blank then next statments aren't executed and goes to next iteration
                continue
        except:                                                         #If it is not converted to int means its not a proper string therefore next statments aren't executed and goes to next iteration
            continue
        if num!=855 or num!=nume:                                       #Checks if the following operation is done only once for a bus
            nume = num                                                  #Sets external bus number to current ones for the checking purpose
            print(f"detected bus number is {num}")                      #Prints the detected bus number
            espeak.synth(f"detected bus number is {num}")               #Speaks the detected bus number through the earphones
        correct, _num, d = checkCurrentNum(num,busStopNo)               #Checks the detected bus number is correct or not
        if nume == _num or _num == None:                                #Checks if the following operation is done only once for a bus
            continue
        else:
            nume = _num                                                 #Sets external bus number to current ones for the checking purpose
            print(f"Predicted - {num} Orignal - {_num} - {correct}")    #Prints the predicted, orignal and correctness of bus number for validation
    

detect(busStopNo) #Calls the main function to start the detection