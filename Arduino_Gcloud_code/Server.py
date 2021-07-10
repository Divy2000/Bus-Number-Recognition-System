import easyocr                              #EasyOCR library is used to detect the text from the image
import re                                   #RegEx library to manipulate the text from the easyOCR to extract the number
from flask import Flask                     #Flask to create a Flask API to use this as a cloud service
from flask import request                   #request gets the request varibale when this API is called
from flask import jsonify                   #jsonify parse the dictionary to a json format to send it back as response
import numpy as np                          #Numpy to uncompress to arriving data buffer as image frame
import io                                   #io to read the recieved data buffer

app = Flask(__name__)                       #Declares a Flask APP
reader = easyocr.Reader(['en'])             #Declares easy-ocr reader for Eglish


#Function to extract bus number from the frame
def startextracting(img):
    bus_no = ''                                                 #inintial value of bus number set to empty string
    result = reader.readtext(img, detail = 0)                   #Text result from easyocr reader
    for line in result:                                         #Iterates through each line of the result variable
        match = re.search(r'[ob\d][ob\d][ob\d]', line.lower())  #searches for three consecutive numbers
        if str(type(match)) != '<class \'NoneType\'>':          #Checks if the detected type is not None
            bus_no = list(match.group())                        #converts the detected list of numbers to list to handle general inconsistensies
            if bus_no[0]=='0':                                  #If "0" is detected as 1st digit, it is converted to "8" as it is false detection of 8 as 0
                bus_no[0]='8'
            for i in range(0,3):
                if bus_no[i]=='b':                              #If "b" is detected as 1st to 3rd digit, it is converted to "8" as it is false detection of 8 as 0
                    bus_no[i]='8'
                if bus_no[i]=='o':                              #If "o" is detected as 1st to 3rd digit, it is converted to "0" as it is false detection of 8 as 0
                    bus_no[i]='0'
            break
    bus_n = str(''.join(bus_no))                                #Converts the list of 3 numbers to one string to make a final bus number
    return bus_n                                                #Returns the bus number if detected or else empty string is returned in this variable

#Sets the route to url/extractinfo with post method to call the following function as API service
@app.route('/extractinfo', methods=['POST'])
def extractinfo():                     #Function to get and process the request to return the output
    r = request                        #request stored in a variable to proesess
    print("recieved")                  #Confirmation of request is recieved
    load_bytes = io.BytesIO(r.data)    #Reading the bytes and storing it to buffer
    img = np.load(load_bytes)['a']     #loading the frame image from the compressed bytes
    print("loaded")                    #Confirmation of decompressing or loading of the image
    busno = startextracting(img)       #Calling function to extract the busnumber from the image
    result = {'busNo': busno}          #Making a dictionary to send the response in json format
    return jsonify(result)             #Returning the dictionary as json

#Main function to start the service on the cloud
if __name__ == "__main__":
    #Starts the Flask APP at localhost at port:8080 so that we can port forward the local IP to external IP to get access anywhere in the world
    app.run(host='0.0.0.0', port=8080 , debug=True)