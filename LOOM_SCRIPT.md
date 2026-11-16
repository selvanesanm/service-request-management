# 5-minute Loom explanation

**0:00–0:35 — Introduction**  
Hello. Today I am explaining my Service Request Management System. I built it using Python FastAPI, MySQL, HTML, CSS and JavaScript. I used ChatGPT as an AI assistant during development.

**0:35–1:20 — Listing page**  
This is the listing page. It displays service requests with customer, product, location, region, status and turnaround time. I added search, filters, status summary cards and pagination.

**1:20–2:10 — Add and Edit**  
I can add a request using this form. JavaScript reads the form values and sends them to FastAPI using Fetch API. FastAPI stores the data in MySQL. I can also edit an existing request.

**2:10–2:50 — View and Delete**  
The View option displays the complete request details. Delete removes a request after confirmation.

**2:50–3:35 — Backend**  
In main.py, FastAPI provides API routes. GET reads requests, POST adds a request, PUT updates a request, and DELETE removes a request. PyMySQL connects Python to MySQL.

**3:35–4:30 — Frontend and database**  
index.html contains the page structure, style.css controls the design, and app.js calls the backend using fetch. schema.sql creates the qrCode database and serviceInfo table.

**4:30–5:00 — Conclusion**  
This project helped me understand CRUD operations, API communication, JavaScript Fetch API and MySQL connectivity. I used ChatGPT as an AI assistant. Thank you.
