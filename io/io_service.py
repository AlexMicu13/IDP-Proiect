import psycopg2

conn = psycopg2.connect(dbname="your_database_name", user="your_username", password="your_password", host="postgres")
cur = conn.cursor()

# Perform database operations here

cur.close()
conn.close()
