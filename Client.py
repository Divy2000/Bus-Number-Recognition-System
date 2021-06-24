# -*- coding: utf-8 -*-
"""
Created on Tue Jun 24 14:13:47 2021

@author: divyp
"""
import requests
import io
import numpy as np
from Capture import get_f
from BusNumberAPI import getArrivingBus, getCurrentBus
from espeak import espeak
from threading import Thread
# import os
#os.chdir("D:\Divy\Compan")

url = 'http://104.198.159.164:8080/extractinfo'
busStopNo = 44221
def compress(image):
    buf = io.BytesIO() #create our buffer
    #pass the buffer as you would an open file object
    np.savez_compressed(buf, a = image)
    buf.seek(0)
    return buf

class BusArriveSpeak(Thread):
    def __init__(self, busStopNo):
        Thread.__init__(self)
        self.daemon = True
        self.busStopNo = busStopNo
        self.start()
    def run(self):
        num = ""
        while True:
            l = getArrivingBus(busStopNo)
            for e in l:
                if num != e:
                    num = e
                    espeak.synth(f"Bus Number {e} is arriving.")
                    print(f"Bus Number {e} is arriving.")
                    #pass
                    
                
def checkCurrentNum(num,busStopNo):
    l = getCurrentBus(busStopNo)
    if len(l)>0:
        boolean = False
        for e in l:
            try:
                e = int(e)
            except:
                e = int(e[:-1])
       
            if e == num:
                boolean = True
                break
        return boolean, e
    return None, None


def detect():
    frame = 0
    while isinstance(frame,int):
        frame = get_f()
    buf = compress(frame)
    print("compressed")
    r = requests.post(url, data=buf)
    num = r.json()["busNo"]
    # num = 123
    correct, orignal_num = checkCurrentNum(num,busStopNo)
    print(f"Predicted - {num} Orignal - {orignal_num} - {correct}")
    espeak.synth(num)
BusArriveSpeak(busStopNo)
    
while True:
    detect()