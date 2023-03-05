import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup


'''This code is for specific parts of the individual cocktail page'''

my_url = r'https://www.cointreau.com/us/en/cocktails/pineapple-upside-down'
cointreau_url = r'https://www.cointreau.com/us/en/cocktails'


uClient = uReq(cointreau_url)
cointreau_html = uClient.read()
uClient.close()
cointreau_html = soup(cointreau_html,'html.parser')

found = cointreau_html.find_all('div',class_= 'cocktail-list__item__content')

#Open up connection with the cointreau webpage
uClient = uReq(my_url)
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

