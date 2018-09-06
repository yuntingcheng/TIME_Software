import netCDF4
import sys, os, re

dir = '/Users/vlb9398/Dropbox/NetCDF_Test/'
sys.path.append(dir)

keep = []
files2 = []
files = []
# ===================================================================================================
def main():
    print("Choose name search or date search: ")
    action = input("a : name , b : date")
    print("\n")

    if action == 'a':
        name_search(files2)
    elif action == 'b':
        date_search(files)
    else :
        print("I'm sorry... I didn't understand. Please try again.")
# ====================================================================================================
def name_search(files2):
    action4 = input('Enter name to search: ')
    print("")
    if action == 'a':
        if os.path.exists(dir):
            files = [dir + x for x in os.listdir(dir) if (x.startswith(action4) and x.endswith(".nc"))]
            print(files)
            print('Do you still want to search by time?')
            action5 = ('y : yes , n : no')
            if action5 == 'y':
                date_search(files)
            elif action5 == 'n':
                pass
            else :
                print("I'm sorry... I didn't understand. Please try again.")
                pass

        else :
            print("Directory does not exist")

    elif action == 'b':
        keep = [x for x in files2 if re.search(action5,x)]
        print(keep)

    else :
        print('uh-oh...something went wrong...')
# ======================================================================================================
def date_search(files):
    if action == 'b' :
        if os.path.exists(dir):
            files = [dir + x for x in os.listdir(dir) if x.endswith(".nc")]
            newest = max(files , key = os.path.getctime)
            oldest = min(files, key = os.path.getctime)
            print("Available Files:",'\n', "Newest: %s" %(newest.replace(dir,'')),'\n', "Oldest: %s" %(oldest.replace(dir,'')))
            action2 = input("Enter Oldest Date: ")
            print("\n")
            action3 = input("Enter Newest Date: ")
            print("\n")

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
            action4 = input('y : yes , n : no')

            if action4 == 'y':
                name_search(keep)
            elif action4 == 'n':
                pass
            else :
                print("I'm sorry... I didn't understand. Please try again.")
                pass

    elif action == 'a' :
        action6 = input("Enter Oldest Date: ")
        print("")
        action7 = input("Enter Newest Date: ")
        print("")

        files2 = [for s in files if (re.search(action6,y)) or (re.search(action7,y))]
        for s in files :
            if os.path.getctime(s) <= os.path.getctime(files2[0]) \
            and os.path.getctime(s) >= os.path.getctime(files2[1]) :
                keep.append(s)
        print(keep)
            else :
                print("No files found in that range.")
                pass
    else :
        print("Action not recognized")
# =======================================================================================================
if __name__ == "__main__" :
    main()
