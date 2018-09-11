from netCDF4 import Dataset
from netCDF4 import MFDataset
import os
import sys
#import takedata_test as td
import datetime as now
from netCDF4 import num2date, date2num

#from multipagegui import parameters


def new_file(n, h_size, head, filestarttime):
    tempfiledir = os.path.expanduser('/home/time/Desktop/time-data/netcdffiles')
    mce = Dataset(tempfiledir + "/mce1_%s.nc" %(filestarttime),"w",format="NETCDF4")

    # create the gui parameters group
    guiparams = mce.createGroup('guiparams')
    stream = mce.createGroup('stream')
    heatmap = mce.createGroup('heatmap')
    mce_header = mce.createGroup('mce_header')

     # GUI PARAMETERS ---------------------------------------------------------------------------------
    guiparams.createDimension('det',1)
    guiparams.createDimension('obs',1)
    guiparams.createDimension('date',1)
    guiparams.createDimension('f',1)
    guiparams.createDimension('mode',1)
    guiparams.createDimension('r',1)
    guiparams.createDimension('t',None)
    # Dimensions for Data Arrays -------------------------------------------------------------------
    stream.createDimension('raw_rows',h_size[0])
    stream.createDimension('raw_cols',8)
    stream.createDimension('raw_cols_all',32)
    stream.createDimension('raw_num', h_size[2])
    stream.createDimension('t',None)

    heatmap.createDimension('rms_rows',h_size[0])
    heatmap.createDimension('rms_cols',8)
    heatmap.createDimension('rms_cols_all',32)
    heatmap.createDimension('t',None)

    mce_header.createDimension('k',2)
    mce_header.createDimension('v',16)
    mce_header.createDimension('t',None)

    # creating variables --------------------------------------------------------------------------------
    Observer = guiparams.createVariable("observer","S3","obs")
    Datetime = guiparams.createVariable('datetime', 'S26','date')
    Frames = guiparams.createVariable('frames', 'S8','f')
    Datamode = guiparams.createVariable('datamode','S2','mode')
    Detector = guiparams.createVariable('detector','f8','det')
    Rc = guiparams.createVariable('rc','S1','r') # can either use rc name or integer used by gui
    global Time
    Time = guiparams.createVariable('time','S26','t')

    global Rms_Noise_All
    global Rms_Noise
    Rms_Noise_All = heatmap.createVariable('rms_noise_all','f8',('t','rms_rows','rms_cols_all'))
    Rms_Noise = heatmap.createVariable('rms_noise','f8',('t','rms_rows','rms_cols'))

    global Raw_Data_All
    global Raw_Data
    Raw_Data = stream.createVariable('raw_data','f8',('t','raw_rows','raw_cols','raw_num'))
    Raw_Data_All = stream.createVariable('raw_data_all','f8',('t','raw_rows','raw_cols_all','raw_num'))

    global Header
    Header = mce_header.createVariable('header','S3',('t','v','k'))


    parafilename = ('tempfiles/tempparameters.txt')
    parafile = open(parafilename, 'r')
    parameters = parafile.readline().strip().split()
    Observer[0] = parameters[0]
    Frames[0] = parameters[3]
    #Datetime[0] = parameters[6]
    Datamode[0] = parameters[1]
    Rc[0] = parameters[2]
    parafile.close()

    return mce

def data_all(h,d,n,a,head):
    Time[a] = str(now.datetime.utcnow())
    #Rms_Noise_All[a,:,:] = d
    Raw_Data_All[a,:,:,:] = h
    Header[a,:,:] = head

def data(h,d,n,a,head):
    Time[a] = str(now.datetime.utcnow())
    #Rms_Noise[a,:,:] = d
    Raw_Data[a,:,:,:] = h
    Header[a,:,:] = head
