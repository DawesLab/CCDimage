#from cloudchamber import airbrush_on, airbrush_off
import serial

WAIT= 4;
AIRBRUSH_ON = 5;
AIRBRUSH_OFF = 6;

cloudcontroller = serial.Serial("/dev/ttyUSB1")
def airbrush_on():
    cloudcontroller.write(bytes([AIRBRUSH_ON]))
    #print("Airbrush On")

def airbrush_off():
    cloudcontroller.write(bytes([AIRBRUSH_OFF]))
    #print("Airbrush Off")
