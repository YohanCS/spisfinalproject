from bs4 import BeautifulSoup
import requests
import pandas as pd

# define this all as a function that obtains the average price and calories
# per meal per dining hall in a list/tuple
def oneMeal(meal):
    if meal == "Breakfast":
        meal = 0 
    elif meal == "Lunch":
        meal = 1
    elif meal == "Dinner":
        meal = 2
    
    tempListOfItems = [] # contains items and prices and unicode chars
    listOfItemsAndPrices = [] # contains items and prices
    listOfItems = [] # contains only items
    listOfPrices = [] # contains only prices

    page = requests.get("https://hdh.ucsd.edu/DiningMenus/default.aspx?i=05")

    soup = BeautifulSoup(page.content, 'html.parser')

    # finds the three meal menus and chooses one depending on the index
    # 0 = "breakfast", 1 = "lunch", and 2 = "dinner"
    menuList = soup.select(".menuList")[meal]

    menuList = menuList.select("li")

    # converts menuList from list <li> tags and html code to string
    stringMenuList = ""
    for item in menuList:
        currentItem = item.get_text()
        stringMenuList = stringMenuList + "\n" + currentItem

    # splits the string 
    tempListOfItems = stringMenuList.split("\n")

    # replaces the unicode spaces with string spaces and adds item and price
    # to listOfItemsAndPrices
    for item in tempListOfItems:
        if item == '':
            tempListOfItems = tempListOfItems[tempListOfItems.index(item) + 1:]
        else:
            item = item.replace('\xa0',' ')
            listOfItemsAndPrices.append(item)
        
    size = len(listOfItems)

    # adds only prices to listOfPrices
    for item in listOfItemsAndPrices:
        if "$" in item:
            price = item[item.index("$") + 1:]
            price = price[:price.index(")")]
            listOfPrices.append(price)
        else:
            listOfPrices.append("N/A")

    # adds only items to listOfItems
    for item in listOfItemsAndPrices:
        if "$" in item:
            item = item[:item.index("$")]
            item = item[:-2]
            listOfItems.append(item)
        else:
            listOfItems.append(item)
            
    # creates a data frame (spreadsheet) with the items in the left column
    # and prices in the right column
    data = pd.DataFrame({
            "item":listOfItems,
            "price":listOfPrices
        })

    # extracts the prices per item so that we can find the average price
    price = data["price"].str.extract("(?P<price_num>\d+.\d+)")
    data["price"] = price.astype('float64')
    averageDailyPrice = round(data["price"].mean(), 2)

    return data



              
   
