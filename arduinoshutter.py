#from arduinoshutter import sigOpen, sigClose
import serial
shutter = serial.Serial("/dev/ttyACM0")
def sigOpen():
    shutter.write("b\n")
    #print("Shutter Open")

def sigClose():
    shutter.write("a\n")
    #print("Shutter Closed")
