import numpy as np
import os, sys, time, logging, mce_data, subprocess
import netcdf as nc
import datetime as dt
from termcolor import colored
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 1) # line buffering

sys.path.append('/home/pilot1/TIME_Software')
def netcdfdata(rc,ch,row):
    a = 0
    mce = 0
    n = 0
    filestarttime = 0
    dir1 = '/home/pilot1/Desktop/time-data/mce1/'
    dir2 = '/home/pilot1/Desktop/time-data/mce2/'

    begin = dt.datetime.utcnow()
    end = dt.datetime.utcnow()
    while end - begin < dt.timedelta(seconds=5):
        mce_file1 = os.path.exists(dir1 + 'temp.%0.3i' %(a+1))
        mce_file2 = os.path.exists(dir2 + 'temp.%0.3i' %(a+1))
        if (mce_file1 and mce_file2):
            files1 = [dir1 + x for x in os.listdir(dir1) if (x.startswith("temp") and not x.endswith('.run'))]
            files2 = [dir2 + x for x in os.listdir(dir2) if (x.startswith("temp") and not x.endswith('.run'))]
            if (len(files1) and len(files2) != 0:
                mce_file1 = min(files1, key = os.path.getctime)
                mce_file2 = min(files2, key = os.path.getctime)
                f1 = mce_data.SmallMCEFile(mce_file1)
                f2 = mce_data.SmallMCEFile(mce_file2)
                head1 = read_header(f1)
                head2 = read_header(f2)
                #++++++++++++++++++++++++++++++++ TELESCOPE DATA +++++++++++++++++++++++++++++++++++++++++++++++++++
                # pa,slew_flag,alt,az,ra,dec = np.loadtxt('tempfiles/tempteledata.txt',delimiter = ',',unpack=True)
                # t = open('tempfiles/tempteledata.txt','w')
                # t.close()
                # tel_size = len(pa)
                # tt = np.column_stack((pa,slew_flag,alt,az,ra,dec))
                #print(tt.shape)
                #print(tt)
                #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                #mce, n, filestarttime, tel_size, tt = readdata(f, mce_file, mce, header, n, a, filestarttime, rc, tel_size, tt)
                mce,n,filestarttime,d1,d2,graphdata1,graphdata2 = readdata(f1,f2,mce_file1,mce_file2,mce,head1,head2,n,a,filestarttime,rc,ch,row)
                print(colored('File Read: %s , %s' %(mce_file1.replace(dir,''),mce_file2.replace(dir,''))),'yellow')
                a = a + 1
            begin = dt.datetime.utcnow()
        end = dt.datetime.utcnow()
    return d1, d2, graphdata1, graphdata2, mce

    else :
        print(colored('No more files!', 'red'))
        subprocess.Popen(['rm /home/pilot1/Desktop/time_data/mce1/temp*'],shell=True)
        subprocess.Popen(['rm /home/pilot1/Desktop/time_data/mce2/temp*'],shell=True)
        #subprocess.Popen(['pkill -9 -f readteledata.py'],shell=True)
        #subprocess.Popen(['ssh -T pilot2@timemce.rit.edu pkill -9 -f tel_sock.py'],shell=True)
        #subprocess.Popen(['/home/pilot1/anaconda3/bin/python /home/pilot1/TIME_Software/stop_server.py'],shell=True)
        #print('Tel Server Stopped')
        #subprocess.Popen(['ssh -T pilot2@timemce.rit.edu /home/pilot2/anaconda3/bin/python /home/pilot2/TIME_Software/stop_client.py'],shell=True)
        #print('Tel Client Stopped')
        sys.exit()

# ===========================================================================================================================
def readdata(f1, f2, mce_file1, mce_file2, mce, head1, head2, n, a, filestarttime, rc, ch, row):
    h1 = f1.Read(row_col=True, unfilter='DC').data
    h2 = f2.Read(row_col=True, unfilter='DC').data
    d1 = np.empty([h1.shape[0],h1.shape[1]],dtype=float)
    for b in range(h1.shape[0]):
        for c in range(h1.shape[1]):
            d1[b][c] = (np.std(h1[b][c][:],dtype=float))
    d2 = np.empty([h2.shape[0],h2.shape[1]],dtype=float)
    for b in range(h1.shape[0]):
        for c in range(h1.shape[1]):
            d2[b][c] = (np.std(h2[b][c][:],dtype=float))

    g1 = h1[:,ch - 1]# + ((rc-1) * 8) - 1]
    g2 = h2[:,ch - 1]
    array1 = []
    for j in range(g1.shape[1]):
        array1.append(g1[row - 1][j])
        array2.append(g2[row - 1][j])
    graphdata1 = [a,ch,array1]
    graphdata2 = [a,ch,array2]

    subprocess.Popen(['rm %s' % (mce_file1)], shell=True)
    subprocess.Popen(['rm %s' % (mce_file2)], shell=True)
    netcdfdir = '/home/pilot1/Desktop/time-data/netcdffiles'

    if n == 0:
        filestarttime = datetime.datetime.utcnow()
        filestarttime = filestarttime.isoformat()
        print('------------ New File -------------')
        mce = nc.new_file(h1.shape, head1, head2, filestarttime)
        if rc == 's' :
            nc.data_all(h1,h2,n,head1,head2,filestarttime)
        else :
            nc.data(h1,h2,n,head1,head2,filestarttime)

    elif os.stat(netcdfdir + "/mce1_%s.nc" % (filestarttime)).st_size >= 20 * 10**6:
        n = 0
        print('----------- New File ------------')
        filestarttime = datetime.datetime.utcnow()
        filestarttime = filestarttime.isoformat()
        mce = nc.new_file(h1.shape, head1, head2, filestarttime)
        if rc == 's' :
            nc.data_all(h1,h2,n,head1,head2,filestarttime)
        else :
            nc.data(h1,h2,n,head1,head2,filestarttime)

    else:
        if rc == 's' :
            nc.data_all(h1,h2,n,head1,head2,filestarttime)
        else :
            nc.data(h1,h2,n,head1,head2,filestarttime)
    n = n + 1
    return mce, n, filestarttime, d1, d2, graphdata1, graphdata2

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
    return head

if __name__ == '__main__':
    netcdfdata(sys.argv[1],sys.argv[2],sys.argv[3])
