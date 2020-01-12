Use-Case: Pull data from the Bitcoin Price Index API for past 10 years, store it in a database, and display a chart. 
Then read the data from the database, build a prediction model using regression to predict bitcoin price.

API Endpoint: https://api.coindesk.com/v1/bpi/historical/close.json?start=2013-09-01&end=2013-09-05

Python Libraries/Packages:
⦁ URLlib
⦁ SQLLite
⦁ matplotlib
⦁ json
⦁ datetime
⦁ pandas
⦁ statsmodels.tsa.ar_model
⦁ numpy

