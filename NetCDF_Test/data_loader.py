from __future__ import division, print_function

import numpy as np
import matplotlib.pyplot as plt
import datetime

# This is just an idea of the type of workflow we are looking for.
# Imagine this script as being the start of a higher-level data analysis
# script, perhaps processing lab testing data.  The "DataLoader" class I
# reference is what I would receive from you.  These are just ideas,
# you don't need to match anything exactly.

from time_analysis.data_loader import DataLoader


# I create an instance of the data loader and point it to the master
# directory full of all of the data files.  No data is actually loaded
# at this point (always assume there is years worth of data, so we can't
# load it all)
dl = DataLoader(basefolder='/data/netcdf/')

# Even better, I point it to a directory on a remote machine (so I can
# run scripts from my personal computer instead of always on time-master).
# We can add this later.
dl = DataLoader(basefolder='time@time-master.caltech.edu:/data/netcdf/', remote=True)

t0 = datetime.datetime(2018,07,21,14,10,0)
t1 = datetime.datetime(2018,07,22,1,1,0)

# Loads in all data between times t0 and t1.
data = dl.load(t0, t1)

# I am assuming there are 33 mux rows, 32 mux columns, and 2 MCEs,
# giving 2112 total detectors. There are T=?? frames in the data.
#
# "data" is now a dictionary with the following structure
# 	data['time'] = array of shape (T) with the frame times (datetime objects?)
#	data['det'] = array of shape (2112,T) with the detector timestreams
# 	data['hk'] = (Can be added later, we will use the exisiting HK
#				 data systems for now)
#				 Probably a dictionary or something, I might want to
#				 do something like data['hk']['temperature']['1K Pot']
#			     and get a sparse array of 1K pot temperatures
#	data['tel'] = (Can be added later) telescope data of some sort
#	data['flags'] = (Can be added later, this is just an idea.)
#					Dictionary of flags, each with a True/False value for each frame.
#					For example, data['flags']['fts'] is an array of
#					shape (T) full of booleans/bits telling me if FTS
#					was running for this frame.  If we store a 128 bit
#					number with each frame, we would get 128 flags that
#					we can name whatever we choose in software
#					("cold_fridge", "fts_wlf", "on_sky", etc)
#					The data collator would keep track of the state of
#					some of the defined flags and store them as data is
#					written, while other flags could be set in post-processing.
#					We should work in plenty of extra unused flags or
#					have a way to add new flags without breaking old files.


# Everything below this point can be future expansion.  We really only
# need "dl.load(t0, t1)" to start getting things working.
#=============================================================================
'''
Data Analysis Scripts
(Do some processing, make some plots, etc)
'''
#=============================================================================
t0 = datetime.datetime(2018,07,20,14,10,0)
t1 = datetime.datetime(2018,07,23,1,1,0)

# Loads in all data between times t0 and t1 where the fts flag is set.
# When I did the FTS measurement, I ran a script that told the data collator
# to set the FTS flag for a certain amount of time.  I know I took FTS
# data in the last couple days, but I forget when exactly, so I give it a
# broad range and tell it to only give me the flagged data.  Perhaps the
# loader can be smart about memory usage to avoid loading the whole
# range of data at once?
data = dl.load(t0, t1, flag='fts')

#=============================================================================
'''
Data Analysis Scripts
(Do some processing, make some plots, etc)
'''
#=============================================================================

t0 = datetime.datetime(2018,07,21,14,10,0)
t1 = datetime.datetime(2018,07,22,1,1,0)

# Load in part of the data in a different way.
t, d = dl.load(t0, t1, fields=['time', 'det'])

# t = array of shape (T) with the frame times (datetime objects?)
# d = array of shape (2112,T) with the detector timestreams

#=============================================================================
'''
Data Analysis Scripts
(Do some processing, make some plots, etc)
'''
#=============================================================================
