import netCDF4
import sys, os

dir = '/Users/vlb9398/Dropbox/NetCDF_Test/'
sys.path.append(dir)

def main():
    if os.path.exists(dir):
        files = [dir + x for x in os.listdir(dir) if (x.startswith("raw") and x.endswith(".nc"))]
        newest = max(files , key = os.path.getctime)
        oldest = min(files, key = os.path.getctime)
        print("Available Files:",'\n', "Newest: %s" %(newest.replace(dir,'')),'\n', "Oldest: %s" %(oldest.replace(dir,'')))
        

    else :
        print("Directory Not Found")

if __name__ == "__main__" :
    main()
