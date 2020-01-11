import sqlite3
conn = sqlite3.connect('dbBitcoin.db')
c = conn.cursor()
try:
 # Create table
    c.execute('''CREATE TABLE tbBitCoin
             (Date, Price)''')



 # Save (commit) the changes
    conn.commit()
except Exception as e:
    print(str(e))

#closing the connection
conn.close()

print("Database creation successfull")
