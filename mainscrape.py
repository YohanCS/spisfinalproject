import requests
from bs4 import BeautifulSoup
import pandas as pd

response = requests.get("https://hdh.ucsd.edu/DiningMenus/default.aspx?i=05")

soup = BeautifulSoup(response.content, 'html.parser')

menu_list = soup.select('.itemList a')
#item = [d.get_text() for d in menu_list.select('a')]
item = menu_list[0]
item_text = item.get_text()

print(item)
#class_="menuList"
#class_="itemList"
#then go into <li> tags  maybe using css select

#if we can navigate to nutritionfacts, then go to id="tblFacts" then take children[2]
#if we can take itemlist and then go to a href then we can assign a variable to get requests.get

#
