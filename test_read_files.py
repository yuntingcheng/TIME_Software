import numpy as np
import os, sys, time, logging, mce_data, subprocess
import netcdf as nc
import datetime as dt
from termcolor import colored
#sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 1) # line buffering
mce = 0
filestarttime = 0
dir1 = '/Users/vlb9398/Desktop/test_mce_file_final'

def netcdfdata(a,rc,ch,row):
    mce_file1 = os.path.exists(dir1 + 'test_data.%0.3i' %(a))
    d1, graphdata1 = readdata(f1, mce_file1, rc, ch, row)
    print(colored('File Read: %s' %(mce_file1.replace(dir1,'')),'yellow'))
    return d1, graphdata1
# ===========================================================================================================================
def readdata(f1, mce_file1, rc, ch, row):
    h1 = f1.Read(row_col=True, unfilter='DC').data
    d1 = np.empty([h1.shape[0],h1.shape[1]],dtype=float)
    for b in range(h1.shape[0]):
        for c in range(h1.shape[1]):
            d1[b][c] = (np.std(h1[b][c][:],dtype=float))
    g1 = h1[:,ch - 1]
    array1 = []
    for j in range(g1.shape[1]):
        array1.append(g1[row - 1][j])
    graphdata1 = [a,ch,array1]
    subprocess.Popen(['rm %s' %(mce_file1)],shell=True)
    return d1, graphdata1
# =========================================================================================================
