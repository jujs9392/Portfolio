# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 16:05:53 2022

@author: jschu
"""

from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import regex as re
import json
import os

os.chdir(r'C:\Users\jschu\GitHub\Portfolio\Personal_Cocktail\Diffords')

with open('cocktail_classes.json') as f:
    data = json.load(f)

count = 1
cocktail_detail = {}
duplicates = []
count_num = []
error = []
duplicates_class = []
for classes in data.keys():
    for urls in data[classes]['url']:
        webpage = urls
        uClient = uReq(webpage)
        page_html = uClient.read()
        uClient.close()
        
        page_soup = soup(page_html,"html.parser")
        product_name = page_soup.find('h1').text
        
        if product_name in cocktail_detail.keys():
            #if type(cocktail_detail[product_name]['class']) != list:
            #     cocktail_detail[product_name]['class']=[cocktail_detail[product_name]['class'],classes]
            #else:
            #    cocktail_detail[product_name]['class'].append(classes)
            duplicates.append(product_name)
            duplicates_class.append(classes)
            count_num.append(count)
            print('Found duplicates!')
        elif product_name not in cocktail_detail.keys():
            #Find the image Booziness and Dry/Sour Image
            images = page_soup.find_all('img')
            number = r'\d+'
            val_list=[]
            for img in images:
                value = img.attrs['src']
                if '.svg' in value:
                    attribute_rating = re.findall(number,value)
                    val_list.append(int(attribute_rating[0]))
                if 'alt' in img.attrs.keys():
                    if img.attrs['alt'] =='Product image':
                        image_link = img.attrs['src']
            if len(val_list) == 2:
                booziness = val_list[0]
                dryness = val_list[1]
            elif len(val_list) == 1:
                booziness = val_list[0]
                print(f'flag {urls}')
            else:
                booziness = None
                dryness = None
            
            #Find the ingredients related to the cocktails
            ingredient_table = page_soup.find_all(class_='no-margin ingredients-table')
            ingredient_name_list = ingredient_table[0].find_all(class_='td-align-top')
            item_list = []
            for items in ingredient_name_list:
                temp_item = items.text.split('\t')
                for ind_item in temp_item:
                    if len(ind_item)>1:
                        second_filter = ind_item.split('\n')
                        for final_items in second_filter:
                            if final_items != '':
                                item_list.append(final_items)
            
            ingredient_dict = {}
            for i in range(1,len(item_list),2):
                key = item_list[i]
                value = item_list[i-1]
                ingredient_dict[key] = value
            
            #Contents
            alcohol_list = []
            glass = None
            garnish = None
            nutrition = None
            alcohol = None
            for content in page_soup.find_all(class_='cell'):
                try: 
                    if len(content.find('h3'))!=0:
                        h3_list = content.find('h3').text
                        if'Serve in a' in h3_list:
                            glass = content.find('a').text
                        if'Garnish' in h3_list:
                            garnish = content.find('p').text
                        if 'Nutrition' in h3_list:
                            nutrition = re.findall(number,content.find('p').text)
                            nutrition = int(nutrition[0])
                        if 'Alcohol' in h3_list:
                            alcohol = content.find(class_='no-margin-bottom').text
                            if alcohol is not None:
                                alcohol = alcohol.split('\n')
                                alcohol = list(filter(lambda p: p!='',alcohol))
                except:
                    pass
        
            cocktail_detail[product_name] = {}
            cocktail_detail[product_name]['booziness'] = booziness
            cocktail_detail[product_name]['dryness'] = dryness
            cocktail_detail[product_name]['ingredient'] = ingredient_dict
            cocktail_detail[product_name]['image'] = image_link
            cocktail_detail[product_name]['glass'] = glass
            cocktail_detail[product_name]['garnish'] = garnish
            cocktail_detail[product_name]['nutrition'] = nutrition
            cocktail_detail[product_name]['alcohol']=alcohol
            cocktail_detail[product_name]['url'] = urls
            cocktail_detail[product_name]['class'] = classes
        else:
            error.append((product_name,classes))
            print('Something is wrong')
        
        print(count)
        count+=1

with open("cocktail_detail2.json", "w") as write_file:
    json.dump(cocktail_detail, write_file, indent=4)