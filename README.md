## Services

### 1. Portainer

- **Description**: Portainer is a lightweight management UI for Docker and Kubernetes environments.
- **Access**: Access the Portainer dashboard at [https://portainer-reservation-app.com](https://portainer-reservation-app.com).
- **Credentials**: No credentials required.

### 2. PostgreSQL Database

- **Description**: PostgreSQL database for storing application data.
- **Credentials**:
  - Username: postgres
  - Password: postgres
  - Database: database

### 3. Authentication Service

- **Description**: Microservice for user authentication and authorization.
- **Dependencies**: Depends on PostgreSQL database.
- **Access**: Access the Authentication Service at [https://auth-reservation-app.com](https://auth-reservation-app.com).
- **Endpoints**:
  - `/auth/register`: Register a new user.
  - `/auth/login`: User login to generate authentication token.
  - `/auth/logout`: User logout to invalidate token.
  - `/auth/users`: Retrieve users data.

### 4. Flask Service

- **Description**: Microservice providing backend functionality.
- **Dependencies**: Depends on PostgreSQL database.
- **Endpoints**:
  - `/api/workspace`: Create a new workspace.
  - `/api/workspace/<workspace_id>`: Delete a workspace.
  - `/api/workspaces`: List all workspaces.
  - `/api/reservation`: Make a new reservation.
  - `/api/reservations/<user_id>`: List all reservations for a user.
  - `/api/reservation/<reservation_id>`: Delete a reservation.
  - `/api/available-slots/<workspace_id>`: Check available time slots for a workspace.

### 5. Grafana

- **Description**: Grafana for monitoring and analyzing metrics.
- **Access**: Access Grafana dashboard at [https://grafana-reservation-app.com](https://grafana-reservation-app.com).
- **Credentials**:
  - Username: admin
  - Password: admin

## Setup Instructions

Are found in azure/README.md and manifests/README.md.