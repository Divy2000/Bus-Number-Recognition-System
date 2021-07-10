from threading import Thread                              #Imports Tread for running function in the background

from BusNumberAPI import getArrivingBus, getCurrentBus    #Functions to get arriving and current bus numbers respectively
from Getnum import startextracting                        #Function to detect number from the frame

busStopNo = int(input("Enter Bus station number:"))       #Takes bus stop number as input from user

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
                print(f"bus number {e} is arriving soon")   #Speaks arriving bus number to earphones


#Returns number detected from the frame and rpint the check of truth value by comparing to the orignal number
def getNum(frame):
    num = startextracting(frame)                                #Number is detected from the frame
    correct, _num, d = checkCurrentNum(num,busStopNo)           #Checks the detected bus number is correct or not
    print(f"Predicted - {num} Orignal - {_num} - {correct}")    #Prints the predicted, orignal and correctness of bus number for validation
    return num                                                  #Returns the detected number


#Method to get bus stop number in main.py to pass in various functions
def getBno():
    return busStopNo    #Returns the bus stop number
