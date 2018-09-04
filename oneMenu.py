from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

# define this all as a function that obtains the average price and calories
# per meal per dining hall in a list/tuple
def oneMeal(meal, hall):
    """ Obtains the items, prices, calories, and calories per meal per dining hall 
        and stores them in a pandas dataframe that can be displayed on a webpage
    """
    
    
    tempListOfItems = [] # contains items and prices and unicode chars
    listOfItemsAndPrices = [] # contains items and prices
    listOfItems = [] # contains only items
    listOfPrices = [] # contains only prices
    listOfCalories = [] # contains only calories
    listOfCaloriesPerDollar = [] # calories divided by price
    listOfProtein = [] #contains proteins
    diningHallPages = {
            "64Degrees":"64",
            "cafeV":"18",
            "canyonV":"24",
            "Foodworx":"11",
            "OVT":"05",
            "Pines":"01"
    }
    meals = {
            "Breakfast":0,
            "Lunch":1,
            "Dinner":2
    }

    hall = diningHallPages[hall] # obtains the hall in ending url digits from dictionary

    meal = meals[meal] # obtains the meal in index from the dictionary

    page = requests.get("https://hdh.ucsd.edu/DiningMenus/default.aspx?i=" + hall)

    soup = BeautifulSoup(page.content, 'html.parser')

    # finds the three meal menus and chooses one depending on the index
    # 0 = "breakfast", 1 = "lunch", and 2 = "dinner"
    menuList = soup.select(".menuList")[meal]

    # https://stackoverflow.com/questions/5815747/beautifulsoup-getting-href
    startstring = "https://hdh.ucsd.edu/DiningMenus/"
    for a in menuList.find_all('a', href=True): 
        if '$' in a.get_text(): # a is the entire line that includes item name and price
            totalstring = startstring + a['href'] # we need to add diningmenus/ to href link
            newpage = requests.get(totalstring) # download the page we get
            # create a html parser for page we downloaded
            newsoup = BeautifulSoup(newpage.content, 'html.parser') 
            # tblFacts is id where the text we want is stored
            itemHeader = newsoup.find(id="tblFacts") 
            #calories are the 6th element of children list in itemHeader
            calories = list(itemHeader.children)[5].get_text() 
            #find digits in the string calories 
            # https://stackoverflow.com/questions/4289331/python-extract-numbers-from-a-string
            caloriesNumber = re.findall(r'\d+', calories) 
            listOfCalories.append(caloriesNumber[0])

            #time to add protein
            itemNutrition = newsoup.find(id="tblNutritionDetails") #id for nutrition table
            nutritionLines = itemNutrition.select('td') #select all the table tags with info
            protein = nutritionLines[18].get_text()  #get the text from the 19th element which has protein
            proteinNumber = re.findall(r'\d+\.\d+', protein) # https://stackoverflow.com/questions/4703390/how-to-extract-a-floating-number-from-a-string
            print(proteinNumber)
            listOfProtein.append(proteinNumber)
    print(len(listOfProtein))
    

    
    menuList = menuList.select("li")

    # converts menuList from list <li> tags and html code to string
    stringMenuList = ""
    for item in menuList:
        currentItem = item.get_text()
        stringMenuList = stringMenuList + "\n" + currentItem

    # splits the string 
    tempListOfItems = stringMenuList.split("\n")

    if tempListOfItems != []:
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
           # else:
                # listOfPrices.append("N/A")
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
        
        # data_ascending = data.sort_values('caloriesPerDollar')
        
        #print( data)

   # else:
       # return


oneMeal('Lunch', 'OVT')

   


              
   
