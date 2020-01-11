from datetime import datetime, timedelta
import sqlite3
import json
import urllib.request
import pandas as pd
import matplotlib.pyplot as plt


def main():
    endDate = datetime.now()
    endDate = endDate.strftime('%Y-%m-%d')
    startDate = datetime.now() - timedelta(days=3465)
    startDate = startDate.strftime('%Y-%m-%d')
    #constructing URL with start and end date. End Date is today and Start Date is 10 days before
    URL = 'https://api.coindesk.com/v1/bpi/historical/close.json?start=' + startDate + '&end=' + endDate

    #invoke API to get the bitcoin data for past 10 days
    raw=getData(URL) #fetch data from API

    #format data. Convert JSON into Tuples
    data_list=loadData(raw)

    #Save datalist to the database
    saveData(data_list)

    #read the saved data
    storedData = readData()

    #create a line chart
    createPlot(storedData)

#load Json data into a list object
def loadData(raw):
    json_object = json.load(raw)
    #print(json_object)
    listResult=json_object["bpi"]
    #print(listResult)
    data_list=[]
    for data in listResult.items():
        #print(data)
        data_list.append(data)
    return data_list

#fetch Data from RecipePuppy Api
def getData(url):
    #print('hello world')
    try:
        f = urllib.request.urlopen(url)
        #print(f)
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
