from bs4 import BeautifulSoup
import requests
import pandas as pd

# define this all as a function that obtains the average price and calories
# per meal per dining hall in a list/tuple
def oneMeal(meal):
    tempListOfItems = [] # contains items and prices and unicode chars
    listOfItemsAndPrices = [] # contains items and prices
    listOfItems = [] # contains only items
    listOfPrices = [] # contains only prices

    page = requests.get("https://hdh.ucsd.edu/DiningMenus/default.aspx?i=05")

    soup = BeautifulSoup(page.content, 'html.parser')

    # finds the three meal menus and chooses one depending on the index
    # 0 = "breakfast", 1 = "lunch", and 2 = "dinner"
    menuList = soup.find_all(class_="menuList")[meal].get_text()

    # splits the string 
    tempListOfItems = menuList.split("\n")

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

    # adds only items to listOfItems
    for item in listOfItemsAndPrices:
        if "$" in item:
            item = item[:item.index("$")]
            item = item[:-2]
            listOfItems.append(item)
            
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

    print(data)
    return averageDailyPrice
    
meal = "lunch"
averagePrice = 0

if meal == "breakfast":
    averagePrice = oneMeal(0)
elif meal == "lunch":
    averagePrice = oneMeal(1)
elif meal == "dinner":
    averagePrice = oneMeal(2)  
    
              
   
