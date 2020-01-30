import sys

# Simple used to process text

# Uses arguments
# e.g. 
# python Read_Write_File.py input_file.txt output_file.txt
inFile = sys.argv[1]
outFile = sys.argv[2]

#This part creates a list containing every line of the input document
txtLines = []
with open(inFile , 'r') as inputRead:
    while True:
        line = inputRead.readline()
        if not line:
            break
        txtLines.append(line)

#Do something to content
#e.g. looks for "input" and replace with "output!" 
for idx, item in enumerate(txtLines):
   if "input" in item:
       txtLines[idx] = "output!"

#This part creates a new file with the processed information
with open(outFile, 'w') as outputWrite:
    for line in txtLines:
        outputWrite.write(line)
