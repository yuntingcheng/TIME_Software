import numpy as np
from os import stat
import os
import sys
import mce_data
import netcdf as nc
import subprocess
import datetime
import time

def netcdfdata(rc):
    print '------ Data Parsing ------'
    a = 0
    n = 0
    filestarttime = datetime.datetime.utcnow()
    filestarttime = filestarttime.isoformat()
    dir = '/home/time/Desktop/time-data/mce1/'
    mce = 0
    subprocess.call(['ssh -T time@time-mce-1.caltech.edu python /home/time/time-software/sftp/mce1_sftp.py'], shell=True)
    while True:
        files = [dir + x for x in os.listdir(dir) if (x.startswith("temp") and not x.endswith('.run'))]
        if len(files) != 0 :
            mce_file = min(files, key = os.path.getctime)
            f = mce_data.SmallMCEFile(mce_file)
            head = read_header(f)
            filestarttime, mce = readdata(f,head,filestarttime,rc,mce_file,a,mce,n)
            print 'File Read:' , mce_file.replace(dir,'')
        else :
            print 'No More Files'
            subprocess.Popen(['rm /home/time/Desktop/time-data/mce1/temp.run'], shell=True)
            sys.exit()

# ===========================================================================================================================
def readdata(f,head,filestarttime,rc,mce_file,a,mce,n):
    h = f.Read(row_col=True, unfilter='DC').data
    # d = np.empty([h.shape[0],h.shape[1]],dtype=float)
    # for b in range(h.shape[0]):
    #     for c in range(h.shape[1]):
    #         d[b][c] = (np.std(h[b][c][:],dtype=float))

    subprocess.Popen(['rm %s' % (mce_file)], shell=True)

    netcdfdir = '/home/time/Desktop/time-data/netcdffiles'
    #if a == 0 or os.stat(netcdfdir + "/mce1_%s.nc" % (filestarttime)).st_size >= 20 * 10**6 :
    if n == 0:
        print '----------New File----------'
        filestarttime = datetime.datetime.utcnow()
        filestarttime = filestarttime.isoformat()
        nc.new_file(h.shape, head, filestarttime)

    elif n == 10 :
        n = 0
        print '----------New File----------'
        filestarttime = datetime.datetime.utcnow()
        filestarttime = filestarttime.isoformat()
        nc.new_file(h.shape, head, filestarttime)

    if rc == 's' :
        nc.data_all(h,a,head,filestarttime)
    else :
        nc.data(h,a,head,filestarttime)
    n = n + 1
    a = a + 1
    return filestarttime, mce
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
