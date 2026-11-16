# Service Request Management System

A beginner-friendly CRUD application built using **Python, FastAPI, MySQL, HTML, CSS, and JavaScript Fetch API**.

## Features

- Add, view, edit, and delete service requests.
- Search by customer name, email, phone number, or case ID.
- Filter requests by status, region, and location.
- Display status summary cards.
- Pagination for service request records.
- Reopen closed service requests.
- Calculate Turnaround Time (TAT).
- Filter by date range and TAT status.
- Identify reopened requests and TAT-breached requests.
- Export service requests to CSV.
- Print service request records.
- Store data in MySQL database.

## Technologies Used

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, FastAPI
- **Database:** MySQL
- **API Communication:** JavaScript Fetch API

## Project Structure

```text
Service-Request-Management-System/
│
├── main.py
├── schema.sql
├── reports.sql
├── requirements.txt
├── run_windows.bat
│
└── static/
    ├── index.html
    ├── style.css
    └── app.js
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Service-Request-Management-System
```

### 2. Create the MySQL Database

Open MySQL Command Line Client and execute:

```sql
SOURCE C:/full/path/to/schema.sql;
```

This creates the `service_request_db` database and the required table.

**Note:** The schema script drops and recreates the existing database. Existing data will be deleted.

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure MySQL Password

In PowerShell:

```powershell
$env:DB_PASSWORD="YOUR_MYSQL_PASSWORD"
```

### 5. Run the Application

```bash
python -m uvicorn main:app --reload
```

### 6. Open the Application

Application: http://127.0.0.1:8000

API Documentation: http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/requests` | View service requests |
| GET | `/api/requests/{id}` | View a single request |
| POST | `/api/requests` | Add a new request |
| PUT | `/api/requests/{id}` | Update a request |
| DELETE | `/api/requests/{id}` | Delete a request |
| POST | `/api/requests/{id}/reopen` | Reopen a request |
| GET | `/api/export` | Export records to CSV |
| GET | `/api/health` | Check database connection |

## TAT Calculation

Turnaround Time (TAT) is calculated based on the time between the request creation and closure.

- Open requests: Calculated using the current time.
- Closed requests: Calculated using the closure time.
- Default TAT limit: 5 days.

## SQL Reports

The `reports.sql` file contains SQL queries for:

- Complete service request listing.
- Status-wise count.
- Region-wise count.
- Customer-wise count.
- TAT reports.
- Last 7 days reports.

## Project Objective

The objective of this project is to develop a service request management application that helps manage customer requests, track their status, monitor turnaround time, and generate reports using a simple frontend and backend architecture.

