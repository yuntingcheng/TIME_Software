from pyqtgraph import QtCore, QtGui
import numpy as np
import sys, os, subprocess, time, datetime, socket, struct, threading
import pyqtgraph as pg
import test_read_files as rf
import random as rm
import netcdf as nc
import settings as st
from termcolor import colored
import time
import multiprocessing as mp
from multiprocessing import Process, Manager

sys.stdout = os.fdopen(sys.stdout.fileno(),'w',1) #line buffering

#class of all components of GUI
class mcegui(QtGui.QWidget):
    #initializes mcegui class and calls other init functions
    def __init__(self):
        super(mcegui, self).__init__()
        self.init_mce()
        self.init_ui()
        self.qt_connections()

    #sets all of the variables for mce/graph, deletes old gui_data_test files
    def init_mce(self):
        self.timeinterval = 1
        self.observer = ''
        self.datamode = ''
        self.readoutcard = ''
        self.framenumber = ''
        self.frameperfile = 100
        self.totaltimeinterval = 120
        self.currentchannel = 1
        self.row = 1
        self.oldch = 1

    #creates GUI window and calls functions to populate GUI
    def init_ui(self):
        self.setWindowTitle('MCE TIME Data')
        self.getparameters()
        self.grid = QtGui.QGridLayout()
        self.grid.addLayout(self.parametersquit, 1, 1, 1, 1)
        self.setLayout(self.grid)
        self.setGeometry(10, 10, 1920, 1080)
        self.show()

    #reacts to button presses and other GUI user input
    def qt_connections(self):
        self.quitbutton.clicked.connect(self.on_quitbutton_clicked)
        self.submitbutton.clicked.connect(self.on_submitbutton_clicked)
        self.selectchannel.currentIndexChanged.connect(self.changechannel)
        self.readoutcardselect.currentIndexChanged.connect(self.changereadoutcard)
        self.selectrow.currentIndexChanged.connect(self.changerow)

    #quits out of GUI and stops the MCE
    def on_quitbutton_clicked(self):
        print('Quitting Application')
        #stop mce with subprocess
        if self.showmcedata == 'Yes':
            ''' have something that stops reading data files '''
        sys.exit()

    #sets parameter variables to user input and checks if valid - will start MCE
    #and live graphing if they are
    def on_submitbutton_clicked(self):
        #set variables to user input
        # observer ---------------------------------------
        self.observer = self.enterobserver.text()
        # data mode --------------------------------------
        self.datamode = self.enterdatamode.currentText()
        if self.datamode == 'Error':
            self.datamode = 0
        elif self.datamode == 'Raw':
            self.datamode = 12
        elif self.datamode == 'Low Pass Filtered':
            self.datamode = 2
        elif self.datamode == 'Mixed Mode':
            self.datamode = 10
        elif self.datamode == 'SQ1 Feedback':
            self.datamode = 1
        # readout card ---------------------------------------------
        self.readoutcard = self.enterreadoutcard.currentIndex() + 1
        if self.readoutcard == 9:
            self.readoutcard = 'All'
            self.currentreadoutcard = 2
            self.currentreadoutcarddisplay = 'MCE 1 RC 2'
        # frame number ----------------------------------------------
        self.framenumber = self.enterframenumber.text()
        # data rate -------------------------------------------------
        self.datarate = self.enterdatarate.text()
        # how much data to view on screen at once -------------------
        self.timeinterval = self.entertimeinterval.text()
        # keep old channel data on graph ----------------------------
        self.channeldelete = self.enterchanneldelete.currentText()
        # keep mce data on screen -----------------------------------
        self.showmcedata = self.entershowmcedata.currentText()
        # time keepers ----------------------------------------------
        self.timestarted = datetime.datetime.utcnow()
        self.timestarted = self.timestarted.isoformat()

        #check if parameters are valid - will create warning box if invalid
        if self.observer == '' or self.framenumber == '' or self.framenumber == '0'\
        or self.datarate == '0' or self.datarate == '' or self.timeinterval == ''\
        or self.timeinterval == '0':
            self.parameterwarning = QtGui.QMessageBox()
            self.parameterwarning.setIcon(QtGui.QMessageBox.Warning)
            self.parameterwarning.setText('One or more parameters not entered correctly!')
            self.parameterwarning.setStandardButtons(QtGui.QMessageBox.Ok)
            self.parameterwarning.setWindowTitle('Parameter Warning')
            self.parameterwarning.buttonClicked.connect(self.on_warningbutton_clicked)
            self.parameterwarning.exec_()
        elif self.showmcedata == 'No':
            self.submitbutton.setEnabled(False)
        else:
            parafile = open('tempfiles/tempparameters.txt', 'w')
            parafile.write(self.observer+' ')
            parafile.write(str(self.datamode)+' ')
            parafile.write(str(self.readoutcard)+' ')
            parafile.write(self.framenumber+' ')
            parafile.write(self.datarate+' ')
            parafile.write(self.timeinterval+' ')
            parafile.write(self.channeldelete+' ')
            parafile.write(self.timestarted+' ')
            parafile.close()

            self.channelselection()
            print(colored('Time Started: %s' % (self.timestarted),'magenta'))
            self.frameperfile = int((50 * 10 ** 6) / (33 * 90 * int(self.datarate))) #calculation taken from UBC MCE Wiki
            print(colored('Frame per file: %s' % (self.frameperfile),'magenta'))

            # prevents user from re-activating everything
            self.submitbutton.setEnabled(False)

            print(colored('Readout Card : %s' %(self.readoutcard),'magenta'))

            # initialize child processes and create plots
            self.a = Manager().Value('i', 0)
            new_files = mp.Process(target = self.file_checker, daemon = True)
            #move_files = mp.Process(target = self.file_transfer, daemon = True)
            new_files.start()
            #move_files.start()
            self.initplot()

    #resets parameter variables after warning box is read
    def on_warningbutton_clicked(self):
        self.observer = ''
        self.datamode = ''
        self.readoutcard = ''
        self.framenumber = ''

    #creates inputs for user to enter parameters and creates 'Quit' button
    def getparameters(self):
        self.parametersquit = QtGui.QVBoxLayout()

        #creating user input boxes
        self.enterobserver = QtGui.QLineEdit('VLB')
        self.enterobserver.setMaxLength(3)
        self.enterdatamode = QtGui.QComboBox()
        self.enterdatamode.addItems(['Error', 'Raw', 'Low Pass Filtered', 'Mixed Mode', 'SQ1 Feedback'])
        self.enterreadoutcard = QtGui.QComboBox()
        for i in range(8):
            if i < 4:
                self.enterreadoutcard.addItem('MCE 1 RC %s' % (i % 4 + 1))
            else:
                self.enterreadoutcard.addItem('MCE 2 RC %s' % (i % 4 + 1))
        self.enterreadoutcard.addItem('All')
        self.enterframenumber = QtGui.QLineEdit('1350000')
        self.enterframenumber.setMaxLength(9)
        self.enterdatarate = QtGui.QLineEdit('45')
        self.entertimeinterval = QtGui.QLineEdit('120')
        self.enterchanneldelete = QtGui.QComboBox()
        self.enterchanneldelete.addItems(['No', 'Yes'])
        self.entershowmcedata = QtGui.QComboBox()
        self.entershowmcedata.addItems(['Yes', 'No'])
        self.submitbutton = QtGui.QPushButton('Submit')

        self.parameters = QtGui.QFormLayout()
        self.parameters.addRow('Observer', self.enterobserver)
        self.parameters.addRow('Datamode', self.enterdatamode)
        self.parameters.addRow('Readout Card', self.enterreadoutcard)
        self.parameters.addRow('Frame Number', self.enterframenumber)
        self.parameters.addRow('Data Rate', self.enterdatarate)
        self.parameters.addRow('Delete Old Columns', self.enterchanneldelete)
        self.parameters.addRow('Time Interval (s)', self.entertimeinterval)
        self.parameters.addRow('Show MCE Data', self.entershowmcedata)
        self.parameters.addRow(self.submitbutton)

        self.parametersquit.addLayout(self.parameters)

        #creating quit button
        self.quitbutton = QtGui.QPushButton('Quit')
        self.parametersquit.addWidget(self.quitbutton)

        self.readoutcardselect = QtGui.QComboBox()
        self.selectchannel = QtGui.QComboBox()
        self.selectrow = QtGui.QComboBox()

    #creates input to change channel of live graph during operation, also adds
    #input for readout card if reading All readout cards
    def channelselection(self):
        self.channelreadoutbox = QtGui.QFormLayout()

        #adds readout card dropbox if All
        if self.readoutcard == 'All':
            for i in range(32):
                self.selectchannel.addItem(str(i))
        else:
            self.selectchannel.addItems(['0', '1', '2', '3', '4', '5', '6', '7'])
        #creates channel dropbox

        for i in range(33):
            self.selectrow.addItem(str(i))

        self.channellabel = QtGui.QLabel('Column')

        self.rowlabel = QtGui.QLabel('Row')

        self.channelreadoutbox.addRow(self.channellabel, self.selectchannel)

        self.channelreadoutbox.addRow(self.rowlabel, self.selectrow)

        self.grid.addLayout(self.channelreadoutbox, 3, 1, 1, 1)

    #changes channel of live graph when user changes channel
    def changechannel(self):
        self.currentchannel = int(self.selectchannel.currentText()) + 1
        if self.readoutcard == 'All':
	           self.changereadoutcard()
        #print(self.currentchannel)

    def changerow(self):
        self.row = int(self.selectrow.currentText()) + 1
        print("Num of Rows:",self.row)

    #changes readout card of live graph when user changes readout card
    def changereadoutcard(self):
    	if self.currentchannel < 9:
    	   self.currentreadoutcard = 1
    	   self.currentreadoutcarddisplay = 'MCE 1 RC 1'
    	elif self.currentchannel >= 9 and self.currentchannel < 17:
    	   self.currentreadoutcard = 2
    	   self.currentreadoutcarddisplay = 'MCE 1 RC 2'
    	elif self.currentchannel >= 17 and self.currentchannel < 25:
    	   self.currentreadoutcard = 3
    	   self.currentreadoutcarddisplay = 'MCE 1 RC 3'
    	elif self.currentchannel >= 25:
    	   self.currentreadoutcard = 4
    	   self.currentreadoutcarddisplay = 'MCE 1 RC 4'
    	self.currentreadoutcardtext.setText('Current Readout Card: %s' % (self.currentreadoutcarddisplay))
            #self.currentreadoutcarddisplay = self.readoutcardselect.currentText()

    #initializes graph for live viewing of data
    def initplot(self):
        #initialize time
        self.starttime = datetime.datetime.utcnow()
        self.totaltimeinterval = int(self.timeinterval)

        self.mce = 1

        #initalize data list
        ''' This is meant to store old data '''
        self.data = [0, 0, 0]

        #initialize graph GUI item
        self.mcegraphdata = pg.ScatterPlotItem()
        self.mcegraph = pg.PlotWidget()
        self.grid.addWidget(self.mcegraph, 1, 5, 2, 3)

        #add labels to graph
        self.mcegraph.setLabel('bottom', 'Time', 's')
        self.mcegraph.setLabel('left', 'Counts')
        self.mcegraph.setTitle('MCE TIME Data')

        #initalize old data graph GUI item and add labels
        self.oldmcegraph = pg.PlotWidget()
        self.oldmcegraphdata = pg.PlotCurveItem()
        self.grid.addWidget(self.oldmcegraph, 1, 2, 2, 3)
        self.oldmcegraph.setLabel('bottom', 'Time', 's')
        self.oldmcegraph.setLabel('left', 'Counts')
        self.oldmcegraph.setTitle('Old MCE TIME Data')
        self.oldmcegraph.addItem(self.oldmcegraphdata)

    #writes and updates data to both live graph and old graph
    def updateplot(self):
        a = self.graphdata1[0]
        ch = self.graphdata1[1]
        y = self.graphdata1[2][:self.frameperfile]
        self.y = y

        #creates x values for current time interval and colors points based on current channel ===
        pointcolor = []
        pointsymbol = []
        x = []
        ''' Need a way to make end of time array be the actual amount of time it
            took to create that file '''
        x = np.linspace(self.a,self.a + 1,self.frameperfile)
        ''' I think he's just making an array that will fill x with the same
            number of points that are in y, there are way easier ways to do this... '''
        self.x = x
        # =====================================================================================
        #picks color based on current channel =============================================
        # if ch % 8 == 1:
        if ch == 1 :
            #pointcolor.append(pg.mkBrush('b'))
            pointcolor.extend([pg.mkBrush('b') for i in range(self.frameperfile)])
        elif ch == 2 :
            # pointcolor.append(pg.mkBrush('r'))
            pointcolor.extend([pg.mkBrush('r') for i in range(self.frameperfile)])
        elif ch == 3 :
            # pointcolor.append(pg.mkBrush('g'))
            pointcolor.extend([pg.mkBrush('g') for i in range(self.frameperfile)])
        elif ch == 4 :
            # pointcolor.append(pg.mkBrush('y'))
            pointcolor.extend([pg.mkBrush('y') for i in range(self.frameperfile)])
        elif ch == 5 :
            # pointcolor.append(pg.mkBrush('c'))
            pointcolor.extend([pg.mkBrush('c') for i in range(self.frameperfile)])
        elif ch == 6 :
            # pointcolor.append(pg.mkBrush('m'))
            pointcolor.extend([pg.mkBrush('m') for i in range(self.frameperfile)])
        elif ch == 7 :
            # pointcolor.append(pg.mkBrush('k'))
            pointcolor.extend([pg.mkBrush('k') for i in range(self.frameperfile)])
        else :
            # pointcolor.append(pg.mkBrush('w'))
            pointcolor.extend([pg.mkBrush('w') for i in range(self.frameperfile)])
        # =================================================================================================================
        # changes symbols for viewing different RC cards on same plot =====================
        if self.readoutcard == 'All':
            # if self.currentreadoutcard % 4 == 1:
            if self.currentreadoutcard == 1:
                pointsymbol.append('o')
            elif self.currentreadoutcard == 2:
                pointsymbol.append('s')
            elif self.currentreadoutcard == 3:
                pointsymbol.append('t')
            elif self.currentreadoutcard == 0:
                pointsymbol.append('d')
        else :
            pass
        #============================================================================================================
        #creates graphdata item on first update
        if self.a == 1:
            print(colored('Triggered first if statement','red'))
            self.mcegraph.addItem(self.mcegraphdata)
            self.mcegraph.setXRange(self.a - 1, self.a + self.totaltimeinterval - 1, padding=0)
            if self.readoutcard == 'All':
                self.mcegraphdata.setData(x, y, brush=pointcolor, symbol=pointsymbol)
            else:
                self.mcegraphdata.setData(x, y, brush=pointcolor)
            self.oldch = ch
            # updates oldgraph data
            self.data[0] = x
            self.data[1] = y
            # recasts for plotting
            x = np.asarray(x)
            y = np.asarray(y)
        # ===========================================================================================================
        #clears graphdata and updates old graph after the total time interval has passed
        elif self.a == self.totaltimeinterval :
            print(colored('Triggered elif statement','red'))
            self.oldmcegraph.setXRange(self.data[0][0], self.data[0][-1], padding=0)
            self.oldmcegraphdata.setData(self.data[0], self.data[1])
            self.mcegraphdata.clear()
            self.mcegraph.setXRange(self.a - 1, self.a + self.totaltimeinterval - 1, padding=0)
            if self.readoutcard == 'All':
                self.mcegraphdata.setData(x, y, brush=pointcolor, symbol=pointsymbol)
            else:
                self.mcegraphdata.setData(x, y, brush=pointcolor)
            self.data = [0, 0, 0]
            # updates oldgraphdata after total time interval is reached
            self.data[0] = x
            self.data[1] = y
            # recasts for plotting
            x = np.asarray(x)
            y = np.asarray(y)
        # ==============================================================================================================
        #updates graph, if channel delete is set to yes will clear data first
        else:
            print(colored('Triggered else statement','red'))
            if self.channeldelete == 'Yes' and self.oldch != ch:
                self.mcegraphdata.clear()
                if self.readoutcard == 'All':
                    self.mcegraphdata.setData(x, y, brush=pointcolor, symbol=pointsymbol)
                else:
                    self.mcegraphdata.setData(x, y, brush=pointcolor)
            else:
                if self.readoutcard == 'All':
                    self.mcegraphdata.addPoints(x, y, brush=pointcolor, symbol=pointsymbol)
                else:
                    self.mcegraphdata.addPoints(x, y, brush=pointcolor)
            # updates old data for when graph resets
            self.data[0].extend(x) # doesn't create a new array but adds to existing
            self.data[1].extend(y)
        # =================================================================================================================
        self.oldch = ch
        #watchdog for time to update graph/heatmap/K-mirror data
        self.endtime = datetime.datetime.utcnow()
        self.timetaken = self.endtime - self.starttime
        print('Time taken: %s' % (self.timetaken))
        # =================================================================================================================
        #initializes old data list on either the first update or the first one after
        #the current total time interval, otherwise adds to current list

        if self.a == 1 or self.a % self.totaltimeinterval == 2:
            self.data[0] = x
            self.data[1] = y
        else:
            self.data[0].extend(x) # doesn't create a new array but adds to existing
            self.data[1].extend(y)
        #recasts x, y as arrays for updating the graph data
        x = np.asarray(x)
        y = np.asarray(y)

    def warningbox(self,message):
        if message == 'KMS' :
            self.kmswarning = QtGui.QMessageBox()
            self.kmswarning.setIcon(QtGui.QMessageBox.Warning)
            self.kmswarning.setText('System has halted due to Kmirror E-Stop. Please standby for user reset...')
            self.kmswarning.setStandardButtons(QtGui.QMessageBox.Ok)
            self.kmswarning.setWindowTitle('KMirror System Emergency Stopped!')
            #self.kmswarning.buttonClicked.connect(self.on_warningbutton_clicked)
            self.kmswarning.exec_()
        elif message == 'tel' :
            self.telwarning = QtGui.QMessageBox()
            self.telwarning.setIcon(QtGui.QMessageBox.Warning)
            self.telwarning.setText('The telescope has unexpectedly halted normal operations. Software must be reset by user.')
            self.telwarning.setStandardButtons(QtGui.QMessageBox.Ok)
            self.telwarning.setWindowTitle('Telescope Emergency Stop')
            #self.telwarning.buttonClicked.connect(self.on_warningbutton_clicked)
            self.telwarning.exec_()
        elif message == 'hk' :
            self.hkwarning = QtGui.QMessageBox()
            self.hkwarning.setIcon(QtGui.QMessageBox.Warning)
            self.hkwarning.setText('Housekeeping as reported an error. No files are being created.')
            self.hkwarning.setStandardButtons(QtGui.QMessageBox.Ok)
            self.hkwarning.setWindowTitle('Housekeeping Error')
            #self.hkwarning.buttonClicked.connect(self.on_warningbutton_clicked)
            self.hkwarning.exec_()

    ''' for linux distro only ... '''
    # def file_checker(self) :
    #     import inotify.adapters
    #     import os
    #     notifier = inotify.adapters.Inotify()
    #     notifier.add_watch('/home/pilot1/test_mce_file_final')
    #     for event in notifier.event_gen():
    #         if self.a == 0 :
    #             self.z1, self.graphdata1, self.mce = rf.netcdfdata(self.a, self.readoutcard, self.currentchannel, self.row)
    #         else :
    #             if event is not None:
    #                 if 'IN_CREATE' in event[1]:
    #                     self.a += 1
    #                     self.z1, self.graphdata1 = rf.netcdfdata(self.a, self.readoutcard, self.currentchannel, self.row)
    #     self.updateplot()

    def file_checker(self) :
        dir = '/home/pilot1/test_mce_file/test_mce_files'
        if os.path.exists(dir + 'test_data.%0.3i' %(int(self.a.value))) :
            if self.a == 0 :
                self.z1, self.graphdata1, self.mce = rf.netcdfdata(self.a, self.readoutcard, self.currentchannel, self.row)
            else :
                self.a += 1
                self.z1, self.graphdata1 = rf.netcdfdata(self.a, self.readoutcard, self.currentchannel, self.row)
        self.updateplot()
        time.sleep(1.0)

#calls mcegui class to start GUI
def main():
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('TIME Raw Data Visualization Suite')
    ex = mcegui()
    sys.exit(app.exec_())

#test changes
if __name__ == '__main__':
    main()
