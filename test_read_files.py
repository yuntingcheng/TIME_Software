import numpy as np
import os, sys, time, logging, mce_data, subprocess
import netcdf as nc
import datetime as dt
from termcolor import colored
import mce_data
import sys
# sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 1) # line buffering
a = 0

def gui_data():
    dir1 = '/Users/vlb9398/Desktop/test_mce_files/'
    file1 = (dir1 + 'test_data.%0.3i' %(a))
    f1 = mce_data.SmallMCEFile(file1)
    h1 = file1.Read(row_col=True, unfilter='DC').data
    print(colored('File Read: %s' %(file1.replace(dir1,'')),'yellow'))
    ''' add stuff in for storing to netcdf '''
    return h1

def fc(queue):
    while True:
        if os.path.exists(dir + 'test_data.%0.3i' %(a)):
            print(colored(a,'red'))
            h1 = gui_data()
            queue.put(a,h1)
            time.sleep(1.0)
            Time_Keeper().plus_one()
        else :
            print(colored('No Matching Files','red'))
            queue.put(a,'done')

class Time_Keeper:
    def plus_one(self):
        global a
        a = a + 1
