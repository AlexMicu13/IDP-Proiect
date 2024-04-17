from flask import Flask, request, jsonify
import psycopg2
from datetime import datetime

app = Flask(__name__)

# Function to establish database connection
def connect_to_db():
    conn = psycopg2.connect(
        dbname="your_database_name", 
        user="your_username", 
        password="your_password", 
        host="postgres"
    )
    return conn

# Route for creating a new workspace
@app.route('/workspace', methods=['POST'])
def create_workspace():
    data = request.json
    workspace_name = data.get('workspace_name')
    capacity = data.get('capacity')
    location = data.get('location')
    description = data.get('description')

    try:
        conn = connect_to_db()
        cur = conn.cursor()

        # Insert new workspace into database
        cur.execute("""
            INSERT INTO Workspaces (workspace_name, capacity, location, description)
            VALUES (%s, %s, %s, %s)
            RETURNING workspace_id
        """, (workspace_name, capacity, location, description))
        workspace_id = cur.fetchone()[0]
        conn.commit()

        return jsonify({'message': 'Workspace created successfully', 'workspace_id': workspace_id}), 201
    except psycopg2.Error as e:
        return jsonify({'message': 'Error creating workspace', 'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

# Route for deleting a workspace
@app.route('/workspace/<int:workspace_id>', methods=['DELETE'])
def delete_workspace(workspace_id):
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        # Check if workspace exists
        cur.execute("SELECT * FROM Workspaces WHERE workspace_id = %s", (workspace_id,))
        workspace = cur.fetchone()
        if not workspace:
            return jsonify({'message': 'Workspace not found'}), 404

        # Delete workspace
        cur.execute("DELETE FROM Workspaces WHERE workspace_id = %s", (workspace_id,))
        conn.commit()

        return jsonify({'message': 'Workspace deleted successfully'}), 200
    except psycopg2.Error as e:
        return jsonify({'message': 'Error deleting workspace', 'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

# Route for listing all workspaces
@app.route('/workspaces', methods=['GET'])
def list_workspaces():
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        # Query to retrieve all workspaces
        cur.execute("SELECT * FROM Workspaces")
        workspaces = cur.fetchall()

        # Format the response
        workspaces_list = []
        for workspace in workspaces:
            workspaces_list.append({
                'workspace_id': workspace[0],
                'workspace_name': workspace[1],
                'capacity': workspace[2],
                'location': workspace[3],
                'description': workspace[4]
            })

        return jsonify(workspaces_list), 200
    except psycopg2.Error as e:
        return jsonify({'message': 'Error retrieving workspaces', 'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()


# Route for making a new reservation
@app.route('/reservation', methods=['POST'])
def make_reservation():
    data = request.json
    user_id = data.get('user_id')
    workspace_id = data.get('workspace_id')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    reservation_date = data.get('reservation_date')

    try:
        conn = connect_to_db()
        cur = conn.cursor()

        # Check if the workspace is available for the given time slot
        cur.execute("""
            SELECT * FROM Reservations 
            WHERE workspace_id = %s 
            AND (%s, %s) OVERLAPS (start_time, end_time)
        """, (workspace_id, start_time, end_time))
        existing_reservation = cur.fetchone()

        if existing_reservation:
            return jsonify({'message': 'Workspace already reserved for this time slot.'}), 400

        # Make the reservation
        cur.execute("""
            INSERT INTO Reservations (user_id, workspace_id, start_time, end_time, reservation_date)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, workspace_id, start_time, end_time, reservation_date))
        conn.commit()
        return jsonify({'message': 'Reservation successfully created.'}), 201
    except psycopg2.Error as e:
        return jsonify({'message': 'Error creating reservation.', 'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

# Route for checking available time slots for a workspace
@app.route('/available-slots/<int:workspace_id>', methods=['GET'])
def check_available_slots(workspace_id):
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        # Query to find available time slots for the given workspace
        cur.execute("""
            SELECT * FROM Reservations 
            WHERE workspace_id = %s 
            AND reservation_date = CURRENT_DATE 
            ORDER BY start_time
        """, (workspace_id,))
        reservations = cur.fetchall()

        available_slots = []

        # Find gaps between reservations
        for i in range(len(reservations) - 1):
            end_time = reservations[i][4]  # end_time of current reservation
            next_start_time = reservations[i + 1][3]  # start_time of next reservation
            if end_time < next_start_time:
                available_slots.append({'start_time': end_time, 'end_time': next_start_time})

        return jsonify(available_slots), 200
    except psycopg2.Error as e:
        return jsonify({'message': 'Error retrieving available slots.', 'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

# Route for listing all reservations for a user
@app.route('/reservations/<int:user_id>', methods=['GET'])
def list_reservations(user_id):
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        # Query to retrieve all reservations for a user
        cur.execute("""
            SELECT * FROM Reservations 
            WHERE user_id = %s
        """, (user_id,))
        reservations = cur.fetchall()

        # Format the response
        reservations_list = []
        for reservation in reservations:
            reservations_list.append({
                'reservation_id': reservation[0],
                'workspace_id': reservation[2],
                'start_time': reservation[3],
                'end_time': reservation[4],
                'reservation_date': reservation[5]
            })

        return jsonify(reservations_list), 200
    except psycopg2.Error as e:
        return jsonify({'message': 'Error retrieving reservations.', 'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

# Route for deleting a reservation
@app.route('/reservation/<int:reservation_id>', methods=['DELETE'])
def delete_reservation(reservation_id):
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        # Check if reservation exists
        cur.execute("SELECT * FROM Reservations WHERE reservation_id = %s", (reservation_id,))
        reservation = cur.fetchone()
        if not reservation:
            return jsonify({'message': 'Reservation not found'}), 404

        # Delete reservation
        cur.execute("DELETE FROM Reservations WHERE reservation_id = %s", (reservation_id,))
        conn.commit()

        return jsonify({'message': 'Reservation deleted successfully'}), 200
    except psycopg2.Error as e:
        return jsonify({'message': 'Error deleting reservation', 'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

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
