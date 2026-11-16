# Service Request Management System

A beginner-friendly CRUD project using **Python, FastAPI, MySQL, HTML, CSS and JavaScript Fetch API**. It does not use Jinja2.

## Features
- Add, view, edit and delete service requests
- Search by customer name, email, phone or case ID
- Filter by status, region and location
- Status summary cards and pagination
- Reopen a request through the API (`POST /api/requests/{id}/reopen`)
- Export all requests to CSV
- MySQL database storage

## 1. Create the database
Open MySQL Command Line Client and run:

```sql
SOURCE C:/full/path/to/Service_Request_Management_System_No_Jinja2/schema.sql;
```

Use the actual folder path on your computer. The script **drops the existing `service_request_db` database**, creates it again, creates the `serviceInfo` table, and inserts 8 sample records with English-letter customer names (Arun Kumar, Kaviya, Murugan, Priya, Selvam, Nandhini, Vijay and Deepa). **Warning: all existing data in `service_request_db` will be permanently deleted.** Back up anything important first. Run `schema.sql` only once for a fresh setup.

To view SQL reports, run:

```sql
SOURCE C:/full/path/to/Service_Request_Management_System_No_Jinja2/reports.sql;
```

`reports.sql` includes full listing, status-wise count, region-wise count, customer-wise count, TAT and last-7-days reports.

The database is named `service_request_db` because it belongs to this project. The table remains `serviceInfo` so the FastAPI code and assignment-style field structure work together. The SQL file includes customer, company, product, issue, location, region, status, request time, IP address, subcategory, user, remarks, closure and reopen fields.

## 2. Install Python packages
Open PowerShell inside this project folder:

```powershell
python -m pip install -r requirements.txt
```

## 3. Set your MySQL password
Use your actual MySQL password (do not copy the example literally):

```powershell
$env:DB_PASSWORD="YOUR_MYSQL_PASSWORD"
```

If your MySQL username is not `root`, set it too:

```powershell
$env:DB_USER="root"
```

## 4. Start the project
```powershell
python -m uvicorn main:app --reload
```
Open http://127.0.0.1:8000 in Chrome. API documentation is at http://127.0.0.1:8000/docs.

## Understand the project
- `main.py`: FastAPI routes, MySQL connection, and CRUD operations.
- `static/index.html`: The page structure and forms.
- `static/style.css`: The design and responsive layout.
- `static/app.js`: Uses `fetch()` to call the backend and update the page.
- `schema.sql`: Creates the MySQL database and table.

## Simple explanation of Fetch
When a user adds a request, JavaScript reads the form values and sends them to FastAPI using `fetch()` with a POST request. FastAPI receives the JSON, inserts it into MySQL, and sends a response. JavaScript then refreshes the listing.

## Important
This is a learning project. Before submitting, test Add, View, Edit, Delete, filters, CSV export and database connection on your own computer. The TAT value is calculated in days from request time to close time (or current time for open requests). Confirm your MySQL date/time values are correct before presenting TAT in the interview.

## Additional assignment filters and listing tools
- Date presets: all dates, last 7/30/90 days, current financial year, previous financial year, and custom date range.
- Reopened only: filters records where `reopened = 1`.
- TAT breached only: filters requests whose TAT exceeds `TAT_LIMIT_DAYS` (default 5 days).
- TAT status: each listing row displays `Within TAT` or `TAT Breached`.
- Print table: use the Print table button on the listing page.

You can change the TAT threshold by setting the `TAT_LIMIT_DAYS` environment variable before starting the app. The default is 5 days; confirm the threshold with your assignment/interviewer if they specify another SLA.
