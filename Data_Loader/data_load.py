# let's the user choose which data to pull out of which files
from netCDF4 import Dataset
from netCDF4 import MFDataset
import sys

def all_files(file,group,var):
    f = MFDataset(file,'r')

    s = f.groups[group]
    t = s.variables[var][:]
    print(t[0:10])

    print("Do you need to load another dataset?")
    action3 = input('y : yes , n : no \n')
    if action3 == 'y':
        file_keys(file,num='all')
    else :
        print("Have a nice day")

def one_file(file,group,var):
    f = Dataset(file[0],'r')

    s = f.groups[group]
    t = s.variables[var][:]
    print(t[0:10])

    print("Do you need to load another dataset?")
    action4 = input('y : yes , n : no \n')
    if action4 == 'y':
        file_keys(file,num='one')
    else :
        print("Have a nice day")

def file_keys(file,num):
    print(file[0])
    f = Dataset(file[0],'r')

    print("Group Keys:")
    print(f.groups.keys())
    action = input("Pick a GROUP \n")

    print("Variable Keys:")
    print(f.groups[action].variables.keys())
    action1 = input("Pick a VARIABLE \n")

    v = f.groups[action]
    print("================================")
    print("Meta Data for {group}".format(group=action))
    print(v)
    print("================================")
    print("================================")
    print("Meta Data for {var}".format(var = action1))
    print(v.variables[action1])
    print("================================")

    if num == 'one':
        one_file(file,action,action1)
    else :
        all_files(file,action,action1)
#------------------------------------------------------------------------------
