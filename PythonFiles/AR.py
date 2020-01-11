from pandas import read_csv
from matplotlib import pyplot
from statsmodels.tsa.ar_model import AR
from sklearn.metrics import mean_squared_error
import numpy
import sqlite3

def main():
    #read the saved data
    stock_data = readData()
    data = [int(i[0]) for i in stock_data]
    data = difference(data)
    #pyplot.plot(data)
    #pyplot.show()
    runPrediction(data)

# create a difference transform of the dataset
def difference(dataset):
	diff = list()
	for i in range(1, len(dataset)):
		value = dataset[i] - dataset[i - 1]
		diff.append(value)
	return numpy.array(diff)

# Make a prediction give regression coefficients and lag obs
def predict(coef, history):
	yhat = coef[0]
	for i in range(1, len(coef)):
		yhat += coef[i] * history[-i]
	return yhat



#Read Data in dbRecipes database
def  readData():
    con = sqlite3.connect('dbBitcoin.db')
    cur = con.cursor()
    cur.execute("SELECT Price from tbBitCoin")
    rows = cur.fetchall()
    #print('Printing the rows')
    #for row in rows:
        #print (row)
    con.close()
    return(rows)

#Print Plot in dbRecipes database
def  runPrediction(data):
    # split dataset
    #X = difference(data)
    X = data
    size = int(len(X) * 0.66)
    train, test = X[0:size], X[size:]
    # train autoregression
    model = AR(train)
    model_fit = model.fit(maxlag=6, disp=False)
    window = model_fit.k_ar
    coef = model_fit.params
    # walk forward over time steps in test
    history = [train[i] for i in range(len(train))]
    predictions = list()
    for t in range(len(test)):
    	yhat = predict(coef, history)
    	obs = test[t]
    	predictions.append(yhat)
    	history.append(obs)
    error = mean_squared_error(test, predictions)
    print('Test MSE: %.3f' % error)

    # plot
    pyplot.plot(test)
    pyplot.plot(predictions, color='red')
    pyplot.show()
main()
