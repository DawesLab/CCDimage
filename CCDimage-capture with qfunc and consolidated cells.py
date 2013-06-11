# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# ## Collect data from Pylon CCD

# <markdowncell>

# Must be run from the MM directory in order to find relevant libraries and config files.

# <codecell>

cd "c:\\Program Files\Micro-Manager-1.4\"

# <codecell>

#Load necessary libraries
import MMCorePy
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy import stats
from collections import Counter 
from numpy.fft import fft,fftshift
from numpy import real, imag, abs
import sys
sys.path.append('C:\Documents and Settings\All Users\Documents\PylonCCD')
import Qfunction

Qfunc = Qfunction


#Initialize camera connection
mmc = MMCorePy.CMMCore()
mmc.loadDevice("ccd","PrincetonInstruments","Camera-1")
mmc.initializeDevice("ccd")
mmc.setProperty("ccd","ShutterMode","Open Shutter Pre-Exposure")
xdim = 1340 #x-dimension of ccd
ydim = 400 #y-dimension of ccd

# <codecell>

print mmc.getProperty("ccd", "CCDTemperature")
print mmc.getProperty("ccd", "CCDTemperatureSetPoint")

# <codecell>

#Set user parameters
frames = 10 #number of frames taken
mmc.setExposure(30) #in ms

#---------------------------------------------------------------

#Automated capture process
im = []
for f in range (0, frames):
    
    mmc.snapImage()
    im.append(mmc.getImage())

#Display one of the captured images
imshow(im[0],cmap = cm.gray)

# <codecell>

qbin = 10

#Data analysis and index plots
maxIndex = np.zeros(frames)

#Create list of indices of maximum magnitude
fftComplex = []

for f in range (0, frames):
    fftComplex.append(fftshift(fft(im[f][ydim//2,:])))
    max = 0
    
    for x in range(0,int(round(xdim*0.45))):
        if abs(fftComplex[f][x]) > max:
            max = abs(fftComplex[f][x])
            maxIndex[f] = x


#Find statistical information to choose appropriate index
fftIndexAverage = np.mean(maxIndex)
fftIndexStd = np.std(maxIndex)
fftIndexMode = stats.mode(maxIndex)[0][0]

#Create histogram of maximum indices in each shot
pylab.hist(maxIndex, bins=100, normed=1)
plt.xlim(fftIndexAverage - 5*fftIndexStd - 1, fftIndexAverage + 5*fftIndexStd + 1)
pylab.show()

#Show most common maximum index and the fft plot of one shot
print fftIndexMode
plot(log(fftshift(abs(fft(im[0][ydim//2,:])))))


#Complex phase plot
#Save complex fft maxima of shots as an array
output = []

for shot in fftComplex:
    output.append(shot[fftIndexMode])
    
qfig = Qfunc.qfuncimage(output,qbin,0)

# <codecell>

#Manual index override

output = []

for shot in fftComplex:
    output.append(shot[487])
    
qfig = Qfunc.qfuncimage(output,qbin,0)

# <codecell>

#Plot complex phase angle over run
import PhaseAnglePlot

phasePlot(output)

print output

pass

# <codecell>

#Save data as .png of qfunc and .npy of array of complex max values of fft's

#If folder for today doesn't exist, create it; else navigate to appropriate folder
target_folder = datetime.datetime.now().strftime("%m-%d-%Y")
if not os.path.exists("C:\\Documents and Settings\photon\My Documents\Google Drive\DawesLab\\" + target_folder):
    os.makedirs("C:\\Documents and Settings\photon\My Documents\Google Drive\DawesLab\\" + target_folder)
os.chdir("C:\\Documents and Settings\photon\My Documents\Google Drive\DawesLab\\" + target_folder)


filename = datetime.datetime.now().strftime("%H-%M-%S")# based on time and date
qfig.savefig(filename)
np.save(filename, output)

print filename

# <codecell>

print matplotlib.__version__
print numpy.__version__
#print scipy.__version__

# <codecell>


# <codecell>


# <markdowncell>

# ## Run this to close camera device:

# <codecell>

mmc.unloadDevice("ccd")

# <codecell>


