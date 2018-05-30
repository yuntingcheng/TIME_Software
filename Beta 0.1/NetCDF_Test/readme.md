1.) Takedata_test.py is the file that must be run to read your data file and create
an example netcdf file.

2.) Edit the variable mce_file_name in takedata_test.py for the location and name of mce data file to
be used.

if __name__ =="__main__":
    mce_file_name = "VLB"

3.) Settings.py stores the global variables that will be used across the different documents.

4.) Netcdf_trial.py is called by takedata_test.py and creates a new netcdf file, and initializes the groups, dimensions, and variables that you will access later. A new file will be created when it reaches the file size limit imposed by takedata_test.py.

5.) Two global variable counters are initialized in settings.py and are used to keep track of the file number generated by the mce that the gui is currently reading, and the netcdf file number that we are putting the data into. These are "a" and "n" repsectively.

6.) Data can be read from the netcdf file using netcdf_read.py. It has three main functions, currently. You can choose to read in the groups and variables from a specific file, or read from all of the files created. You also have the option of printing all available groups and variables without parsing any actual data.
  a) To print groups and variables, enter the following command in the netcdf_read.py directory:
      python netcdf_read.py keys

  b) To read in data from a single file of name "gui_data_test{n}.nc":
      python netcdf_read.py one {n} {group} {variable}
      Example:
      python netcdf_read.py one 0 mce_header header

      # NOTE: the variable and groups names are case sensitive!
      # This will return data for only that variable and the time stamps that go with it

  c) (STILL UNDER CONSTRUCTION) To read in data from all files of names "gui_data_test{n}.nc"
      python netcdf_read.py all {group} {variable}

  d) (STILL UNDER CONSTRUCTION) To print the attributes of a group:
      Add the flag "--group_att" to end of command
 
      # NOTE: This cannot be used in conjunction with "--var_att"

  e) (STILL UNDER CONSTRUCTION) To print the attributes of a variable:
      Add the flag "--var_att" to end of command

      # NOTE: This cannot be used in conjunction with "--group_att"