import sqlite3

conn = sqlite3.connect("school.db")
cursor = conn.cursor()

# AI מניח שהטבלה נקראת "students"
cursor.execute("SELECT * FROM students WHERE grade > 90")
print(cursor.fetchall())