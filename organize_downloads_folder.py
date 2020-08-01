"""
 Script to quickly organize downloads folder
 @Guilherme Trevisan - TrevisanGMW@gmail.com - 2020-07-30 - github.com/TrevisanGMW
         
""" 

import os
import collections
from pprint import pprint

downloads_folder_path = os.path.join(os.path.expanduser('~'),'Downloads')
ignored_types = ['ini', 'obv']

file_mappings = collections.defaultdict()
for filename in os.listdir(downloads_folder_path):
    file_type = filename.split('.')[-1]
    if file_type not in ignored_types:
        file_mappings.setdefault(file_type, []).append(filename)


for folder_name, folder_items in file_mappings.items():
    folder_path = os.path.join(downloads_folder_path, folder_name)
    if not os.path.exists(folder_path):
    	os.mkdir(folder_path)

    for folder_item in folder_items:
        source = os.path.join(downloads_folder_path, folder_item)
        destination = os.path.join(folder_path, folder_item)
        try:
            print(f'Moving {source} to {destination}')
            os.rename(source, destination)
        except:
            print(f'An error happened when trying to move {source} to {destination}')
