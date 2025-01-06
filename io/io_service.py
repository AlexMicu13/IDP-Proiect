from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

# Database connection function
def connect_to_db():
    conn = psycopg2.connect(
        dbname="database",
        user="postgres",
        password="postgres",
        host="localhost",
        port=5432
    )
    return conn

# GET route for fetching all users
@app.route('/users', methods=['GET'])
def get_all_users():
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        # Fetch all users
        cur.execute("SELECT * FROM Users")
        users = cur.fetchall()

        # Format the data for JSON response
        users_list = []
        for user in users:
            users_list.append({
                'user_id': user[0],
                'username': user[1],
                'email': user[2],
                'created_at': user[5],
            })

        return jsonify(users_list), 200
    except psycopg2.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

# GET route for fetching all workspaces
@app.route('/workspaces', methods=['GET'])
def get_all_workspaces():
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        # Fetch all workspaces
        cur.execute("SELECT * FROM Workspaces")
        workspaces = cur.fetchall()

        # Format the data for JSON response
        workspaces_list = []
        for workspace in workspaces:
            workspaces_list.append({
                'workspace_id': workspace[0],
                'workspace_name': workspace[1],
                'capacity': workspace[2],
                'location': workspace[3],
                'description': workspace[4],
                'created_at': workspace[5],
            })

        return jsonify(workspaces_list), 200
    except psycopg2.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

# GET route for fetching all reservations
@app.route('/reservations', methods=['GET'])
def get_all_reservations():
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        # Fetch all reservations
        cur.execute("SELECT * FROM Reservations")
        reservations = cur.fetchall()

        # Format the data for JSON response
        reservations_list = []
        for reservation in reservations:
            reservations_list.append({
                'reservation_id': reservation[0],
                'user_id': reservation[1],
                'workspace_id': reservation[2],
                'start_time': reservation[3],
                'end_time': reservation[4],
                'reservation_date': reservation[5],
            })

        return jsonify(reservations_list), 200
    except psycopg2.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=83)
