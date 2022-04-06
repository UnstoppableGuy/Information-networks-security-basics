import sqlite3
import json

# server = sqllite3
conn_sql = sqlite3.connect('newdb.db')
cursor = conn_sql.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users(    
    id INTEGER PRIMARY KEY,
    name TEXT,
    password TEXT,
    role INT);
""")
# conn_sql.commit()
cursor.execute("""CREATE TABLE IF NOT EXISTS posts(    
    id INTEGER PRIMARY KEY,
    id_users INT,
    name TEXT,
    category TEXT,
    author TEXT,
    price TEXT,
    telephone TEXT);
""")
# conn_sql.commit()

cursor.execute("DELETE FROM posts WHERE name <> 0")
cursor.execute("DELETE FROM users WHERE name <> 0")

cursor.execute(" INSERT INTO users(name, password, role) VALUES('vladik', 'password', 2)")
cursor.execute(" INSERT INTO users(name, password, role) VALUES('petya', 'password', 1)")
cursor.execute(" INSERT INTO users(name, password, role) VALUES('omega', '1234567890', 2)")

cursor.execute(" INSERT INTO posts(name, id_users, name, category, author, price, telephone) VALUES('the beginning after the end','fantasy', 'TurleMe', '120', '80291111111', '1', '2')")
cursor.execute(" INSERT INTO posts(name, id_users, name, category, author, price, telephone) VALUES('witcher', 'fantasy', 'Анджиан Сапкойвский', '150', '+375293556787', '1', '2')")
cursor.execute(" INSERT INTO posts(name, id_users, name, category, author, price, telephone) VALUES('TEST', 1, 'TEST', 'TEST', 'TEST', 'TEST', 'TEST')")

cursor.close()
conn_sql.commit()
conn_sql.close()
