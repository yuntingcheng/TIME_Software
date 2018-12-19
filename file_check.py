from test_read_files import Read_Files
import os
def fc(queue) :
    dir = '/Users/vlb9398/Desktop/test_mce_files/'
    while True:
        if os.path.exists(dir + 'test_data.%0.3i' %(a)):
            print(colored(a,'red'))
            z1, graphdata1 = rf.netcdfdata()
            queue.put(a)
            time.sleep(1.0)
        else :
            print(colored('No Matching Files','red'))
