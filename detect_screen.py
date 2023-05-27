from pyzbar.pyzbar import decode, ZBarSymbol
from PIL import Image
import os
import os.path
import mss
import time
import requests
import re

#PRINT SCREEN
def on_exists(fname):
    if os.path.isfile(fname):
        os.remove(fname)
def prtsc():
    with mss.mss() as sct:
        filename = sct.shot(output="mon-{mon}.png", callback=on_exists)

#READ QR
temp = ""
shown = False
def readqr():
    global temp
    global shown
    try:
        img = Image.open('mon-1.png')
        targetCodeType = [ZBarSymbol.QRCODE]
        result = decode(img,symbols=targetCodeType)[0].data
        text = result.decode('utf-8')
        if(text!=temp):
            temp = text
            shown = False
            print("QR Code Detected:",text,"  Taking Attendance...")
            send_otp(text)
        else:
            if not shown:
                shown = True
                print("HIBERNATE until new QR Code found...")
    except Exception as e:
        #print(str(e))
        pass

#SEND OTP
def send_otp(text):
    if(re.search("^\d{3}$", text)):
            #put your server link here
            url = 'https://sleepyattendix.josephlow5.repl.co/post/otp'
            myobj = {'otp': text}
            x = requests.post(url, data = myobj)
            response = x.text.replace('<script>alert("','').replace('");window.location.replace("https://SleepyAttendix.josephlow5.repl.co/");</script>','')
            print("\tRequest submitted:",text,"  Result:",response,"\n")
    else:
        print("\tInvalid OTP detected. Returning...")


starttime = time.time()
interval = 10.0
print("\t============================")
print("\t\tQR Attendance")
print("\t============================")
print("Starting repeater with interval of {} seconds".format(interval))
print("Please note that your screen 1 will be continuously captured\n\n")
while True:
    prtsc();
    readqr();
    time.sleep(interval - ((time.time() - starttime) % interval))


