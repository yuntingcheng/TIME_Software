from netCDF4 import Dataset
from netCDF4 import MFDataset
import os
import sys
#import takedata_test as td
import datetime as now
from netCDF4 import num2date, date2num


tempfiledir = '/home/time/Desktop/time-data/netcdffiles'
def new_file(h_size, head, filestarttime):
    mce = Dataset(tempfiledir + "/mce1_%s.nc" %(filestarttime),"w",format="NETCDF4_CLASSIC")

    # create the gui parameters group
    # guiparams = mce.createGroup('guiparams')
    # stream = mce.createGroup('stream')
    # heatmap = mce.createGroup('heatmap')
    # mce_header = mce.createGroup('mce_header')

     # GUI PARAMETERS ---------------------------------------------------------------------------------
    mce.createDimension('det',1)
    mce.createDimension('obs',1)
    mce.createDimension('date',1)
    mce.createDimension('f',1)
    mce.createDimension('mode',1)
    mce.createDimension('r',1)
    mce.createDimension('t',None)
    # Dimensions for Data Arrays -------------------------------------------------------------------
    mce.createDimension('raw_rows',h_size[0])
    mce.createDimension('raw_cols',8)
    mce.createDimension('raw_cols_all',32)
    mce.createDimension('raw_num', h_size[2])
    mce.createDimension('k',2)
    mce.createDimension('v',16)


    # creating variables --------------------------------------------------------------------------------
    Observer = createVariable("observer","S3","obs")
    Datetime = createVariable('datetime', 'S26','date')
    Frames = createVariable('frames', 'S8','f')
    Datamode = createVariable('datamode','S2','mode')
    Detector = createVariable('detector','f8','det')
    Rc = createVariable('rc','S1','r') # can either use rc name or integer used by gui
    global Time
    Time = createVariable('time','S26','t')

    global Rms_Noise_All
    global Rms_Noise
    Rms_Noise_All = createVariable('rms_noise_all','f8',('t','rms_rows','rms_cols_all'))
    Rms_Noise = createVariable('rms_noise','f8',('t','rms_rows','rms_cols'))

    global Raw_Data_All
    global Raw_Data
    Raw_Data = createVariable('raw_data','f8',('t','raw_rows','raw_cols','raw_num'))
    Raw_Data_All = createVariable('raw_data_all','f8',('t','raw_rows','raw_cols_all','raw_num'))

    global Header
    Header = createVariable('header','S3',('t','v','k'))

    parafilename = ('tempfiles/tempparameters.txt')
    parafile = open(parafilename, 'r')
    parameters = parafile.readline().strip().split()
    Observer[0] = parameters[0]
    Frames[0] = parameters[3]
    Datamode[0] = parameters[1]
    Rc[0] = parameters[2]
    parafile.close()

    mce.close()
    return mce

def data_all(h,a,head,filestarttime):
    mce = Dataset(tempfiledir + "/mce1_%s.nc" %(filestarttime),"a")
    Time[a] = str(now.datetime.utcnow())
    Raw_Data_All[a,:,:,:] = h
    Header[a,:,:] = head
    mce.close()

def data(h,a,head,filestarttime):
    mce = Dataset(tempfiledir + "/mce1_%s.nc" %(filestarttime),"a")
    Time[a] = str(now.datetime.utcnow())
    Raw_Data[a,:,:,:] = h
    Header[a,:,:] = head
    mce.close()
