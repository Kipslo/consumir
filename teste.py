import sqlite3

oi = sqlite3.connect("sql.db")
cursor = oi.cursor()
temp = cursor.execute("SELECT * FROM Conts")
for i in temp:
    print(i)