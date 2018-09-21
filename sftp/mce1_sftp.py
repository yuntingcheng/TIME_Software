import os
import subprocess
import time
import shutil
import sys
import datetime as dt

def main():
    dir = '/data/cryo/current_data/'
    print '------- Starting Data Transfer -------'
    a = 0
    begin = dt.datetime.utcnow()
    end = dt.datetime.utcnow()
    while end - begin < dt.timedelta(seconds=5):
        if os.path.exists("/data/cryo/current_data/temp.%0.3i" %(a+1)) :
            mce_file_name = '/data/cryo/current_data/temp.%0.3i' %(a)
            if a == 0:
                subprocess.call(['scp', '/data/cryo/current_data/temp.run', 'time@time-master.caltech.edu:/home/time/Desktop/time-data/mce1/temp.run'])
                #subprocess.Popen(['rm %s' % ('/data/cryo/current_data/temp.run')],shell=True)
            if os.path.exists(mce_file_name):
                subprocess.call(['scp', mce_file_name, 'time@time-master.caltech.edu:/home/time/Desktop/time-data/mce1/temp.%0.3i' % (a)])
                subprocess.Popen(['rm %s' % (mce_file_name)],shell=True)
                print 'File Transfered :' , mce_file_name.replace(dir,'')
                a += 1
                begin = dt.datetime.utcnow()

            else :
                print "File Doesn't Exist"
        end = dt.datetime.utcnow()
    else :
        print 'File Transfer Stopped'
        #subprocess.Popen(['rm temp*'],shell=True)
        #subprocess.Popen(['rm /data/cryo/current_data/temp*'],shell=True)
        subprocess.Popen(['ssh -T time@time-master.caltech.edu pkill -f /home/time/time-software/main/read_files.py'])
        print 'File Read Stopped'
        sys.exit()

if __name__ == '__main__':
    main()
