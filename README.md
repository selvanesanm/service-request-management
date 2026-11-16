# Service Request Management System

A beginner-friendly CRUD application built using **Python, FastAPI, MySQL, HTML, CSS, and JavaScript Fetch API**. This project uses a separate frontend and backend without Jinja2 templates.

## Features

* Add, view, edit, and delete service requests.
* Search by customer name, email, phone, or case ID.
* Filter requests by status, region, and location.
* Display status summary cards.
* Pagination for service request listings.
* Reopen a request through the API (`POST /api/requests/{id}/reopen`).
* Export all service requests to CSV.
* Date filters: All Dates, Last 7 Days, Last 30 Days, Last 90 Days, Current Financial Year, Previous Financial Year, and Custom Date Range.
* Filter reopened requests only.
* Filter TAT-breached requests only.
* Display TAT status as Within TAT or TAT Breached.
* Print the service request table.
* Store all request details in a MySQL database.

## Technologies Used

| Technology | Purpose                        |
| ---------- | ------------------------------ |
| Python     | Backend programming            |
| FastAPI    | Backend API development        |
| MySQL      | Database management            |
| HTML       | Frontend structure             |
| CSS        | Frontend styling               |
| JavaScript | Frontend functionality         |
| Fetch API  | Frontend-backend communication |

## Project Structure

```text
srm/
│
├── main.py
├── schema.sql
├── reports.sql
├── requirements.txt
│
└── static/
    ├── index.html
    ├── style.css
    └── app.js
```

## 1. Create the Database

Open MySQL Command Line Client and execute:

```sql
SOURCE C:/full/path/to/srm/schema.sql;
```

Replace the example path with the actual location of your `srm` project folder.

**Important:** The `schema.sql` script drops the existing `service_request_db` database, creates it again, creates the `serviceInfo` table, and inserts 8 sample records.

Sample customer names:

* Arun Kumar
* Kaviya
* Murugan
* Priya
* Selvam
* Nandhini
* Vijay
* Deepa

**Warning:** Running this script permanently deletes all existing data in `service_request_db`. Back up important data before executing it. Run this script only once for a fresh setup.

### Run SQL Reports

To execute the SQL reports:

```sql
SOURCE C:/full/path/to/srm/reports.sql;
```

The `reports.sql` file includes:

* Complete service request listing
* Status-wise request count
* Region-wise request count
* Customer-wise request count
* Turnaround Time (TAT) reports
* Last 7 days report

**Database Name:** `service_request_db`

**Table Name:** `serviceInfo`

## 2. Install Python Packages

Open PowerShell inside the project folder and execute:

```powershell
python -m pip install -r requirements.txt
```

## 3. Configure MySQL Password

Set your actual MySQL password in PowerShell:

```powershell
$env:DB_PASSWORD="YOUR_MYSQL_PASSWORD"
```

Replace `YOUR_MYSQL_PASSWORD` with your actual MySQL password.

If your MySQL username is different from the application's default username, configure it:

```powershell
$env:DB_USER="root"
```

Do not upload actual passwords or private credentials to GitHub.

## 4. Run the Application

Start the FastAPI server:

```powershell
python -m uvicorn main:app --reload
```

Open the application in your browser:

**Frontend:** http://127.0.0.1:8000

**API Documentation:** http://127.0.0.1:8000/docs

## 5. API Operations

The application uses REST API endpoints to perform CRUD operations.

| HTTP Method | Operation | Purpose                   |
| ----------- | --------- | ------------------------- |
| GET         | Read      | View service requests     |
| POST        | Create    | Add a new service request |
| PUT         | Update    | Edit an existing request  |
| DELETE      | Delete    | Remove a service request  |
| POST        | Reopen    | Reopen a closed request   |

The reopen endpoint is:

```text
POST /api/requests/{id}/reopen
```

Refer to the FastAPI Swagger documentation at `/docs` for the actual available endpoints and request formats.

## 6. Understanding the Project Files

| File                | Description                                           |
| ------------------- | ----------------------------------------------------- |
| `main.py`           | FastAPI routes, MySQL connection, and CRUD operations |
| `static/index.html` | Frontend page structure and forms                     |
| `static/style.css`  | Styling and responsive design                         |
| `static/app.js`     | JavaScript functionality and Fetch API calls          |
| `schema.sql`        | Creates the database and table                        |
| `reports.sql`       | Contains SQL reports and queries                      |
| `requirements.txt`  | Required Python packages                              |

## 7. How Fetch API Works

When a user adds a service request:

1. JavaScript reads the form values.
2. The Fetch API sends the data to FastAPI using an HTTP POST request.
3. FastAPI receives the JSON data.
4. Python processes the request and inserts the data into MySQL.
5. FastAPI sends a response to JavaScript.
6. JavaScript refreshes the request listing to display the updated data.

The same communication approach is used for viewing, editing, deleting, and filtering service requests.

## 8. Turnaround Time (TAT)

Turnaround Time (TAT) measures the time taken to resolve a service request.

* For closed requests, TAT is calculated using the request time and closure time.
* For open requests, TAT is calculated using the request time and current time.
* The application displays whether a request is Within TAT or TAT Breached.
* The default TAT limit is 5 days.

You can change the TAT threshold using the `TAT_LIMIT_DAYS` environment variable before starting the application.

Example:

```powershell
$env:TAT_LIMIT_DAYS="5"
```

Confirm the required TAT threshold with the assignment or interviewer if a different SLA is specified.

## 9. Testing Checklist

Before submitting the project, verify the following functionalities:

* [ ] MySQL database connection
* [ ] Add service request
* [ ] View service requests
* [ ] Edit service request
* [ ] Delete service request
* [ ] Search functionality
* [ ] Status, region, and location filters
* [ ] Date filters
* [ ] Reopen request functionality
* [ ] TAT calculation and filtering
* [ ] CSV export
* [ ] Pagination
* [ ] Print table

## 10. Important Notes

* This is a beginner-friendly learning project.
* The frontend communicates with the backend using JavaScript Fetch API.
* FastAPI handles the backend operations.
* MySQL stores the service request information.
* The application does not use Jinja2 templates.
* Ensure all functionalities work correctly before presenting or submitting the project.

---

**Project:** Service Request Management System

**Backend:** Python + FastAPI

**Frontend:** HTML + CSS + JavaScript

**Database:** MySQL

