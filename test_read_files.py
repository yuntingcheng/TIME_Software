import numpy as np
import os, sys, time, logging, mce_data, subprocess
import netcdf as nc
import datetime as dt
from termcolor import colored
import mce_data
import sys
# sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 1) # line buffering

class Read_Files:

    def __init__(self, a, rc, ch, row):
        self.a = a
        self.rc = rc
        self.ch = ch
        self.row = row
        self.d1 = []
        self.graphdata1 = []
        self.file1 = ''

    def readdata(self):
        f1 = mce_data.SmallMCEFile(self.file1)
        h1 = f1.Read(row_col=True, unfilter='DC').data
        self.d1 = np.empty([h1.shape[0],h1.shape[1]],dtype=float)
        for b in range(h1.shape[0]):
            for c in range(h1.shape[1]):
                self.d1[b][c] = (np.std(h1[b][c][:],dtype=float))
        g1 = h1[:,self.ch - 1]
        array1 = []
        for j in range(g1.shape[1]):
            array1.append(g1[self.row - 1][j])
        self.graphdata1 = [self.ch,array1]
        return self.d1, self.graphdata1

    def netcdfdata(self):
        dir1 = '/Users/vlb9398/Desktop/test_mce_files/'
        self.file1 = (dir1 + 'test_data.%0.3i' %(self.a))
        print(colored('File Read: %s' %(self.file1.replace(dir1,'')),'yellow'))
        s,t = self.readdata()
        return s,t
