import socket, struct, subprocess
from threading import Thread
import settings as st
import traceback

# I am accepting tel socket packets as server
tele = []
data_send = True

def main():
    PORT = 8888
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try :
        s.bind(('',PORT))
    except:
        print("Bind failed. Error : " + str(sys.exc_info()))
        sys.exit()
    s.listen(5)

    while True:
        # establish a connection with client
        client, info = s.accept()
        ip, port = str(info[0]), str(info[1])
        #lock acquired by client
        try :
            Thread(target=loop, args=(client, ip, port)).start()
            print('Connected to :', info[0], ':', info[1])
        except :
            print("Thread did not start.")
            traceback.print_exc()
    s.close()

def loop(client,ip,port):
    is_active = True
    while is_active :
        # data received from client
        unpacker = struct.Struct('d d d d d d d')
        data = client.recv(unpacker.size)
        pa,slew_flag,alt,az,ra,dec,time = unpacker.unpack(data)
        print('Tel Data Received')
        tempfilename = '/home/pilot1/TIME_Software/tempfiles/tempteledata.txt'
        f = open(tempfilename,'a')
        # write new data to file
        f.write("\n%.06f,%.06f,%.06f,%.06f,%.06f,%.06f" %(pa, slew_flag, alt, az, ra, dec))
        f.close()

        if st.status == False :
                print("Client is requesting to quit")
                client.close()
                print("Connection " + ip + ":" + port + " closed")
                is_active = False

    #print('Tel Server:',pa,slew_flag,alt,az,ra,dec)
if __name__=='__main__':
    main()
