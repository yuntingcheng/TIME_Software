import netCDF4
import sys, os, re

dir = '/Users/vlb9398/Dropbox/NetCDF_Test/'
sys.path.append(dir)

keep = []
def main():
    print("Choose name search or date search: ")
    action = input("a : name , b : date")
    print("\n")

    if action == 'b':
        if os.path.exists(dir):
            files = [dir + x for x in os.listdir(dir) if (x.startswith("raw") and x.endswith(".nc"))]
            newest = max(files , key = os.path.getctime)
            oldest = min(files, key = os.path.getctime)
            print("Available Files:",'\n', "Newest: %s" %(newest.replace(dir,'')),'\n', "Oldest: %s" %(oldest.replace(dir,'')))
            action = input("Enter First Date: [t0,t1] ")
            print("\n")
            action2 = input("Enter Second Date: [y0,t1] ")
            print("\n")

            files2 = [dir + y for y in os.listdir(dir) if (re.search(action,y)) or (re.search(action2,y))]
            for s in files :
                if os.path.getctime(s) <= os.path.getctime(files2[0]) \
                and os.path.getctime(s) >= os.path.getctime(files[1]) :
                    keep.append(s)

                else :
                    print("No files found in that range. Please try again...")

            print(keep)
        else :
            print("Directory Not Found")

if __name__ == "__main__" :
    main()
