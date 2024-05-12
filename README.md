## Services

### 1. Portainer

- **Description**: Portainer is a lightweight management UI for Docker environments.
- **Access**: Access the Portainer dashboard at [http://localhost:9443](http://localhost:9443).
- **Credentials**: No credentials required.

### 2. PostgreSQL Database

- **Description**: PostgreSQL database for storing application data.
- **Credentials**:
  - Username: postgres
  - Password: postgres
  - Database: database

### 3. IO Service

- **Description**: Microservice for handling IO operations.
- **Dependencies**: Depends on PostgreSQL database.
- **Endpoints**:
  - `/io/users`: Retrieve users data.
  - `/io/reservations`: Retrieve reservations data.
  - `/io/workspaces`: Retrieve workspaces data.

### 4. Authentication Service

- **Description**: Microservice for user authentication and authorization.
- **Dependencies**: Depends on PostgreSQL database.
- **Endpoints**:
  - `/auth/register`: Register a new user.
  - `/auth/login`: User login to generate authentication token.
  - `/auth/logout`: User logout to invalidate token.
  - `/auth/users`: Retrieve users data.

### 5. Flask Service

- **Description**: Microservice providing backend functionality.
- **Dependencies**: Depends on IO Service for data operations.
- **Endpoints**:
  - `/api/workspace`: Create a new workspace.
  - `/api/workspace/<workspace_id>`: Delete a workspace.
  - `/api/workspaces`: List all workspaces.
  - `/api/reservation`: Make a new reservation.
  - `/api/reservations/<user_id>`: List all reservations for a user.
  - `/api/reservation/<reservation_id>`: Delete a reservation.
  - `/api/available-slots/<workspace_id>`: Check available time slots for a workspace.

### 6. Kong

- **Description**: Kong API gateway for managing API traffic.
- **Routes**:
  - Authentication Service endpoints.
    - `/auth/register`
    - `/auth/login`
    - `/auth/logout`
    - `/auth/users`
  - Flask Service endpoints.
    - `/api/workspace`
    - `/api/workspace/<workspace_id>`
    - `/api/workspaces`
    - `/api/reservation`
    - `/api/reservations/<user_id>`
    - `/api/reservation/<reservation_id>`
    - `/api/available-slots/<workspace_id>`
  - IO Service endpoints.
    - `/io/users`
    - `/io/reservations`
    - `/io/workspaces`
- **Access**: Routes can be accessed through Kong API gateway.
  - Example: To access the authentication service login endpoint, use [http://localhost:80/auth/login](http://localhost:80/auth/login).

### 7. Grafana

- **Description**: Grafana for monitoring and analyzing metrics.
- **Access**: Access Grafana dashboard at [http://localhost:3000](http://localhost:3000).
- **Credentials**:
  - Username: admin
  - Password: admin

### 8. Prometheus

- **Description**: Prometheus for monitoring metrics.
- **Access**: Access Prometheus dashboard at [http://localhost:9090](http://localhost:9090).

## Setup Instructions

Install docker\*, download the docker-compose.yml file and run `docker deploy -c docker-compose.yml stack-name`.
