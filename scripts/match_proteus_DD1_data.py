'''
 daniel vogler
 daniel.vogler@erdw.ethz.ch
 2015
 
 e.g.
 python3 match_proteus_DD1_data.py ~/projects/3d_printed_sstone/data/bt/ ethz_ss_n_massongex_d52mm_18p-45-0
 '''
 
import csv
import collections
import numpy as np
#import pylab as pl

import matplotlib
import matplotlib.pyplot as pl

import sys

import glob, os

import math

import time
from datetime import datetime

from scipy.interpolate import splev, splrep
from scipy import interpolate

####### definitions

btRadius = 0.0251

print( "\n System input variables" )
print( str(sys.argv) )


# read in filepath from command line
filepath =  sys.argv[1]
loadFile =  sys.argv[2]

print( "Reading data for test" )
print( str(filepath+loadFile+"\n") )

print( "##############################################################" )
print( "Loading Brazilian test data \n" )

# search string
btSearchString = 'Index'
# 
fileToLoad = str(filepath+loadFile+".txt")
with open(fileToLoad) as file:
        btFile = csv.reader(file, delimiter=';', skipinitialspace=True)
        for line in btFile:
                btData = list(btFile)
        #
		# find search string occurences in list
        btIndices = [l for l, s in enumerate(btData) if str(btSearchString) in s]

# initialize variables
btIndex = []
btElement = []
btMarker = []
btTime = []
btTimeTS = []
btTimeHMS = []
btForceDiff = []
btMachineDisplacement = []
btSensorDisplacement = []
btSigmaZ = []

btTimeStr = []

# seperate data sheets
for l in range(btIndices[0]+2, btIndices[1]-3):
    btIndex.append( float(btData[l][0]) )
    btElement.append( float(btData[l][1]) )
    btMarker.append( float(btData[l][2]) )
    btTime.append( btData[l][3]) 
    btTimeHMS.append( time.strptime(btData[l][3], "%H:%M:%S:%f") )
    btForceDiff.append( float(btData[l][4]) )
    btMachineDisplacement.append( float(btData[l][5]) )
    #btSensorDisplacement.append( float(btData[l][6]) )
    btSigmaZ.append( float(btData[l][4])/(math.pi*btRadius**2) )

# formula for sigma tensile
# sigma_tensile = ( 2*PrimaryFailureLoad) / (pi * diameter * thickness) in [MPa]

# initialize time variable
btHours = []
btMinutes = []
btSeconds = []
btMiliseconds = []
btTimeMiliseconds = []
timeS = []

# convert brazilian test data to miliseconds
for i in range(len(btTime)):
    timeS.append(btTime[i])
    h, m, s, ms = (["0", "0"] + timeS[i].split(":"))[-4:]
    btHours.append( int(h) )
    btMinutes.append( int(m) )
    btSeconds.append( float(s) )
    btMiliseconds.append( float(ms) )
    btTimeMiliseconds.append( int(3600000 * btHours[i] + 60000 * btMinutes[i] + 1000 * btSeconds[i] + btMiliseconds[i] ) )

btTimeMiliseconds = np.array(btTimeMiliseconds).astype(np.float)
btTimeSeconds = btTimeMiliseconds/1000

# convert to float
btForceDiff = np.array(btForceDiff).astype(np.float)
btMachineDisplacement = np.array(btMachineDisplacement).astype(np.float)
#btSensorDisplacement = np.array(btSensorDisplacement).astype(np.float)
btSigmaZ = np.array(btSigmaZ).astype(np.float)/1000

# find maximum load and stress indexes
maxLoadIdx = btForceDiff.argmax(axis=0)
maxSigmaZIdx = btSigmaZ.argmax(axis=0)

print( "Brazilian test data starting at %s" %btTime[0] )
print( "in miliseconds %i \n" %btTimeMiliseconds[0] )
print( "in seconds %i \n" %btTimeSeconds[0] )



print( "Maximum force difference during Experiment:" )
print( "%3.2f [kN]" % btForceDiff[maxLoadIdx] )
print( "%3.2f [MPa] \n" % btSigmaZ[maxSigmaZIdx] )



print( "##############################################################" )
print( "Read DD1 test data information \n" )
# search string
dd1InfoSearchString = 'Start time'
# 
fileToLoad = str(filepath+loadFile+".TSX")
with open(fileToLoad) as file:
        dd1InfoFile = csv.reader(file, delimiter='=', skipinitialspace=True)
        for line in dd1InfoFile:
                dd1Info = list(dd1InfoFile)

# find start time
dd1InfoIndices = [l for l, s in enumerate(dd1Info) if str(dd1InfoSearchString) in s]
dd1StartTime = dd1Info[dd1InfoIndices[0]][1]
dd1StartTimeSplit = dd1StartTime.split()
dd1StartDateTS = time.strptime(dd1StartTimeSplit[0], "%d.%m.%Y") 
dd1StartTimeTS = time.strptime(dd1StartTimeSplit[1], "%H:%M:%S")
dd1StartDateTime = time.strptime(dd1StartTime, "%d.%m.%Y %H:%M:%S")

# convert dd1 test data to miliseconds
h, m, s = (["0", "0"] + dd1StartTimeSplit[1].split(":"))[-3:]
dd1StartTimeMiliseconds = ( int(3600000 * int(h) + 60000 * int(m) + 1000 * float(s) ) )
dd1StartTimeSeconds = dd1StartTimeMiliseconds/1000


print( "DD1 test data starting on %s at %s" %(dd1StartTimeSplit[0], dd1StartTimeSplit[1]) )
print( "in miliseconds %i " %dd1StartTimeMiliseconds )
print( "in seconds %i \n" %dd1StartTimeSeconds )



print( "##############################################################" )
print( "Loading DD1 test data \n" )

# search string
dd1DataSearchString = 'Time'
# 
fileToLoad = str(filepath+loadFile+".ASC")
with open(fileToLoad) as file:
        dd1File = csv.reader(file, delimiter='\t', skipinitialspace=True)
        for line in dd1File:
                dd1Data = list(dd1File)
        #
        # find search string occurences in list
        dd1Indices = [l for l, s in enumerate(dd1Data) if str(dd1DataSearchString) in s]

# initialize variables
dd1Time = []# [s]
dd1L = []   # [mV/V]
dd1R = []   # [mV/V]

# seperate data sheets
for l in range(0, len(dd1Data) ):
    dd1Time.append( dd1Data[l][0]) 
    dd1L.append( float(dd1Data[l][1]) )
    dd1R.append( float(dd1Data[l][2]) )

# convert to float
dd1L = np.array(dd1L).astype(np.float)
dd1R = np.array(dd1R).astype(np.float)
dd1TimeSeconds = np.array(dd1Time).astype(np.float)

# find max/min voltages
maxdd1LIdx = dd1L.argmax(axis=0)
maxdd1RIdx = dd1R.argmax(axis=0)
mindd1LIdx = dd1L.argmin(axis=0)
mindd1RIdx = dd1R.argmin(axis=0)

print( "Maximum voltage during Experiment:" )
print( "%1.5f [mV/V]" % dd1L[maxdd1LIdx] )
print( "%1.5f [mV/V] \n" % dd1R[maxdd1RIdx] )
 
print( "Minimum voltage during Experiment:" )
print( "%1.5f [mV/V]" % dd1L[mindd1LIdx] )
print( "%1.5f [mV/V] \n" % dd1R[mindd1RIdx] )

# convert both times into global times
dd1GlobalTimeSeconds = dd1TimeSeconds
btGlobalTimeSeconds =  btTimeSeconds - dd1StartTimeSeconds


print( "##############################################################" )
print( "Number of measurement points \n" )
print( "Brazilian test \t- %d" %len(btGlobalTimeSeconds) )
print( "DD1 Sensors \t- %d\n" %len(dd1GlobalTimeSeconds) )

print( "Brazilian test \t- %d" %len(btGlobalTimeSeconds) )
print( "DD1 Sensors \t- %d\n" %len(dd1GlobalTimeSeconds) )


print( "##############################################################" )
print( "Merge data sets \n" )

minTime = min(btGlobalTimeSeconds[0], dd1GlobalTimeSeconds[0])
maxTime = max(btGlobalTimeSeconds[-1], dd1GlobalTimeSeconds[-1])

upperMinTime = max(btGlobalTimeSeconds[0], dd1GlobalTimeSeconds[0])
lowerMaxTime = min(btGlobalTimeSeconds[-1], dd1GlobalTimeSeconds[-1])

boundMin = upperMinTime*1000
boundMax = lowerMaxTime*1000
globalTimeSecondsInt = np.arange( boundMin, boundMax, 1)

globalTimeline = np.arange(minTime*1000,maxTime*1000,1)

# interpolate BT sigma z
fBtSigmaZ = interpolate.interp1d(btGlobalTimeSeconds*1000, btSigmaZ)
btSigmaZInt = fBtSigmaZ( globalTimeSecondsInt )  

# interpolate BT machine displacement
fBtMachineDisplacement = interpolate.interp1d(btGlobalTimeSeconds*1000, btMachineDisplacement)
btMachineDisplacementInt = fBtSigmaZ( globalTimeSecondsInt )  

# interpolate dd1 L
fDD1L = interpolate.interp1d(dd1GlobalTimeSeconds*1000, dd1L)
DD1LInt = fDD1L( globalTimeSecondsInt ) 

# interpolate dd1 R
fDD1R = interpolate.interp1d(dd1GlobalTimeSeconds*1000, dd1R)
DD1RInt = fDD1R( globalTimeSecondsInt )



print( "##############################################################" )
print( "Plotting Figures \n" )

# plots
# settings
markerSize = 10.0
lineStyle = '-'
legendLocation = "upper left"
Color = ['b', 'r', 'm', 'g']
conversionFactor = 1000

# plot 
pl.figure()

pl.plot( btMachineDisplacement[0:maxSigmaZIdx], btSigmaZ[0:maxSigmaZIdx], c='r', marker='o', label='Experiment', markersize=markerSize, linestyle=lineStyle)

pl.xlabel('Displacement [mm]')
pl.legend(loc=legendLocation, numpoints = 1)
pl.grid(b=True, which='major', color='lightgrey', linestyle='-')



# plot 
pl.figure()

pl.plot( dd1GlobalTimeSeconds, dd1L, c='r', label='dd1L', markersize=markerSize, linestyle=lineStyle)
pl.plot( dd1GlobalTimeSeconds, dd1R, c='g', label='dd1R', markersize=markerSize, linestyle=lineStyle)
pl.plot( btGlobalTimeSeconds, btMachineDisplacement, c='b', label='Displacement', markersize=markerSize, linestyle=lineStyle)

pl.xlabel('Time [s]')
pl.legend(loc=legendLocation, numpoints = 1)
pl.grid(b=True, which='major', color='lightgrey', linestyle='-')



# plot sigma tensile vs. time
pl.figure()
pl.plot( globalTimeSecondsInt, btSigmaZInt, '-',label='BT Experiment')
pl.xlabel('Time [s]')
pl.ylabel('Sigma Tensile [MPa]]')
pl.legend(loc=legendLocation, numpoints = 1)
pl.grid(b=True, which='major', color='lightgrey', linestyle='-')



# plot dd1 data vs. sigma tensile
pl.figure()
pl.plot( btSigmaZInt, DD1LInt, '-', color='r',label='dd1 L')
pl.plot( btSigmaZInt, DD1RInt, '-', color='b',label='dd1 R')
pl.xlabel('Sigma tensile [MPa]')
pl.ylabel('dd1 [mV/V]')
pl.legend(loc=legendLocation, numpoints = 1)
pl.grid(b=True, which='major', color='lightgrey', linestyle='-')



# plot dd1 data vs. machine displacement
pl.figure()
pl.plot( btMachineDisplacementInt, DD1LInt, '-', color='r',label='dd1 L')
pl.plot( btMachineDisplacementInt, DD1RInt, '-', color='b',label='dd1 R')
pl.xlabel('Machine displacement [mm]')
pl.ylabel('dd1 [mV/V]')
pl.legend(loc=legendLocation, numpoints = 1)
pl.grid(b=True, which='major', color='lightgrey', linestyle='-')


pl.show()
exit()
