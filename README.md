# pyhackrf

Introduction:
 - This application is a signal visualizer for data from the HackRF One Software-Defined Radio (SDR). This is very much still a work in progress.

Dependencies:
 - pyqtgraph
 - pyqt5
 - numpy
 - scipy
 
Usage:
 - Pipe the output of hackrf_sweep into the application.
   - Example:  hackrf_sweep -f 70:110 -w 10000 | ./HackRF.py
