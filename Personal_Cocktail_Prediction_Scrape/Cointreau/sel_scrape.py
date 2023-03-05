"""
Infinite scrolling of the webpage to retrieve URLs from cointreau

Selenium used for infinite scrolling and URL retreival
BeautifulSoup used for retreiving cocktail info

The output of this script is a csv with cocktail ingredients and key attributes
"""

from selenium import webdriver
import time
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

PATH = r"C:\Program Files (x86)/chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get(r'https://www.cointreau.com/us/en/cocktails')
time.sleep(5) #Allow 5 seconds for the web page to open

#Remember that once the webpage opens, you need to enter your birthday & year to continue

#Infinite scrolling after loading
scroll_pause_time = 1
screen_height = driver.execute_script("return window.screen.height;") #This sends the message directly to the webpage to return screen height
i = 1

while True:
    #scroll one screen height each time
    driver.execute_script(f"window.scrollTo(0,{screen_height}*{i});".format(screen_height = screen_height,i=i))
    i += 1
    time.sleep(scroll_pause_time)
    
    #update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
    scroll_height = driver.execute_script("return document.body.scrollHeight;")
    
    #Break the loop when the height we need to scroll to is larger than the total scroll ehgith
    if (screen_height) *i > scroll_height:
        break

#Retreive cocktail information and their URLs
urls = []
for url in driver.find_elements_by_xpath("//a[@href]"):
    urls.append(url.get_attribute("href"))

filter1 = r'https://www.cointreau.com/us/en/cocktails/'
urls = [final for final in urls if filter1 in final]

drop1 = 'https://www.cointreau.com/us/en/cocktails/discover'
drop2 = 'https://www.cointreau.com/us/en/cocktails/find-your-cocktails'
drop3 = 'https://www.cointreau.com/us/en/cocktails/categories/cinco-de-mayo'
for url in urls:
    if url == drop1 or url == drop2 or url == drop3:
        urls.remove(url)

driver.quit()

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
    
