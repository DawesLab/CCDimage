#from arduinoshutter import sigOpen, sigClose
import serial
shutter = serial.Serial("/dev/ttyACM1")
def sigOpen():
    shutter.write(str.encode("b\n"))
    #print("Shutter Open")

def sigClose():
    shutter.write(str.encode("a\n"))
    #print("Shutter Closed")
