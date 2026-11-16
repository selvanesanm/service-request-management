"""Service Request Management System - FastAPI backend (no Jinja2)."""
import csv
import io
import os
from datetime import date, datetime, timedelta

import pymysql
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI(title="Service Request Management System")
app.mount("/static", StaticFiles(directory="static"), name="static")

STATUSES = ["RECEIVED", "ACKNOWLEDGED", "WIP", "TECH-COMPLETED", "CLOSED"]
REGIONS = ["International", "North", "South", "SouthCentral", "West"]


# One function manages the MySQL connection for all database operations.
def run_sql(sql, values=(), one=False):
    connection = pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "root"),
        database=os.getenv("DB_NAME", "service_request_db"),
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, values)
            return cursor.fetchone() if one else cursor.fetchall()
    finally:
        connection.close()


# These are the fields accepted from the Add and Edit form.
class ServiceRequest(BaseModel):
    name: str
    email: str | None = None
    customerID: int | None = None
    companyName: str | None = None
    customerManual: bool = False
    phoneNumber: str | None = None
    productID: str | None = None
    productType: str | None = None
    issueDescription: str | None = None
    locationID: int | None = None
    locationName: str | None = None
    regionName: str | None = None
    issueImages: str | None = None
    requestTime: datetime | None = None
    subcategoryID: int | None = None
    subcategoryName: str | None = None
    status: str = "RECEIVED"
    userID: int | None = None
    remarks: str | None = None


def prepare_data(data):
    """Convert the form data into a normal dictionary for MySQL."""
    values = data.model_dump()
    values["customerManual"] = int(values["customerManual"])
    if values["regionName"] in REGIONS:
        values["regionID"] = REGIONS.index(values["regionName"]) + 1
    else:
        values["regionID"] = None
    if values["status"] not in STATUSES:
        raise HTTPException(status_code=400, detail="Choose a valid status")
    return values


@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.get("/api/requests")
def list_requests(
    search: str = "", status: str = "", region: str = "",
    location: str = "", date_preset: str = "all", date_from: str = "", date_to: str = "",
    reopened_only: bool = False, tat_breached: bool = False,
    page: int = Query(1, ge=1), limit: int = Query(25, ge=1, le=100),
):
    """Return the matching requests for the listing table."""
    conditions = ["1=1"]
    values = []
    if search:
        conditions.append("(name LIKE %s OR email LIKE %s OR phoneNumber LIKE %s OR companyName LIKE %s OR CAST(id AS CHAR) LIKE %s)")
        word = f"%{search}%"
        values.extend([word] * 5)
    if status:
        conditions.append("status=%s")
        values.append(status)
    if region:
        conditions.append("regionName=%s")
        values.append(region)
    if location:
        conditions.append("locationName=%s")
        values.append(location)
    if reopened_only:
        conditions.append("reopened=1")
    tat_limit = float(os.getenv("TAT_LIMIT_DAYS", "5"))
    if tat_breached:
        conditions.append("(TIMESTAMPDIFF(MINUTE, requestTime, COALESCE(closedAt, NOW())) / 1440) > %s")
        values.append(tat_limit)

    # Date filters use the requestTime column. The end date is inclusive.
    today = date.today()
    start_date = end_date = None
    if date_preset in ("7", "30", "90"):
        days = int(date_preset)
        start_date, end_date = today - timedelta(days=days - 1), today
    elif date_preset in ("this_fy", "last_fy"):
        fy_start_year = today.year if today.month >= 4 else today.year - 1
        if date_preset == "last_fy":
            fy_start_year -= 1
        start_date = date(fy_start_year, 4, 1)
        end_date = date(fy_start_year + 1, 3, 31)
    elif date_preset == "custom":
        try:
            if not date_from or not date_to:
                raise ValueError
            start_date = date.fromisoformat(date_from)
            end_date = date.fromisoformat(date_to)
            if start_date > end_date:
                raise ValueError
        except ValueError:
            raise HTTPException(status_code=400, detail="Choose a valid custom date range")

    if start_date and end_date:
        conditions.append("requestTime >= %s AND requestTime < %s")
        values.extend([start_date, end_date + timedelta(days=1)])

    where = " AND ".join(conditions)
    total = run_sql(f"SELECT COUNT(*) AS total FROM serviceInfo WHERE {where}", values, one=True)["total"]
    offset = (page - 1) * limit
    rows = run_sql(
        f"SELECT *, ROUND(TIMESTAMPDIFF(MINUTE, requestTime, COALESCE(closedAt, NOW())) / 1440, 2) AS tat, CASE WHEN (TIMESTAMPDIFF(MINUTE, requestTime, COALESCE(closedAt, NOW())) / 1440) > %s THEN 'TAT Breached' ELSE 'Within TAT' END AS tat_status FROM serviceInfo WHERE {where} ORDER BY requestTime DESC, id DESC LIMIT %s OFFSET %s",
        [tat_limit] + values + [limit, offset],
    )
    counts = run_sql(f"SELECT status, COUNT(*) AS total FROM serviceInfo WHERE {where} GROUP BY status", values)
    return {"items": rows, "total": total, "page": page, "pages": max(1, (total + limit - 1) // limit), "counts": counts}


@app.get("/api/requests/{request_id}")
def get_request(request_id: int):
    row = run_sql("SELECT * FROM serviceInfo WHERE id=%s", [request_id], one=True)
    if not row:
        raise HTTPException(status_code=404, detail="Service request not found")
    return row


@app.post("/api/requests")
def add_request(data: ServiceRequest, request: Request):
    values = prepare_data(data)
    values["reqIpAddr"] = request.client.host if request.client else None
    values["closedAt"] = datetime.now() if values["status"] == "CLOSED" else None
    columns = list(values.keys())
    marks = ", ".join(["%s"] * len(columns))
    sql = f"INSERT INTO serviceInfo ({', '.join(columns)}) VALUES ({marks})"
    run_sql(sql, list(values.values()))
    return {"message": "Request added successfully"}


@app.put("/api/requests/{request_id}")
def update_request(request_id: int, data: ServiceRequest):
    old = run_sql("SELECT id FROM serviceInfo WHERE id=%s", [request_id], one=True)
    if not old:
        raise HTTPException(status_code=404, detail="Service request not found")
    values = prepare_data(data)
    columns = list(values.keys())
    changes = ", ".join([f"{column}=%s" for column in columns])
    sql = f"UPDATE serviceInfo SET {changes}, closedAt=IF(%s='CLOSED', COALESCE(closedAt, NOW()), NULL) WHERE id=%s"
    run_sql(sql, list(values.values()) + [values["status"], request_id])
    return {"message": "Request updated successfully"}


@app.delete("/api/requests/{request_id}")
def delete_request(request_id: int):
    run_sql("DELETE FROM serviceInfo WHERE id=%s", [request_id])
    return {"message": "Request deleted successfully"}


@app.post("/api/requests/{request_id}/reopen")
def reopen_request(request_id: int):
    run_sql("UPDATE serviceInfo SET status='RECEIVED', closedAt=NULL, reopened=1 WHERE id=%s", [request_id])
    return {"message": "Request reopened"}


@app.get("/api/export")
def export_requests():
    rows = run_sql("SELECT id, requestTime, name, email, phoneNumber, productType, regionName, locationName, status FROM serviceInfo ORDER BY requestTime DESC")
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Case ID", "Requested At", "Name", "Email", "Phone", "Product", "Region", "Location", "Status"])
    for row in rows:
        writer.writerow([row["id"], row["requestTime"], row["name"], row["email"], row["phoneNumber"], row["productType"], row["regionName"], row["locationName"], row["status"]])
    return Response(output.getvalue(), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=service_requests.csv"})


@app.get("/api/health")
def health():
    run_sql("SELECT 1")
    return {"status": "ok", "database": "connected"}
