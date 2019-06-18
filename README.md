# pyhackrf

Introduction:
 - This application is a signal visualizer for data from the [HackRF One](https://greatscottgadgets.com/hackrf/one/) Software-Defined Radio (SDR). This is very much still a work in progress.

Dependencies:
 - [pyqtgraph](http://www.pyqtgraph.org/)
 - [pyqt5](https://pypi.org/project/PyQt5/)
 - [numpy](https://www.numpy.org/)
 - [scipy](https://www.scipy.org/)
 
Usage:
 - Pipe the output of [hackrf_sweep](https://github.com/mossmann/hackrf/wiki/hackrf_sweep) into the application.
   - Example:  hackrf_sweep -f 70:110 -w 10000 | ./HackRF.py
   
Features:
 - Zoom, Pan, Gaussian Filter
