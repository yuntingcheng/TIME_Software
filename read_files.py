import numpy as np
import os, sys, time, logging, mce_data, subprocess
import netcdf as nc
import datetime as dt
from termcolor import colored
#sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 1) # line buffering

sys.path.append('/home/pilot1/TIME_Software')
def netcdfdata(rc,ch,row):
    print('Read files has started')
    sys.stdout.flush()
    a = 0
    mce = 0
    n = 0
    filestarttime = 0
    dir1 = '/home/pilot1/Desktop/time-data/mce1/'
    #dir2 = '/home/pilot1/Desktop/time-data/mce2/'

    while True:
        mce_file1 = os.path.exists(dir1 + 'temp.%0.3i' %(a+1))
        #mce_file2 = os.path.exists(dir2 + 'temp.%0.3i' %(a+1))
        #if (mce_file1 and mce_file2):
        if mce_file1 :
            files1 = [dir1 + x for x in os.listdir(dir1) if (x.startswith("temp") and not x.endswith('.run'))]
            print(colored('First if statement passed'))
            sys.stdout.flush()
            #files2 = [dir2 + x for x in os.listdir(dir2) if (x.startswith("temp") and not x.endswith('.run'))]
            # if (len(files1) and len(files2)) != 0:
            if len(files1) != 0:
                mce_file1 = min(files1, key = os.path.getctime)
                print(colored('Second if statement passed'))
                sys.stdout.flush()
                #mce_file2 = min(files2, key = os.path.getctime)
                f1 = mce_data.SmallMCEFile(mce_file1)
                #f2 = mce_data.SmallMCEFile(mce_file2)
                head1 = read_header(f1)
                #head2 = read_header(f2)
                #++++++++++++++++++++++++++++++++ TELESCOPE DATA +++++++++++++++++++++++++++++++++++++++++++++++++++
                # pa,slew_flag,alt,az,ra,dec = np.loadtxt('tempfiles/tempteledata.txt',delimiter = ',',unpack=True)
                # t = open('tempfiles/tempteledata.txt','w')
                # t.close()
                # tel_size = len(pa)
                # tt = np.column_stack((pa,slew_flag,alt,az,ra,dec))
                #print(tt.shape)
                #print(tt)
                #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                mce, n, filestarttime, d1, graphdata1 = readdata(f1, mce_file1, mce, head1, n, a, filestarttime, rc, ch, row)
                #mce, n, filestarttime, tel_size, tt = readdata(f, mce_file, mce, header, n, a, filestarttime, rc, tel_size, tt)
                #mce,n,filestarttime,d1,d2,graphdata1,graphdata2 = readdata(f1,f2,mce_file1,mce_file2,mce,head1,head2,n,a,filestarttime,rc,ch,row)
                # print(colored('File Read: %s , %s' %(mce_file1.replace(dir,''),mce_file2.replace(dir,''))),'yellow')
                print(colored('File Read: %s' %(mce_file1.replace(dir1,'')),'yellow'))
                a = a + 1
                sys.stdout.flush()
            break
        else :
            pass
    print(colored(graphdata1,'red'))
    return d1, graphdata1, mce
    #return d1, d2, graphdata1, graphdata2, mce
# ===========================================================================================================================
#def readdata(f1, f2, mce_file1, mce_file2, mce, head1, head2, n, a, filestarttime, rc, ch, row):
def readdata(f1, mce_file1, mce, head1, n, a, filestarttime, rc, ch, row):
    h1 = f1.Read(row_col=True, unfilter='DC').data
    #h2 = f2.Read(row_col=True, unfilter='DC').data
    d1 = np.empty([h1.shape[0],h1.shape[1]],dtype=float)
    for b in range(h1.shape[0]):
        for c in range(h1.shape[1]):
            d1[b][c] = (np.std(h1[b][c][:],dtype=float))
    # d2 = np.empty([h2.shape[0],h2.shape[1]],dtype=float)
    # for b in range(h1.shape[0]):
    #     for c in range(h1.shape[1]):
    #         d2[b][c] = (np.std(h2[b][c][:],dtype=float))

    g1 = h1[:,ch - 1]# + ((rc-1) * 8) - 1]
    #g2 = h2[:,ch - 1]
    array1 = []
    for j in range(g1.shape[1]):
        array1.append(g1[row - 1][j])
        #array2.append(g2[row - 1][j])
    graphdata1 = [a,ch,array1]
    #graphdata2 = [a,ch,array2]

    subprocess.Popen(['rm %s' % (mce_file1)], shell=True)
    #subprocess.Popen(['rm %s' % (mce_file2)], shell=True)
    netcdfdir = '/home/pilot1/Desktop/time-data/netcdffiles'

    if n == 0:
        filestarttime = dt.datetime.utcnow()
        filestarttime = filestarttime.isoformat()
        print('------------ New File -------------')
        #mce = nc.new_file(h1.shape, head1, head2, filestarttime)
        mce = nc.new_file(h1.shape, head1, filestarttime)
        if rc == 's' :
            #nc.data_all(h1,h2,n,head1,head2,filestarttime)
            nc.data_all(h1,n,head1,filestarttime)
        else :
            #nc.data(h1,h2,n,head1,head2,filestarttime)
            nc.data(h1,n,head1,filestarttime)

    elif os.stat(netcdfdir + "/raw_%s.nc" % (filestarttime)).st_size >= 20 * 10**6:
        n = 0
        print('----------- New File ------------')
        filestarttime = datetime.datetime.utcnow()
        filestarttime = filestarttime.isoformat()
        #mce = nc.new_file(h1.shape, head1, head2, filestarttime)
        mce = nc.new_file(h1.shape, head1, filestarttime)
        if rc == 's' :
            #nc.data_all(h1,h2,n,head1,head2,filestarttime)
            nc.data_all(h1,n,head1,filestarttime)
        else :
            #nc.data(h1,h2,n,head1,head2,filestarttime)
            nc.data(h1,n,head1,filestarttime)

    else:
        if rc == 's' :
            #nc.data_all(h1,h2,n,head1,head2,filestarttime)
            nc.data_all(h1,n,head1,filestarttime)
        else :
            #nc.data(h1,h2,n,head1,head2,filestarttime)
            nc.data(h1,n,head1,filestarttime)
    n = n + 1
    #return mce, n, filestarttime, d1, d2, graphdata1, graphdata2
    return mce, n, filestarttime, d1, graphdata1

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
                    print("I don't know what I am...")
            value = ''.join(map(str,value))
        value = int(value)
        values.append(value)
    values = np.asarray(values)
    return values

# if __name__ == '__main__':
