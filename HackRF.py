#!/usr/bin/env python3

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import sys
import numpy as np
from collections import OrderedDict
from pyqtgraph.ptime import time
from scipy import ndimage as ndi;
import csaps
import pandas as PD


# Parses output strings from hackrf_sweep and adds them to the `data` dictionary
def parse(l: str):
    fields = l.replace('\n', "").split(", ")
    numEntries = len(fields) - 6

    # List of fields parsed out
    date = fields[0]
    time = fields[1]
    freqLower = int(fields[2])
    freqUpper = int(fields[3])
    freqSize = fields[4]
    numSamples = fields[5]
    samples = fields[6:numEntries + 6]

    freqWidth = freqUpper - freqLower
    freqSampleWidth = freqWidth // len(samples)

    # Loop through each sample and store it in `data`
    x = 0
    for samp in samples:
        data[freqLower + x * freqSampleWidth] = float(samp)
        x += 1


# Plots the current data
def update():
    global prevLength, lastTime, gaussianSigma
    pg.QtGui.QGuiApplication.processEvents()
    now = time()
    a = OrderedDict(sorted(data.items()))
    keys = np.array(list(a.keys()))
    vals = np.array(list(a.values()))
    minX = keys.min()
    maxX = keys.max()
    # pw.setXRange(minX, maxX)
    # pw.plot(keys, vals, clear=True)

    filteredVals = ndi.gaussian_filter1d(vals, gaussianSigma)
    pw.plot(keys, filteredVals, clear=True, fillLevel=-120, brush=(50,50,200,100))

    # sp = csaps.UnivariateCubicSmoothingSpline(keys, vals, smooth=0.25)
    # xs = np.linspace(keys[0], keys[-1], len(keys)//32)
    # pw.plot(xs, sp(xs), clear=True)
    # displayY = running_mean(np.array(list(a.values())), 2)
    # pw.plot(np.linspace(minX, maxX, len(displayY)), displayY, clear=True)
    # pw2.plot(np.abs(np.fft.fft(list(a.values()))), clear=True)


    if len(a.keys()) == prevLength:
        pw.enableAutoRange('xy', False)  # Stops auto-scaling
        # pw2.enableAutoRange('xy', False)  # Stops auto-scaling
    prevLength = len(a.keys())
    pg.QtGui.QGuiApplication.processEvents()




global data, prevLength, gaussianSigma
data = {}
prevLength = 0
gaussianSigma = 5
win = pg.GraphicsWindow(title="HackRF Visualizer")
# win.close.connect(doClose)

#setup tool window
toolWin = QtGui.QMainWindow()
toolWin.setWindowTitle('Settings')
toolCentralWidget = QtGui.QWidget()
toolLayout = QtGui.QGridLayout()
toolCentralWidget.setLayout(toolLayout)
toolWin.setCentralWidget(toolCentralWidget)
toolWin.show()

# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)
pg.setConfigOption('background', 'b')
pg.setConfigOption('foreground', 'g')

timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)


def gaussianSigmaChanged(sb : pg.SpinBox):
    global gaussianSigma
    gaussianSigma = sb.value()
    print("Gaussian Sigma changed to: %s" % str(sb.value()))
    sb.update()



if __name__ == "__main__":
    print("Processing HackRF Data...")

    # pw2 = win.addPlot(title="FFT")





    spins = [("Gaussian-Filter Sigma:", pg.SpinBox(value=5, bounds=[1, None], step=0.25))]
    for text, spin in spins:
        label = QtGui.QLabel(text)
        toolLayout.addWidget(label)
        toolLayout.addWidget(spin)
        spin.sigValueChanged.connect(gaussianSigmaChanged)

    pw = win.addPlot(title="HackRF Data Visualizer")



    for line in sys.stdin:
        if len(line) > 40:
            parse(line)
        pg.QtGui.QGuiApplication.processEvents()
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
