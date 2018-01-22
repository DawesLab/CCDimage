
#from qfigures import saveQfig, saveRaw
import datetime
import os
import numpy as np

def saveQfig(root_path = "/home/photon/Dropbox/Data/"):
    """
    Save Qfig data as .png of qfunc and .npy of array of complex max values of fft's
    Creates a folder with today's date: 01-13-2014
    If folder for today doesn't exist, create it; else navigate to appropriate folder
    """
    target_folder = datetime.datetime.now().strftime("%m-%d-%Y")
    if not os.path.exists(root_path + target_folder):
        os.makedirs(root_path + target_folder)
    os.chdir(root_path + target_folder)


    filename = datetime.datetime.now().strftime("%H-%M-%S")# based on time and date
    qfig.savefig(filename)
    np.save(filename, output)

    print(filename)

def saveRaw(VacCorrected,ncount,root_path = "/home/photon/data/"):
    """
    Save Raw zipped data as .npz of array of complex max values of fft's
    Creates a folder with today's date: 01-13-2014
    If folder for today doesn't exist, create it; else navigate to appropriate folder
    """
    target_folder = datetime.datetime.now().strftime("%m-%d-%Y")
    if not os.path.exists(root_path + target_folder):
        os.makedirs(root_path + target_folder)
    os.chdir(root_path + target_folder)


    filename = datetime.datetime.now().strftime("%H-%M-%S") + "_raw"  # based on time and date
    np.savez(filename, VacCorrected=VacCorrected, ncount=ncount)

    print(filename)
