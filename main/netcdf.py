import netCDF4 as nc
import os
import sys
#import takedata_test as td
import datetime as now
import numpy as np


tempfiledir = '/home/time/Desktop/time-data/netcdffiles'
def new_file(h_size, head, filestarttime):
    mce = nc.Dataset(tempfiledir + "/mce1_%s.nc" %(filestarttime),"w",format="NETCDF4_CLASSIC")

    # create the gui parameters group
    # guiparams = mce.createGroup('guiparams')
    # stream = mce.createGroup('stream')
    # heatmap = mce.createGroup('heatmap')
    # mce_header = mce.createGroup('mce_header')

     # GUI PARAMETERS ---------------------------------------------------------------------------------
    mce.createDimension('det',1)
    mce.createDimension('obs',3)
    mce.createDimension('date',26)
    mce.createDimension('f',8)
    mce.createDimension('mode',2)
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
    Observer = mce.createVariable("observer","S1",("obs",))
    Datetime = mce.createVariable('datetime', 'S1',('date',))
    Frames = mce.createVariable('frames', 'S1',('f',))
    Datamode = mce.createVariable('datamode','S1',('mode',))
    Detector = mce.createVariable('detector','f8',('det',))
    Rc = mce.createVariable('rc','S1',('r',)) # can either use rc name or integer used by gui
    global Time
    Time = mce.createVariable('time','S1',('t',))

    global Raw_Data_All
    global Raw_Data
    Raw_Data = mce.createVariable('raw_data','f8',('t','raw_rows','raw_cols','raw_num'))
    Raw_Data_All = mce.createVariable('raw_data_all','f8',('t','raw_rows','raw_cols_all','raw_num'))

    # global Header
    # Header = mce.createVariable('header','S3',('t','v','k'))

    parafilename = ('tempfiles/tempparameters.txt')
    parafile = open(parafilename, 'r')
    parameters = parafile.readline().strip().split()
    Observer[0] = nc.stringtochar(np.array([parameters[0]],dtype='S3').reshape((1,)))
    Frames[0] = nc.stringtochar(np.array([parameters[3]],dtype='S8').reshape((1,)))
    Datamode[0] = nc.stringtochar(np.array([parameters[1]],dtype='S2').reshape((1,)))
    Rc[0] = nc.stringtochar(np.array([parameters[2]],dtype='S1').reshape((1,)))
    parafile.close()

    mce.close()
    return mce

def data_all(h,a,head,filestarttime):
    mce = nc.Dataset(tempfiledir + "/mce1_%s.nc" %(filestarttime),"a")
    Time[a] = nc.stringtochar(np.array([str(now.datetime.utcnow())],dtype='S26').reshape((1,)))
    Raw_Data_All[a,:,:,:] = h
    #Header[a,:,:] = head
    mce.close()

def data(h,a,head,filestarttime):
    mce = nc.Dataset(tempfiledir + "/mce1_%s.nc" %(filestarttime),"a")
    Time[a] = nc.stringtochar(np.array([str(now.datetime.utcnow())],dtype='S26').reshape((1,)))
    Raw_Data[a,:,:,:] = h
    #Header[a,:,:] = head
    mce.close()
