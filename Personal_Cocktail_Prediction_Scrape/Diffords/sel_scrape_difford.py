"""
Selenium used for diffords URL navigation 

Output of this file is a json organized by classes of cocktails with their names and urls
"""

from selenium import webdriver
import time
import json
import os as os

directory = r'C:\Users\jschu\GitHub\Portfolio\Personal_Cocktail\Diffords'
os.chdir(directory)

PATH = r"C:\Program Files (x86)/chromedriver.exe"
driver = webdriver.Chrome(PATH)

#List of Drivers to Get through
classification = {}
classification['Anytime'] = 63
classification['Apertivo'] = 26
classification['Autumn'] = 27
classification['Bittersweet'] = 38
classification['Breakfast'] = 46
classification['Champagne'] = 21
classification['July_4th'] = 51
classification['After_Dinner'] =36
classification['Barbecue'] = 48
classification['Beer'] = 30
classification['Christmas_Thanksgiving'] = 33
classification['Fruitini'] = 61
classification['Hall_of_Fame'] = 37
classification['Halloween'] = 53
classification['Citrusy'] = 59
classification['Classic'] = 3
classification['Easy'] = 62
classification['Contemporary'] = 18
classification['Creamy'] = 5
classification['Dessert'] = 29
classification['Afternoon'] = 55
classification['Floral'] = 39
classification['Frozen'] = 17
classification['Fruity'] = 23
classification['Famous'] = 37
classification['Herbal'] = 56
classification['Hot'] = 24
classification['Icecream'] = 25
classification['Long_Highball'] = 42
classification['Martini'] = 19
classification['Modern'] = 20
classification['Molecular'] = 60
classification['New_Year'] = 54
classification['Saint_Patrick'] = 50
classification['Nightcap'] = 34
classification['Non-alcoholic'] = 12
classification['Party'] = 49
classification['Romantic'] = 31
classification['Savory'] = 40
classification['Short'] = 44
classification['Shot'] = 13
classification['Sours'] = 45
classification['Spicy'] = 41
classification['Spirit_Forward'] = 57
classification['Spring'] = 28
classification['Sugar_free_low_calorie'] = 58
classification['Summer'] =32
classification['Tiki'] = 16
classification['Winter'] = 47
classification['Wimbledon'] = 52
classification['Top_100'] = 14

if 'cocktail_classes.json' in os.listdir():
    cocktail_db = {}
    for key,value in classification.items():
        index = 0
        driver = webdriver.Chrome(PATH)
        webpage = f"https://www.diffordsguide.com/cocktails/search?style={value}&include%5Bdg%5D=1&limit=20&sort=rating&offset={index}"
        driver.get(webpage)
        time.sleep(5) #Allow 5 seconds for the web page to open
        
        #Find the number of cocktails within the category
        total = driver.find_elements_by_class_name('text-xxlarge')
        total = int(total[0].text)
        cocktail_name = []
        cocktail_urls=[]
        
        #This part is to find all the cocktails within the category
        while index <= total:
            #Retrieve cocktail names and its URLs
            if index > 0:
                driver = webdriver.Chrome(PATH)
                webpage = f"https://www.diffordsguide.com/cocktails/search?style={value}&include%5Bdg%5D=1&limit=20&sort=rating&offset={index}"
                driver.get(webpage)
                cocktail_sel_list = driver.find_elements_by_class_name('box__title')
                for name in cocktail_sel_list:
                    cocktail_name.append(name.text)
                
                urls = []
                match = 'https://www.diffordsguide.com/cocktails/recipe/'
                for url in driver.find_elements_by_xpath("//a[@href]"):
                    urls.append(url.get_attribute("href"))
                
                for url in urls:
                    if match in url:
                        cocktail_urls.append(url)
                driver.quit()
            else:
                cocktail_sel_list = driver.find_elements_by_class_name('box__title')
                for name in cocktail_sel_list:
                    cocktail_name.append(name.text)
                    
                urls = []
                match = 'https://www.diffordsguide.com/cocktails/recipe/'
                for url in driver.find_elements_by_xpath("//a[@href]"):
                    urls.append(url.get_attribute("href"))
        
                for url in urls:
                    if match in url:
                        cocktail_urls.append(url)
                driver.quit()
            index+=20
        
        cocktail_db[key] = {}
        cocktail_db[key]['name'] = cocktail_name
        cocktail_db[key]['url'] = cocktail_urls
else:
    print('Please erase file in directory before running the program')


with open("cocktail_classes.json", "w") as write_file:
        json.dump(cocktail_db, write_file, indent=4)

"""

#Create a function that extract information out of the individual cocktail websites

def get_cocktail_info(url):
    #Open up connection with the cointreau webpage
    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()
    
    #html parsing
    page_soup = soup(page_html,"html.parser")
    
    #grabs cocktail name
    cock_name = page_soup.find_all('div',class_='app-cocktail-title__content')
    title = cock_name[0].div.h1.text
    cock_id = cock_name[0].find('div',class_='app-cocktail-title__links').button['data-id']
    rating = cock_name[0].find('div',class_='js-rating')['data-rating']
    num_votes = cock_name[0].find('div',class_='votes js-votes')['data-votes']
    
    #grabs the container that finds taste, preptime, preplevel
    cock_info = page_soup.find_all('div',class_="app-cocktail-info__specifications-container")
    info_container = cock_info[0].find_all('span')
    taste = info_container[0].text
    preptime = info_container[1].text
    preplevel = info_container[2].text
    
    #grabs the container that finds ingredients and volume
    cock_ingredient = page_soup.find_all('ul',class_='app-cocktail-info__ingredients-table__list')
    ingredient_container = cock_ingredient[0].find_all('li')
    ingredient_list = []
    for item in ingredient_container:
        amount = item.find('div',class_='count js-count').text
        try:
            unit = item.find('div',class_='unit js-unit').text
        except:
            unit = item.find('div',class_='unit').text
        ingredient = item.find('div',class_='ingredient').text
        ingredient_list.append([ingredient,amount,unit])
        
    cocktail_info = [title,cock_id,rating,num_votes,taste,preptime,preplevel]
    return cocktail_info, ingredient_list

#Loop through the urls to retrieve the information and store it
cocktail_info_list = []
cocktail_ingredient_dic = {}
for url in urls:
    info,ingredient = get_cocktail_info(url)
    cocktail_info_list.append(info)
    cocktail_ingredient_dic[info[1]]=ingredient #entered dictionary by cocktail id

    """
