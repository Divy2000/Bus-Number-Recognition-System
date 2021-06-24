# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 12:00:39 2021

@author: Divy
"""

import json
# import urllib
# from urlparse import urlparse
from urllib.parse import urlparse
import httplib2 as http #External library
# import Timestamp
import datetime
from pytz import timezone
key = None
#Date time pattern
pattern = "%Y-%m-%d %H:%M:%S"

#Authentication parameters
headers = { 'AccountKey' : '5myd8tu8QEedpYd4BB1sAg==',
'accept' : 'application/json'} #this is by default

def getBusDict(busStopNo):
    #API parameters
    uri = 'http://datamall2.mytransport.sg/' #Resource URL
    path = f'ltaodataservice/BusArrivalv2?BusStopCode={busStopNo}'
    #Build query string & specify type of API call
    target = urlparse(uri + path)
    # print(target.geturl())
    method = 'GET'
    body = ''
    #Get handle to http
    h = http.Http()
    #Obtain results
    response, content = h.request(
        target.geturl(),
        method,
        body,
        headers)
    #Parse JSON to print
    jsonObj = json.loads(content)
    # print json.dumps(jsonObj, sort_keys=True, indent=4))
    
    BusNum = {}
    keyList = []
    for each in jsonObj["Services"]:
        time = each["NextBus"]["EstimatedArrival"]
        # print(time)
        Busnum = each['ServiceNo']
        time = time.replace("+08:00","").replace("T"," ")
        date = datetime.datetime.strptime(time,pattern)
        now = datetime.datetime.now(timezone('Asia/Singapore'))
        now = now.replace(tzinfo=None)
        # print(now)
        t = date - now
        key = int(t.total_seconds())
        BusNum[key] = Busnum
        keyList.append(key)
    return BusNum, keyList

# while True:
#     BusNum, keyList = getBusDict()
#     print(BusNum)

def getCurrentBus(busStopNo):
    BusNum, keyList = getBusDict(busStopNo)
    print(BusNum)
    currentBus = []
    for e in keyList:
        if e<=5 and e>-7:
            currentBus.append(BusNum[e])
    return currentBus

def getArrivingBus(busStopNo):
    BusNum, keyList = getBusDict(busStopNo)
    arrivingBus = []
    for e in keyList:
        if e<20 and e>10:
            arrivingBus.append(BusNum[e])
    return arrivingBus