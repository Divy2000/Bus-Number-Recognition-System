import easyocr
import re
import cv2
from flask import Flask, jsonify, request
import numpy as np
import io

app = Flask(__name__)
reader = easyocr.Reader(['en'])

def startextracting(img):
    bus_no = ''
    result = reader.readtext(img, detail = 0)
    for line in result:
        match = re.search(r'[ob\d][ob\d][ob\d]', line.lower())
        if str(type(match)) != '<class \'NoneType\'>':
            bus_no = list(match.group())
            if bus_no[0]=='0':
                bus_no[0]='8'
            for i in range(0,3):
                if bus_no[i]=='b':
                    bus_no[i]='8'
                if bus_no[i]=='o':
                    bus_no[i]='0'
            break
    bus_n = str(''.join(bus_no))
    return bus_n

@app.route('/extractinfo', methods=['POST'])
def extractinfo():
    r = request
    print("recieved")
    load_bytes = io.BytesIO(r.data)
    img = np.load(load_bytes)['a']
    print("loaded")
    # print(nparr.shape)
    busno = startextracting(img)
    result = {'busNo': busno}
    return jsonify(result)
    # return str(nparr.shape)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080 , debug=True)
    # app.run(debug=True)