import os
import shutil
import sys

# This script will go through the subdirectories of a folder and move all 
# their content to a destionation folder.
# Tested on Windows 10 - 2020-01-28
# @ Guilherme Trevisan V1.0

# Path containing subdirectories (folders)
#root_source_dir = r'C:\Source' # Custom Path
root_source_dir = os.getcwd() #Use Script location

# Path to where content of subfolders will be moved to
root_destination_dir = r'F:\Destination'

# A list to append only subfolders
sourceFolders = []

subdirectoriesLength = 0
currentIndex = 1
clear = lambda: os.system('cls')

# Extract all folders in rootSourceDir 
# and store their path in the sourceFolders list
for item in os.listdir(root_source_dir):
    src_file = os.path.join(root_source_dir, item)
    if os.path.isdir(src_file):
        #print(src_file)
        sourceFolders.append(src_file)

clear()
print()
subdirectoriesLength = len(sourceFolders)
print("    Number of subdirectories: " + str(subdirectoriesLength))


# Walk through subfolders moving all contents 
# to destination (overwriting)
for subdir in sourceFolders:
    sys.stdout.write('\r' + "    Currently working on: " + str(currentIndex) + " out of " + str(subdirectoriesLength))
    currentIndex += 1
    for src_dir, dirs, files in os.walk(subdir):
        dst_dir = src_dir.replace(subdir, root_destination_dir, 1)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                # if src and dst are the same
                if os.path.samefile(src_file, dst_file):
                    continue
                os.remove(dst_file)
            shutil.move(src_file, dst_dir)
