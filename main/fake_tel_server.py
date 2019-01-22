
import socket, struct, sys

MAC_PORT = 8888

# I am accepting telescope sim data for the gui

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('',MAC_PORT))
print('Server listening on port %i' %(MAC_PORT))
s.listen(5)
unpacker = struct.Struct('d d d d d d d')
client, info = s.accept()
while True:
    data = client.recv(unpacker.size)
    pa,slew_flag,alt,az,ra,dec,time = unpacker.unpack(data)
    print('Data Received')
    print(pa,time)

    if KeyboardInterrupt:
        False
        s.close()
        sys.exit()
