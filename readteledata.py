import socket, struct, subprocess
from _thread import *
import threading

# I am accepting tel socket packets as server
tele = []
print_lock = threading.Lock()

def main():
    PORT = 8555
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('',PORT))
    print('Server listening on port %i' %(PORT))
    s.listen(5)

    while True:
        # establish a connection with client
        client, info = s.accept()

        #lock acquired by client
        print_lock.acquire()
        print('Connected to :', info[0], ':', info[1])
        start_new_thread(loop,(client,))
        #loop(client,unpacker,data_recv,s)
    s.close()

def loop(client):
    while True :
        # data received from client
        unpacker = struct.Struct('d d d d d d d')
        data = client.recv(unpacker.size)
        if not data:
            print('Bye')
            # lock released on exit
            print_lock.release()
            break
        pa,slew_flag,alt,az,ra,dec,time = unpacker.unpack(data)
        tempfilename = '/home/pilot1/TIME_Software/tempfiles/tempteledata.txt'
        f = open(tempfilename,'a')
        # write new data to file
        f.write("\n%.06f,%.06f,%.06f,%.06f,%.06f,%.06f" %(pa, slew_flag, alt, az, ra, dec))
        f.close()
    # connection closed
    client.close()

    print('Tel Data Received')
    #print('Tel Server:',pa,slew_flag,alt,az,ra,dec)
if __name__=='__main__':
    main()
