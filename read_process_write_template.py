"""
 Simple template used to process input data (usually text)
 @Guilherme Trevisan - TrevisanGMW@gmail.com - 2019-12-01 - github.com/TrevisanGMW
 
        Parameters:
                input_file (string) : path for the input file
                output_file (string) : path to write the output file  

How to use:
python read_process_write_template.py input_file.txt output_file.txt
        
""" 

import sys


input_file = sys.argv[1]
output_file = sys.argv[2]

#Creates a list containing every line of the input document
lines_list = []
with open(input_file , 'r') as input_read:
    while True:
        line = input_read.readline()
        if not line:
            break
        lines_list.append(line)

#Do something to content
#e.g. looks for "input" and replace with "output!" 
for idx, item in enumerate(lines_list):
   if "input" in item:
       lines_list[idx] = "output!"

#Creates a new file with the processed information
with open(output_file, 'w') as output_write:
    for line in lines_list:
        output_write.write(line)
output_write.close()
