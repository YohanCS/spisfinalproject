from bs4 import BeautifulSoup
import requests
import pandas as pd

# define this all as a function that obtains the average price and calories
# per meal per dining hall in a list/tuple
def oneMeal(meal):
    tempListOfItems = [] # contains items and prices and unicode chars
    listOfItems = [] # contains items and prices
    oneMenu = [] # contains the items of only one menu
    listOfPrices = [] # contains only prices

    page = requests.get("https://hdh.ucsd.edu/DiningMenus/default.aspx?i=05")

    soup = BeautifulSoup(page.content, 'html.parser')

    menuList = soup.find_all(class_="menuList")[meal].get_text()

    tempListOfItems = menuList.split("\n")

    for item in tempListOfItems:
        if '(Pillows)' in item:
            do nothing;
        if item == '':
            tempListOfItems = tempListOfItems[tempListOfItems.index(item) + 1:]
        else:
            item = item.replace('\xa0',' ')
            listOfItems.append(item)
        
    size = len(listOfItems)

    # adds only prices to listOfPrices and only items to editedListOfItems
    for item in listOfItems:
        if "$" in item:
            price = item[item.index("$") + 1:item.index(')')]
            listOfPrices.append(price)
        else:
            listOfPrices.append("N/A")

    # creates a data frame (spreadsheet) with the items in the left column
    # and prices in the right column
    data = pd.DataFrame({
            "item":listOfItems,
            "price":listOfPrices
        })

    # extracts the prices per item so that we can find the average price
    # but this loses accuracy because of the \d character
    price_nums = data["price"].str.extract("(?P<price_num>\d+)")
    data["price_num"] = price_nums.astype('float64')
    averageDailyPrice = round(data["price_num"].mean(), 2)

    print(averageDailyPrice)
    print(data)
    
meal = "lunch"

if meal == "breakfast":
    oneMeal(0)
elif meal == "lunch":
    oneMeal(1)
elif meal == "dinner":
    oneMeal(2)  
    
              
   

