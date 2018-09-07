import netCDF4
import sys, os, re

# ------------- NetCDF Directory ----------------
dir = '/Users/vlb9398/Dropbox/NetCDF_Test/'
sys.path.append(dir)
# -----------------------------------------------

keep = []
files2 = []
files = []

# ===================================================================================================
def main():
    print("Choose name search or date search: ")
    action = input("a : name , b : date \n")

    if action == 'a':
        name_search(files2,action)
    elif action == 'b':
        date_search(files,action)
    else :
        print("I'm sorry... I didn't understand. Please try again.")
# ====================================================================================================
def name_search(files2,action):
    action4 = input('Enter name to search: \n')
    if action == 'a':
        if os.path.exists(dir):
            files = [dir + x for x in os.listdir(dir) if (x.startswith(action4) and x.endswith(".nc"))]
            print('\n'.join([s.replace(dir,'') for s in files]))
            print('Do you still want to search by time?')
            action5 = input('y : yes , n : no \n')

            if action5 == 'y':
                date_search(files,action)
            elif action5 == 'n':
                pass
            else :
                print("I'm sorry... I didn't understand. Please try again.")
                pass

        else :
            print("Directory does not exist")

    elif action == 'b':
        keep = [x for x in files2 if re.search(action4,x)]
        print('\n'.join([s.replace(dir,'') for s in keep]))

    else :
        print('uh-oh...something went wrong...')
# ======================================================================================================
def date_search(files, action):
    if action == 'b' :
        if os.path.exists(dir):
            files = [dir + x for x in os.listdir(dir) if (x.endswith(".nc") and x.startswith("raw"))]
            newest = max(files , key = os.path.getctime)
            oldest = min(files, key = os.path.getctime)
            print("Available Files:",'\n', "Newest: %s" %(newest.replace(dir,'')),'\n', "Oldest: %s" %(oldest.replace(dir,'')))
            action2 = input("Enter Oldest Date: \n")
            action3 = input("Enter Newest Date: \n")

            files2 = [dir + y for y in os.listdir(dir) if (re.search(action2,y)) or (re.search(action3,y))]
            for s in files :
                if os.path.getctime(s) <= os.path.getctime(files2[0]) \
                and os.path.getctime(s) >= os.path.getctime(files2[1]) :
                    keep.append(s)

                else :
                    print("No files found in that range.")
                    pass

            print(keep)
            print("Do you still want to search by name?")
            action4 = input('y : yes , n : no \n')

            if action4 == 'y':
                name_search(keep,action)
            elif action4 == 'n':
                pass
            else :
                print("I'm sorry... I didn't understand. Please try again.")
                pass

    elif action == 'a' :
        action6 = input("Enter Oldest Date: \n")
        action7 = input("Enter Newest Date: \n")

        files2 = [ y for y in files if (re.search(action6,y)) or (re.search(action7,y))]
        for s in files :
            if os.path.getctime(s) <= os.path.getctime(files2[0]) \
            and os.path.getctime(s) >= os.path.getctime(files2[1]) :
                keep.append(s)
            else :
                print("No files found in that range.")
                pass

        print('\n'.join([s.replace(dir,'') for s in keep]))
    else :
        print("Action not recognized")
# =======================================================================================================
if __name__ == "__main__" :
    main()
