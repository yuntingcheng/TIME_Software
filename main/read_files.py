import numpy as np
from os import stat
import os
import sys
import mce_data
import netcdf as nc
import subprocess
import datetime
import time
import logging
import settings as st

def netcdfdata(rc):
    a = 0
    mce = 0
    n = 0
    filestarttime = 0
    dir = '/home/time/Desktop/time-data/mce1/'
    subprocess.Popen(['ssh -T time@time-mce-1.caltech.edu python /home/time/time-software/sftp/mce1_sftp.py'], shell=True)
    begin = dt.datetime.utcnow()
    end = dt.datetime.utcnow()
    while end - begin < dt.timedelta(seconds=5):
        mce_file = os.path.exists('/home/time/Desktop/time-data/mce1/temp.%0.3i' %(a+1))
        print('/home/time/Desktop/time-data/mce1/temp.%0.3i' %(a+1))
        if mce_file:
            for i in range(len(os.listdir("/home/time/Desktop/time-data/mce1")) - 2):
                mce_file_name = '/home/time/Desktop/time-data/mce1/temp.%0.3i' %(a)
                a = a + 1
                f = mce_data.SmallMCEFile(mce_file_name)
                header = read_header(f)
                mce, n, filestarttime = readdata(f, mce_file_name, mce, header, n, a, filestarttime, rc)
                mce_file = os.path.exists('/home/time/Desktop/time-data/mce1/temp.%0.3i' %(a+1))
                print 'File Read: %s' %(mce_file_name.replace(dir,''))
                begin = dt.datetime.utcnow()
            end = dt.datetime.utcnow()
    else :
        print 'No More Files'
        subprocess.Popen(['rm /home/time/Desktop/time-data/mce1/temp.run'], shell=True)
        sys.exit()

# ===========================================================================================================================
def readdata(f, mce_file_name, mce, head, n, a, filestarttime, rc):
    h = f.Read(row_col=True, unfilter='DC').data
    # d = np.empty([h.shape[0],h.shape[1]],dtype=float)
    # for b in range(h.shape[0]):
    #     for c in range(h.shape[1]):
    #         d[b][c] = (np.std(h[b][c][:],dtype=float))
    old_mce_file_name = '/home/time/Desktop/time-data/mce1/temp.%0.3i' %(a - 1)
    subprocess.Popen(['rm %s' % (old_mce_file_name)], shell=True)
    netcdfdir = '/home/time/Desktop/time-data/netcdffiles'

    if n == 0:
        filestarttime = datetime.datetime.utcnow()
        filestarttime = filestarttime.isoformat()
        mce = nc.new_file(h.shape, head, filestarttime)
        if rc == 's' :
            nc.data_all(h,n,head,filestarttime)
        else :
            nc.data(h,n,head,filestarttime)
        n = n + 1
    elif os.stat(netcdfdir + "/mce1_%s.nc" % (filestarttime)).st_size < 20 * 10**6: # of bytes here
        if rc == 's' :
            nc.data_all(h,n,head,filestarttime)
        else :
            nc.data(h,n,head,filestarttime)
        n = n + 1
    else:
        n = 0
        print('----------New File----------')
        filestarttime = datetime.datetime.utcnow()
        filestarttime = filestarttime.isoformat()
        mce = nc.new_file(h.shape, head, filestarttime)
        if rc == 's' :
            nc.data_all(h,n,head,filestarttime)
        else :
            nc.data(h,n,head,filestarttime)
    return mce, n, filestarttime

# =========================================================================================================
def read_header(f):
    keys = []
    values = []
    for key,value in f.header.items():
        if key == '_rc_present':
            for i in range(len(value)):
                if value[i] == True:
                    value[i] = "1"
                elif value[i] == False:
                    value[i] = "0"
                else:
                    print "I don't know what I am..."
            value = ''.join(map(str,value))
        value = str(value)
        keys.append(key)
        values.append(value)
    keys = np.asarray(keys,dtype=object)
    values = np.asarray(values,dtype=object)
    head = np.array((keys,values)).T
    return head

if __name__ == '__main__':
    netcdfdata(sys.argv[1])
