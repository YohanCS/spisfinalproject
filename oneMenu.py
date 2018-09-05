from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

def oneMeal(meal, hall):
    """ Obtains the items, prices, calories, and calories per meal per dining hall 
        and stores them in a pandas dataframe that can be displayed on a webpage
    """
    
    tempListOfItems = [] # contains items and prices and unicode chars
    listOfItemsAndPrices = [] # contains items and prices
    listOfItems = [] # contains only items
    listOfPrices = [] # contains only prices
    listOfCalories = [] # contains only calories
    listOfServings = [] # contains servings and unicode spaces
    editedListOfServings = [] # contains only servings
    listOfCaloriesPerDollar = [] # calories divided by price
    listOfProtein = [] #contains proteins

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

            itemHeader = newsoup.find(id="tblFacts") # id for the table facts
            facts = itemHeader.select('td')
            serving = facts[1].get_text()
            servingNumber = 1
            if "EACH" in serving or "BOWL" in serving or "PORTN" in serving:
                servingNumber = re.findall(r'\d+', serving)
                servingNumber = float(servingNumber[0])

            listOfServings.append(serving)
                
            # calories are the 6th element of children list in itemHeader
            calories = list(itemHeader.children)[5].get_text() 
            # find digits in the string calories 
            # https://stackoverflow.com/questions/4289331/python-extract-numbers-from-a-string
            caloriesNumber = re.findall(r'\d+', calories)
            caloriesNumber = caloriesNumber[0]
            caloriesNumber = float(caloriesNumber)
            caloriesPerServing = round(caloriesNumber/servingNumber, 2)
            listOfCalories.append(caloriesPerServing) #we need to convert the list of size 1 we get from re.findall to just a string value
            
            # time to add protein
            itemNutrition = newsoup.find(id="tblNutritionDetails") #id for nutrition table
            nutritionLines = itemNutrition.select('td') #select all the table tags with info
            protein = nutritionLines[18].get_text()  #get the text from the 19th element which has protein
            proteinNumber = protein[protein.index('n')+2: protein.index('g')] #
            proteinNumber = float(proteinNumber)
            proteinPerServing = round(proteinNumber/servingNumber, 2)
            listOfProtein.append(proteinPerServing)     

    menuList = menuList.select("li")

    # converts menuList from list <li> tags and html code to string
    stringMenuList = ""
    for item in menuList:
        currentItem = item.get_text()
        stringMenuList = stringMenuList + "\n" + currentItem

    # splits the string 
    tempListOfItems = stringMenuList.split("\n")

    if len(tempListOfItems) > 1:
        # replaces the unicode spaces with string spaces and adds item and price
        # to listOfItemsAndPrices
        for item in tempListOfItems:
            if item == '':
                tempListOfItems = tempListOfItems[tempListOfItems.index(item) + 1:]
            else:
                item = item.replace('\xa0',' ')
                listOfItemsAndPrices.append(item)

        # replaces the unicode spaces with string spaces in listOfServings
        for serving in listOfServings:
            serving = serving.replace('\xa0',' ')
            serving = serving[serving.index("e  ") + 1:]
            serving = serving.strip()
            editedListOfServings.append(serving)
                
        size = len(listOfItems)

        # adds only prices to listOfPrices
        for item in listOfItemsAndPrices:
            if "$" in item:
                price = item[item.index("$"):]
                price = price[:price.index(")")]
                listOfPrices.append(price)
           # else:
                # listOfPrices.append("N/A")
        print(listOfPrices)

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
            price = listOfPrices[x]
            price = price[price.index("$") + 1:]
            a = round(float(listOfCalories[x])/ float(price))
            listOfCaloriesPerDollar.append(a)
                
        # creates a data frame (spreadsheet) with the items in the left column
        # and prices in the right column
        
        data = pd.DataFrame({
                "item":listOfItems,
                "price":listOfPrices,
                "serving":editedListOfServings,
                "caloriesPerServing":listOfCalories,
                "caloriesPerDollar":listOfCaloriesPerDollar,
                "proteinPerServing":listOfProtein
            })

        # extracts the prices per item so that we can find the average price
        # price = data["price"].str.extract("(?P<price_num>\d+.\d+)")
        # data["price"] = price.astype('float64')
        
        #averageDailyPrice = round(data["price"].mean(), 2)
        #caloriesPerDollar = data["caloriesPerDollar"].str.extract("(?P<price_num>\d+.\d+)")
        #data["caloriesPerDollar"] = caloriesPerDollar.astype('float64')
        
        data_ascending = data.sort_values('caloriesPerDollar')
        
        return data_ascending

    else:
        return



   


              


              
   
