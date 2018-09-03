from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

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
    listOfCalories = [] # contains only calories
    listOfCaloriesPerDollar = [] #calories divided by price
    page = requests.get("https://hdh.ucsd.edu/DiningMenus/default.aspx?i=05")

    soup = BeautifulSoup(page.content, 'html.parser')

    #going to scrape each link by using a for loop;
    lunchlist = soup.select(".itemList")[1] #selects 2nd element in list of itemList classes, which is lunch.
    startstring = "https://hdh.ucsd.edu/DiningMenus/"
    for a in lunchlist.find_all('a', href=True): #i got help from: https://stackoverflow.com/questions/5815747/beautifulsoup-getting-href
        if '$' in a.get_text(): #a is the entire line that includes item name and price
            totalstring = startstring+a['href'] #we need to add diningmenus/ to href link
            newpage = requests.get(totalstring) # download the page we get
            newsoup = BeautifulSoup(newpage.content, 'html.parser') #create a html parser for page we downloaded
            itemHeader = newsoup.find(id="tblFacts") #tblFacts is id where the text we want is stored
            calories = list(itemHeader.children)[5].get_text() #calories are the 6th element of children list in itemHeader
            caloriesnumber = re.findall(r'\d+', calories) #find digits in the string calories https://stackoverflow.com/questions/4289331/python-extract-numbers-from-a-string
            listOfCalories.append(caloriesnumber[0])



    # finds the three meal menus and chooses one depending on the index
    # 0 = "breakfast", 1 = "lunch", and 2 = "dinner"
    menuList = soup.select(".menuList")[1]

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
        #else:
          #  listOfPrices.append("N/A")

    # adds only items to listOfItems
    for item in listOfItemsAndPrices:
        if "$" in item:
            item = item[:item.index("$")]
            item = item[:-2]
            listOfItems.append(item)
        #else:
           # listOfItems.append(item)
           
    #creating the third column, calories per dollar
    for x in range(len(listOfCalories)):
        a = float(listOfCalories[x])/ float(listOfPrices[x])
        listOfCaloriesPerDollar.append(a)

            
    # creates a data frame (spreadsheet) with the items in the left column
    # and prices in the right column


    data = pd.DataFrame({
            "item":listOfItems,
            "price":listOfPrices,
            "calories":listOfCalories,
            "caloriesPerDollar":listOfCaloriesPerDollar
        })

    # extracts the prices per item so that we can find the average price
    price = data["price"].str.extract("(?P<price_num>\d+.\d+)")
    data["price"] = price.astype('float64')
    #averageDailyPrice = round(data["price"].mean(), 2)
    #caloriesPerDollar = data["caloriesPerDollar"].str.extract("(?P<price_num>\d+.\d+)")
    #data["caloriesPerDollar"] = caloriesPerDollar.astype('float64')
    data_ascending = data.sort_values('caloriesPerDollar')
    return data_ascending




   


              
   
