#!/usr/bin/python
# -*- coding: utf-8 -*-

import Tkinter
import time

#imports for matplotlib embedding
import numpy
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as matPlot


#Button Callbacks TODO: place in separate FILE
def advanceCallBack():
    print("advance")

def reverseCallBack():
    print("reverse")
    

def flushCallBack():
    print("flush")
    
def startCallBack():
    print("advance")

def stopCallBack():
    print("reverse")
    

def resetCallBack():
    print("flush")
    
def leftThresholdButtonCallBack():
    print(leftThresholdEntry.textvariable)

def rightThresholdButtonCallBack():
    print(rightThresholdEntry.textvariable)


#import tkMessageBox
currentRow = 1

top = Tkinter.Tk()
top.title("Lever Arena GUI revision 1.0")
top.geometry('{}x{}'.format(1024,768)) #default window size
#top.configure(background = 'white')

#Plot embed
figure = matPlot.figure(1)
matPlot.ion()
axis = matPlot.gca()
#axis.set_axis_bgcolor('black')
t = numpy.arange(0.0,3.0,0.01)
s = numpy.sin(numpy.pi*t)
matPlot.plot(t,s)
canvas = FigureCanvasTkAgg(figure, master = top)
plot_widget = canvas.get_tk_widget().grid(row=currentRow, columnspan = 3)

currentRow += 1
    
#Logging Configuration
    
    
#Parameter Configuration
leftThresholdLabel = Tkinter.Label(top, text = "leftThreshold").grid(row = currentRow, column = 1)
leftThresholdEntry = Tkinter.Entry(top, text = "Threshold").grid(row = currentRow, column = 2)
leftThresholdButton = Tkinter.Button(top, text = "Set", command = leftThresholdButtonCallBack).grid(row = currentRow, column = 3)
currentRow += 1

rightThresholdLabel = Tkinter.Label(top, text = "rightThreshold").grid(row = currentRow, column = 1)
rightThresholdEntry = Tkinter.Entry(top).grid(row = currentRow, column = 2)
rightThresholdButton = Tkinter.Button(top, text = "Set", command = rightThresholdButtonCallBack).grid(row = currentRow, column = 3)
currentRow += 1

#Task Control
reverse = Tkinter.Button(top, text = "Reverse", command = reverseCallBack).grid(row = currentRow, column = 1)
advance = Tkinter.Button(top, text ="Advance", command = advanceCallBack).grid(row = currentRow, column = 2)
flush = Tkinter.Button(top, text ="Flush", command = flushCallBack).grid(row = currentRow, column = 3)
currentRow += 1

#Program Control

start = Tkinter.Button(top, text = "Start", command = startCallBack).grid(row = currentRow, column = 1)
stop = Tkinter.Button(top, text ="Stop", command = stopCallBack).grid(row = currentRow, column = 2)
reset = Tkinter.Button(top, text ="Reset", command = resetCallBack).grid(row = currentRow, column = 3)


#functions

def updateGUI():
    top.update_idletasks()
    top.update()


#main GUI loop
loopTime = time.time()
while True:
    currentTime = time.time()
    updateGUI()
    