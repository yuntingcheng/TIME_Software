# let's the user choose which data to pull out of which files
from netCDF4 import Dataset
from netCDF4 import MFDataset
import sys

def all_files(file,var):
    f = MFDataset(file,'r')
    t = f.variables[var][:]
    print(t[:])

    print("Do you need to load another dataset?")
    action3 = input('y : yes , n : no \n')
    if action3 == 'y':
        file_keys(file,num='all')
    else :
        print("Have a nice day")

def one_file(file,var):
    f = Dataset(file[0],'r')
    t = f.variables[var][:]
    print(t[:])

    print("Do you need to load another dataset?")
    action4 = input('y : yes , n : no \n')
    if action4 == 'y':
        file_keys(file,num='one')
    else :
        print("Have a nice day")

def file_keys(file,num):
    print(file[0])
    f = Dataset(file[0],'r')

    print("Variable Keys:")
    print(f.variables.keys())
    action = input("Pick a VARIABLE \n")

    print("================================")
    print("Meta Data for {var}".format(var = action))
    print(f.variables[action])
    print("================================")

    if num == 'one':
        one_file(file,action)
    else :
        all_files(file,action)
#------------------------------------------------------------------------------
