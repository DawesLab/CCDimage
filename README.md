CCDimage
========

IPython notebooks for collecting and saving data from our CCD camera.

These use the pypicam module provided by PythonForPicam and the Camserver "Server.py" code.

The workflow is as follows:

from a Camserver folder run (to start the image server)

`sudo python Server.py`

then start an ipython notebook server as a regular user (e.g.):

`ipython notebook --profile=server`

the CCDimage.ipynb notebook steps through a basic data collection and analysis sequence.

*TODO: add automatic selection of the FFT index to analyze. Noah has code that did some of this.* 


