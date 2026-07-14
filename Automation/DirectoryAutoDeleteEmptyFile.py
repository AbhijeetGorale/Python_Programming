# python File_name.py Folder_name 

import sys
import os
import time
import schedule

def DirctoryScanner(DirName = "Directory_name"):    # Mention the Directory name insted of  Directory_Name you want to scan 
    Border = "-"*50
    timestamp = time.ctime()

    Logfilename = "Report%s.log" %(timestamp)
    Logfilename = Logfilename.replace(" ","_")
    Logfilename = Logfilename.replace(":","_")

    fobj = open(Logfilename,"w")

    fobj.write(Border+"\n")
    fobj.write("This is a log file created by Automation\n")
    fobj.write("This is a Directory Cleaner Script\n")
    fobj.write(Border+"\n")
    
    Ret = False

    Ret = os.path.exists(DirName)
    if(Ret == False):
        print("There is no such directory")
        return

    Ret = os.path.isdir(DirName)
    if(Ret == False):
        print("It is not a directory")
        return

    FileCount = 0
    EmptyFileCount = 0

    for FolderName, SubFolder, FileName in os.walk(DirName):

        for fname in FileName:
            FileCount = FileCount + 1

            fname = os.path.join(FolderName,fname)
            
            if(os.path.getsize(fname) == 0):    # Empty file
                EmptyFileCount = EmptyFileCount + 1
                os.remove(fname)

    fobj.write("Total files scnned : "+str(FileCount)+"\n")
    fobj.write("Total empty files found : "+str(EmptyFileCount)+"\n")
    fobj.write("This log file is created at : "+timestamp+"\n")
    fobj.write(Border+"\n")

    fobj.close()

def main():
    Border = "-"*50
    print(Border)
    print("-------- Directory Automation ---------")
    print(Border)

    if(len(sys.argv) != 2):
        print("Invalid Number of arguments")
        print("Please specify the name of directory")
        print("Please Execute the file with Directory name")
        return

    # DirctoryScanner(sys.argv[1])
    schedule.every(1).minute.do(DirctoryScanner)

    while True:
        schedule.run_pending()
        time.sleep(1)

    print(Border)
    print("-------- Directory Automation ---------")
    print(Border)

if __name__ == "__main__":
    main()