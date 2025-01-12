from flask import Flask, request, jsonify
import psycopg2
import random
import string
app = Flask(__name__)

def connect_to_db():
    conn = psycopg2.connect(
        dbname="database",
        user="postgres",
        password="postgres",
        host="postgres-service.database.svc.cluster.local",
        port=5432
    )
    return conn

def generate_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

@app.route('/', methods=['GET'])
def def_route():
    return jsonify({'auth': 'successfully'}), 201

# Route for user registration
@app.route('/register', methods=['POST'])
def register_user():
    user_data = request.json
    username = user_data.get('username')
    email = user_data.get('email')
    password = user_data.get('password')

    if not (username and email and password):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        conn = connect_to_db()
        cur = conn.cursor()

        # Insert the user data into the database
        cur.execute("""INSERT INTO Users (username, email, password_hash)
                    VALUES (%s, %s, %s)
                    RETURNING user_id""",
                    (username, email, password))
        user_id = cur.fetchone()[0]
        conn.commit()

        return jsonify({'message': 'User created successfully', 'user_id': user_id}), 201
    except psycopg2.Error as e:
        return jsonify({'message': 'Error creating user', 'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

#Route for user login
@app.route('/login', methods=['POST'])
def login_user():
    login_data = request.json
    username = login_data.get('username')
    password = login_data.get('password')

    if not (username and password):
        return jsonify({'error': 'Missing username or password'}), 400

    try:
        conn = connect_to_db()
        cur = conn.cursor()

        # Check if the username and password match
        cur.execute("SELECT * FROM Users WHERE username = %s AND password_hash = %s", (username, password))
        user = cur.fetchone()

        if user:
            # Generate a random token
            token = generate_token()

            # Save the token in the database
            cur.execute("UPDATE Users SET token = %s WHERE username = %s", (token, username))
            conn.commit()

            return jsonify({'token': token}), 200
        else:
            return jsonify({'error': 'Invalid username or password'}), 401
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

#Route for user logout
@app.route('/logout/<string:token>', methods=['DELETE'])
def logout_user(token):
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        # Check if token exists
        cur.execute("SELECT * FROM Users WHERE token = %s", (token,))
        user = cur.fetchone()
        if not user:
            return jsonify({'message': 'Token not found'}), 404

        # Delete the token from the database
        cur.execute("UPDATE Users SET token = NULL WHERE token = %s", (token,))
        conn.commit()
        return jsonify({'message': 'User logged out successfully'}), 200
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

# Route for listing all users
@app.route('/users', methods=['GET'])
def list_users():
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        # Query to retrieve all workspaces
        cur.execute("SELECT * FROM Users")
        users = cur.fetchall()

        # Format the response
        users_list = []
        for user in users:
            users_list.append({
                'user_id': user[0],
                'username': user[1],
                'email': user[2],
                'token': user[4]
            })

        return jsonify(users_list), 200
    except psycopg2.Error as e:
        return jsonify({'message': 'Error retrieving users', 'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/')
def hello_world():
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Users")
    result = cur.fetchall()
    cur.close()
    conn.close()
    return str(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)

