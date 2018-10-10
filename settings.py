def mode_check(m):
    if m == False :
        print('mode check is called false')
        f = open('/home/pilot2/TIME_Software/tempfiles/data_send.txt','w')
        f.write('False')
        f.close()

    elif m == True :
        f = open('/home/pilot2/TIME_Software/tempfiles/data_send.txt','w')
        f.write('True')
        f.close()

    else :
        f = open('/home/pilot2/TIME_Software/tempfiles/data_send.txt','w')
        f.close()
