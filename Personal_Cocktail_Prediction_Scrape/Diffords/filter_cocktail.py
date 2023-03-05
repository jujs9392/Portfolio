# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 15:38:53 2022

@author: jschu
"""
import regex as re
import json
import os
import pandas as pd

os.chdir(r'C:\Users\jschu\GitHub\Portfolio\Personal_Cocktail\Diffords')

with open('cocktail_detail.json') as f:
    detail = json.load(f)
    
with open('cocktail_classes.json') as f:
    types = json.load(f)
    
#Find duplicate names:
#Based on names
cocktail_name = []
for name in detail.keys():
    if name not in cocktail_name:
        cocktail_name.append(name)
            
#Based on classes
cocktail_list = []
count = 0
for classes in types.keys():
    for name in types[classes]['name']:
        count +=1
        if name not in cocktail_list:
            cocktail_list.append(name)
            
print(count==len(cocktail_list))

#Convert the json into a flat table
