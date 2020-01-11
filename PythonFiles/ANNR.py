from datetime import datetime, timedelta
import sqlite3
import json
import urllib.request
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import scale
from TFANN import ANNR
#from google.colab import files

def main():
    #read the saved data
    stock_data = readData()
    #stock_data=scale(stock_data)
    dates = [int((datetime.strptime(i[0], "%Y-%m-%d") - datetime(1970, 1, 1)).total_seconds()) for i in stock_data]
    prices = [int(i[1]) for i in stock_data]
    #dates=scale(dates)
    #prices=scale(prices)

    #plt.plot(dates, prices)
    #plt.show()
    input = 1
    output = 1
    hidden = 50
    #array of layers, 3 hidden and 1 output, along with the tanh activation function
    layers = [('F', hidden), ('AF', 'tanh'), ('F', hidden), ('AF', 'tanh'), ('F', hidden), ('AF', 'tanh'), ('F', output)]
    #construct the model and dictate params
    mlpr = ANNR([input], layers, batchSize = 256, maxIter = 20000, tol = 0.2, reg = 1e-4, verbose = True)
    #number of days for the hold-out period used to access progress
    holdDays = 5
    totalDays = len(dates)
    #fit the model to the data "Learning"
    mlpr.fit(dates[(totalDays-holdDays)], prices[(totalDays-holdDays)])
    #createPlot(stock_data)



#load Json data into a list object
def loadData(raw):
    json_object = json.load(raw)
    #print(json_object)
    listResult=json_object["bpi"]
    print(listResult)
    data_list=[]
    for data in listResult.items():
        print(data)
        data_list.append(data)
    return data_list

#fetch Data from RecipePuppy Api
def getData(url):
    #print('hello world')
    try:
        f = urllib.request.urlopen(url)
        print(f)
    except Exception as e:
        print('Exception while calling endpoint')
        print(str(e))
    return f

#Save Data in dbRecipes database
def  saveData(data_list):
    try:
       con = sqlite3.connect('dbBitcoin.db')
       c = con.cursor()

       c.execute("DELETE  FROM tbBitCoin")
    # Insert data list to the tblRecipePuppy table
       c.executemany('INSERT INTO tbBitCoin VALUES (?,?)', data_list)

    # Save (commit) the changes
       con.commit()
    except Exception as e:
        print(str(e))
    #close the connection
    con.close()

#Read Data in dbRecipes database
def  readData():
    con = sqlite3.connect('dbBitcoin.db')
    cur = con.cursor()
    cur.execute("SELECT * from tbBitCoin")
    rows = cur.fetchall()
    #print('Printing the rows')
    #for row in rows:
        #print (row)
    con.close()
    return(rows)

#Print Plot in dbRecipes database
def  createPlot(data):
    df=pd.DataFrame(data)
    df[0]=pd.to_datetime(df[0])
    plt.plot(df[0],df[1])
    plt.show()
main()
