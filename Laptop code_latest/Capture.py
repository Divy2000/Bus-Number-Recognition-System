import cv2#Imports Open-CV
from threading import Thread#Imports Tread for running function in the background

frame = 0#Declares frame variable of frame to check if we get access to the carema in other codes

#Thread to run in background to capture the live feed
class myClassA(Thread):

    #Default initialization function of thread
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
    
    #Run function of thread which runs on calling the class
    def run(self):
        cap = cv2.VideoCapture(1)                   #Divice is set to capture the video (usb cam in our case) 
        print(cap)                                  #Prints the interface to check if we got connected to camera
        while cap.isOpened():                       #Infinite loop to show the read the frames from webcam and show the livefeed 
            global frame                            #Calls the global frame variable so frames are written on it
            _, frame = cap.read()                   #Reads the frame from the usb cam

#Function to get the current frame asynchronously. (to be called to pass the frame for detection)       
def get_f():
    while isinstance(frame,int):    #Checks if variable type is int we dont have access and continues to check
        pass
    return frame                    #Returns if we get have access and continues to check