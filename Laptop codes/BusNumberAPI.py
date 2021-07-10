import json                         #Imports library to parse the json data and make a dictionary
from urllib.parse import urlparse   #Parses the URL
import httplib2 as http             #This sends the http request to get the data
import datetime                     #It is used to manipulate te date time data from the Singapore server to get the remaining time of bus(in seconds)
from pytz import timezone           #This is used to set the singapore timezone

pattern = "%Y-%m-%d %H:%M:%S"       #Date time pattern for manipulation of data from bus time API

#Authentication parameters
headers = { 'AccountKey' : '5myd8tu8QEedpYd4BB1sAg==', #Acconut key is to be issued from https://datamall.lta.gov.sg/
'accept' : 'application/json'}      #this is by default

#This is function call the API to get BusNumber and time left(in seconds).
def getBusDict(busStopNo):
    #API parameters
    uri = 'http://datamall2.mytransport.sg/'                        #Resource URL
    path = f'ltaodataservice/BusArrivalv2?BusStopCode={busStopNo}'  #Path to API
    #Build query string & specify type of API call
    target = urlparse(uri + path)                                   #Sets target URL
    method = 'GET'                                                  #Defines GET method
    body = ''
    h = http.Http()                                                 #Get handle to http
    response, content = h.request(                                  #Obtain results
        target.geturl(),
        method,
        body,
        headers)

    jsonObj = json.loads(content)                                   #Parse JSON to get a dictionary
    
    #Declares empty dictionary of busNumbers to store the data
    BusNum = {}
    keyList = []

    #Organizes the data from the server to give us the list
    for each in jsonObj["Services"]:                               #Iterates through the dictionaries of bus and timestamp
        time = each["NextBus"]["EstimatedArrival"]                 #Gets ETA of the next bus
        Busnum = each['ServiceNo']                                 #Gets the bus number of the same
        time = time.replace("+08:00","").replace("T"," ")          #Manipulates the time string for further manipulation
        date = datetime.datetime.strptime(time,pattern)            #Converts the datetime string to datetime
        now = datetime.datetime.now(timezone('Asia/Singapore'))    #Gets currnt siganpore standard time
        now = now.replace(tzinfo=None)                             #Removes timezone info from it for further manipulation
        t = date - now                                             #Gets remaining time for the arrival of the bus
        key = int(t.total_seconds())                               #Extracts the number of seconds from the time variable to use it as a key to the dictionary
        BusNum[key] = Busnum                                       #Assign the bus number as value to the corresponding key(or number of seconds to arrival)
        keyList.append(key)                                        #Appends the key to the keylist
    return BusNum, keyList                                         #Returns both dictionary(of bus number and time left) and keys of the dictionary


#Get current bus number by getting current time from the API
def getCurrentBus(busStopNo):
    BusNum, keyList = getBusDict(busStopNo)    #Calls the function to get bus number and time remainig
    currentBus = []                            #List of current bus numbers to be populated 
    boolean = False                            #Boolean to check the return values
    for e in keyList:                          #Iterates the list to get current bus numbers
        if e==5:                               #checks if the bus is there or not
            currentBus.append(BusNum[e])       #Appends the list if bus is there according to API timings
            boolean = True                     #Sets boolean to True to return the list of current bus number alongwith the latest bus number
    if boolean:                                #Checks the boolean for value to return
        return currentBus, BusNum              #Returns the current bus numbers
    else:
        return None, None                      #Returns None values if there is no bus currently there


#Get arriving bus number by getting current time from the API
def getArrivingBus(busStopNo):
    BusNum, keyList = getBusDict(busStopNo)    #Calls the function to get bus number and time remainig
    arrivingBus = []                           #List of arriving bus numbers to be populated 
    boolean = False                            #Boolean to check the return values
    for e in keyList:                          #Iterates the list to get arriving bus numbers
        if e==20:                              #checks if the bus is arriving or not
            arrivingBus.append(BusNum[e])      #Appends the list if bus is there according to API timings
            boolean = True                     #Sets boolean to True to return the list of current bus number alongwith the latest bus number
    if boolean:                                #Checks the boolean for value to return
        return arrivingBus, BusNum             #Returns the arriving bus numbers
    else:
        return None, None                      #Returns None values if there is no bus arriving soon there
