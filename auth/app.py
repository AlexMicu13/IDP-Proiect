from flask import Flask
import psycopg2

app = Flask(__name__)

@app.route('/')
def hello_world():
    conn = psycopg2.connect(dbname="your_database_name", user="your_username", password="your_password", host="postgres")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Users")
    result = cur.fetchall()
    cur.close()
    conn.close()
    return str(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

