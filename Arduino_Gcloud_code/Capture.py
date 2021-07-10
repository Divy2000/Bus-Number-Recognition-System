import cv2                      #Imports Open-CV 
from threading import Thread    #Imports Tread for running function in the background

frame = 0                       #Declares frame variable of frame to check if we get access to the carema in other codes

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
            cv2.imshow("frame",frame)               #Show the live feed in a window named "frame"
            if cv2.waitKey(1) & 0xFF == ord('q'):   #Check to exit the loop if we press "q" key on the keyboard
                break                               #Break statment to stop the loop

#Function to get the current frame asynchronously. (to be called to pass the frame for detection)
def get_f():
    return frame    #Returns the frame

myClassA()  #Calls the thread to start the capture from the live feed
