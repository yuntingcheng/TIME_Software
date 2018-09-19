import os
import subprocess
import time
import shutil
import sys
import datetime as dt

def main():
    dir = '/data/cryo/current_data/'
    print('------- Starting Data Transfer -------')
    a = 0
    begintimer = dt.datetime.utcnow()
    while endtime - begintimer < dt.timedelta(seconds=5):
        if a == 0:
            subprocess.Popen(['scp', '/data/cryo/current_data/temp.run', 'time@time-master.caltech.edu:/home/time/Desktop/time-data/mce1/temp.run']).wait()
            subprocess.Popen(['rm %s' % ('/data/cryo/current_data/temp.run')],shell=True)
        if os.path.exists("/data/cryo/current_data/temp.%0.3i" %(a+1)) :
            mce_file_name = '/data/cryo/current_data/temp.%0.3i' %(a)
            if os.path.exists(mce_file_name):
                subprocess.Popen(['scp', mce_file_name, 'time@time-master.caltech.edu:/home/time/Desktop/time-data/mce1/temp.%0.3i' % (a)]).wait()
                subprocess.Popen(['rm %s' % (mce_file_name)],shell=True)
                print('File Transfered :' , mce_file_name.replace(dir,''))
                a += 1
                begintimer = dt.datetime.now()

            else :
                print("File Doesn't Exist")
        else :
            pass
    else :
        print('File Transfer Stopped')
        sys.exit()

if __name__ == '__main__':
    main()
