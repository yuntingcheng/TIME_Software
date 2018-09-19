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
    filestarttime = 0
    dir = '/home/time/Desktop/time-data/mce1/'
    mce = 0
    subprocess.call(['ssh -T time@time-mce-1.caltech.edu python /home/time/time-software/sftp/mce1_sftp.py'], shell=True)
    while True:
        files = [dir + x for x in os.listdir(dir) if (x.startswith("temp") and not x.endswith('.run'))]
        if len(files) != 0:
            print 'I found a file...'
        mce_file = min(files, key = os.path.getctime)
        f = mce_data.SmallMCEFile(mce_file)
        head = read_header(f)
        readdata(f,head,filestarttime,rc,mce_file,a)
        a = a + 1
        print 'File Read:' , mce_file.replace(dir,'')
#-----------------------------------------------------------------------------------------------
        # mce_file = os.path.exists('/home/time/Desktop/time-data/mce1/temp.%0.3i' %(a+1))
        # #print('/home/time/Desktop/time-data/mce1/temp.%0.3i' %(a+1))
        # if mce_file:
        #     print(len(os.listdir("/home/time/Desktop/time-data/mce1")) - 2)
        #     for i in range(len(os.listdir("/home/time/Desktop/time-data/mce1")) - 2):
        #         mce_file_name = '/home/time/Desktop/time-data/mce1/temp.%0.3i' %(a)
        #         a = a + 1
        #         f = mce_data.SmallMCEFile(mce_file_name)
        #         header = read_header(f)
        #         mce, filestarttime = readdata(f, mce, header, a, filestarttime, rc)
        #         print('File Read:' , mce_file_name.replace(dir,''))
        #         begin = dt.datetime.now()
                #mce_file = os.path.exists('/home/time/Desktop/time-data/mce1/temp.%0.3i' %(a+1))

    else :
        print 'Read Files Stopped'
        sys.exit()

# ===========================================================================================================================
def readdata(f,head,filestarttime, rc, mce_file,a):
    h = f.Read(row_col=True, unfilter='DC').data
    # d = np.empty([h.shape[0],h.shape[1]],dtype=float)
    # print("++++++++ H Array ++++++++")
    # print(h[0][0][:])
    # print("+++++++++++++++++++++++++")
    # for b in range(h.shape[0]):
    #     for c in range(h.shape[1]):
    #         d[b][c] = (np.std(h[b][c][:],dtype=float))
    #print h.shape

    #old_mce_file_name = '/home/time/Desktop/time-data/mce1/temp.%0.3i' %(a - 1)
    subprocess.Popen(['rm %s' % (mce_file)], shell=True)

    netcdfdir = os.path.expanduser('/home/time/Desktop/time-data/netcdffiles')
    if a == 0:
        filestarttime = datetime.datetime.utcnow()
        filestarttime = filestarttime.isoformat()
        mce = nc.new_file(h.shape, head, filestarttime)
    elif os.stat(netcdfdir + "/mce1_%s.nc" % (filestarttime)).st_size < 20 * 10**6: # of bytes here
        if os.path.exists('/home/time/Desktop/time-data/netcdffiles/mce1_%s.nc' %(filestarttime)) :
            if rc == 's' :
                nc.data_all(h,a,head)
            else :
                nc.data(h,a,head)
    else:
        mce.close()
        print '----------New File----------'
        filestarttime = datetime.datetime.utcnow()
        filestarttime = filestarttime.isoformat()
        mce = nc.new_file(h.shape, head, filestarttime)
        if os.path.exists('/home/time/Desktop/time-data/netcdffiles/mce1_%s.nc' %(filestarttime)) :
            if rc == 's' :
                nc.data_all(h,a,head)
            else :
                nc.data(h,a,head)
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
    # print("+++++++++ MCE HEADER +++++++++")
    # print(head)
    # print("++++++++++++++++++++++++++++++")
    return head

if __name__ == '__main__':
    netcdfdata(sys.argv[1])
