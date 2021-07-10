import easyocr    #EasyOCR library is used to detect the text from the image
import re         #RegEx library to manipulate the text from the easyOCR to extract the number

reader = easyocr.Reader(['en'])    #Declares easy-ocr reader for Eglish


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
