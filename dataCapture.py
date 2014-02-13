
##************************************************##
##                                                ##
## This file helps in automation of data capture  ##
##                                                ##
##************************************************##

import numpy as np
import pylab
import os
import zmq
from scipy import stats
from collections import Counter 
from numpy.fft import fft,fftshift
from numpy import real, imag, abs, frombuffer
import sys
import datetime
sys.path.append('/home/photon/code/PylonCCD')
import Qfunction as Qfunc

class Capture():
	# Import python packages and initialize data server
	def __init__(self):

		print "Changing settings...."
		pylab.rcParams['figure.figsize'] = (12.0, 6.0)

		print "Initializing variables...."
		self.REQUEST_TIMEOUT = 25000
		self.SERVER_ENDPOINT = "tcp://localhost:5555"

		context = zmq.Context()

		self.background = np.array([[[]]]) # Background reference image in an np array
		self.output = [] # Contains analyzed data
		self.dataOut = np.array([[[]]]) # Save location for takeData()
		self.peak_mode = 0 # The peak mode of the data set
		self.qfig = 0 # Will be made into a graph

		#  Socket to talk to server
		print "Connecting to array server..."
		self.client = context.socket(zmq.REQ)
		self.client.connect(self.SERVER_ENDPOINT)

		self.poll = zmq.Poller()
		self.poll.register(self.client, zmq.POLLIN)
		print "Ready!"


	# Averages N shots of background and sets to background variable
	def takeBackground(self, N = 5): # default number of shots to average is 5
		self.request_images(N)
		images = self.open_images()
		self.background = np.mean(images, 2)


	# Clears all analysis data
	def clearData(self):
		self.output = []


	#Finds the peak mode of the data set taken by takeData()
	def findPeakMode(self):
		print "This function has not yet been implemented."
		# TODO: import mode_strength_plot to find mode. Set strongest mode to self.peak_mode


	# Makes a histogram figure
	def makeQfig(self, mode = None): #makes a Qfig for a specified mode
		if mode == None:
			mode = self.peak_mode
		mode_array = self.dataOut[mode,:,:].flatten() #takes only the desired mode
		self.qfig = Qfunc.qfuncimage(mode_array,30,0)


	# Saves Qfig as a .png file in the default directory or wherever specified
	def saveQfig(self, root_path = "/home/photon/data/"):
	    """
	    Save Qfig data as .png of qfunc and .npy of array of complex max values of fft's
	    Creates a folder with today's date: 01-13-2014
	    If folder for today doesn't exist, create it; else navigate to appropriate folder
	    """

	    if self.qfig != 0:
		    target_folder = datetime.datetime.now().strftime("%m-%d-%Y")
		    if not os.path.exists(root_path + target_folder):
		        os.makedirs(root_path + target_folder)
		    os.chdir(root_path + target_folder)
		    
		    
		    filename = datetime.datetime.now().strftime("%H-%M-%S")# based on time and date
		    self.qfig.savefig(filename)
		    np.save(filename, self.output)
		    
		    print filename


	# Save all data as an np array in the default directory or wherever specified
	def saveRaw(self, root_path = "/home/photon/data/"):
	    """
	    Save all data as an .npy of array of complex max values of fft's
	    Creates a folder with today's date: 01-13-2014
	    If folder for today doesn't exist, create it; else navigate to appropriate folder
	    """
	    target_folder = datetime.datetime.now().strftime("%m-%d-%Y")
	    if not os.path.exists(root_path + target_folder):
	        os.makedirs(root_path + target_folder)
	    os.chdir(root_path + target_folder)
	    
	    
	    filename = datetime.datetime.now().strftime("%H-%M-%S") + "_raw"  # based on time and date
	    np.save(filename, self.dataOut)
	    
	    print filename


	# Take a data set
	def takeData(self, N = 50, M = 20, ROI = [500, 900]): 
		# N is frame request size sent to the ZMQ server; M is rounds of data (total shots is N*M)
		minPixel = ROI[0]  # The pixel range for FFT analysis (Region Of Interest)
		maxPixel = ROI[1]

		self.dataOut = np.empty([maxPixel-minPixel,N,M],dtype=complex)
		for i in range(M):
		    self.request_images(N)
		    data = self.open_images()
		    frames = data.shape[2]
		    ydim = data.shape[0]
		    xdim = data.shape[1]

		    for f in range (0, frames):
		        corrected = data[:,:,f] - self.background[:,:] # could probably speed this up?
		        self.dataOut[:,f,i] = fft( corrected[195:205, minPixel:maxPixel].sum(axis = 0) ) 
		print "Finished"



	# Ask server to take N images
	def request_images(self, N=1):
	    shots_requested = N
	    request = str(shots_requested)  # ask for one shot of data
	    print "I: Sending (%s)" % request
	    
	    self.client.send(request)


	# Returns data from server
	def open_images(self):
	    socks = dict(self.poll.poll(self.REQUEST_TIMEOUT))
	    if socks.get(self.client) == zmq.POLLIN:
	        data_array = self.recv_array(self.client)
	        #reply = self.client.recv()
	    
	        if len(data_array) > 1:  # TODO test for the right size array
	            print "I: Server replied OK: " + str(data_array.shape)
	            return data_array
	    
	        else:
	            # print "E: Malformed reply from server: %s" % reply
	            print "E: no reply from server"
	            return -1


	# Reads off server socket
	def recv_array(self, socket, flags=0, copy=False, track=False):
	    """recv a numpy array"""
	    md = socket.recv_json(flags=flags)
	    msg = socket.recv(flags=flags, copy=copy, track=track)
	    buf = buffer(msg)
	    A = frombuffer(buf, dtype=md['dtype'])
	    return A.reshape(md['shape'])


	# Provides names of included functions in packages
	def help(self):
		print """\
		takeBackground( shots )
		clearData( )
		takeData( )
		findPeakMode( ) # Not yet implemented
		makeQfig( mode )
		saveQfig( path )
		saveRaw( path )

		request_images( client, shots )
		open_images( )
		recv_array( socket, flags, copy, track )\
		"""