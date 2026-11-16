// Frontend JavaScript: all data is loaded and saved through the FastAPI JSON API.
let currentPage = 1;
let editingId = null;
const statuses = ["RECEIVED", "ACKNOWLEDGED", "WIP", "TECH-COMPLETED", "CLOSED"];

function showMessage(message, error = false) {
  const box = document.getElementById("notice");
  box.textContent = message;
  box.className = error ? "msg err" : "msg ok";
  box.hidden = false;
  setTimeout(() => box.hidden = true, 3500);
}

function showList() {
  document.getElementById("listPage").hidden = false;
  document.getElementById("formPage").hidden = true;
  document.getElementById("viewPage").hidden = true;
  editingId = null;
  loadRequests(currentPage);
}

function showForm(record = null) {
  editingId = record ? record.id : null;
  const form = document.getElementById("requestForm");
  form.reset();
  document.getElementById("formTitle").textContent = record ? "Edit service request" : "Add service request";
  if (record) {
    for (const [key, value] of Object.entries(record)) {
      const field = form.elements[key];
      if (!field) continue;
      if (field.type === "checkbox") field.checked = Boolean(value);
      else if (key === "requestTime" && value) field.value = value.replace(" ", "T").slice(0, 16);
      else if (value !== null) field.value = value;
    }
  } else {
    form.elements.status.value = "RECEIVED";
    form.elements.requestTime.value = new Date().toISOString().slice(0, 16);
  }
  document.getElementById("listPage").hidden = true;
  document.getElementById("viewPage").hidden = true;
  document.getElementById("formPage").hidden = false;
  window.scrollTo(0, 0);
}

async function loadRequests(page = 1) {
  currentPage = page;
  const params = new URLSearchParams({
    search: document.getElementById("search").value,
    status: document.getElementById("status").value,
    region: document.getElementById("region").value,
    location: document.getElementById("location").value,
    date_preset: document.getElementById("datePreset").value,
    date_from: document.getElementById("dateFrom").value,
    date_to: document.getElementById("dateTo").value,
    reopened_only: document.getElementById("reopenedOnly").checked,
    tat_breached: document.getElementById("tatBreached").checked,
    page: currentPage
  });
  try {
    const response = await fetch(`/api/requests?${params}`);
    if (!response.ok) throw new Error("Could not load requests");
    const data = await response.json();
    drawRows(data.items);
    drawStatusCards(data.counts);
    document.getElementById("totalLabel").textContent = `${data.total} requests`;
    document.getElementById("pageLabel").textContent = `Page ${data.page} of ${data.pages}`;
    document.getElementById("previous").disabled = data.page <= 1;
    document.getElementById("next").disabled = data.page >= data.pages;
  } catch (error) {
    showMessage(error.message, true);
  }
}

function drawStatusCards(counts) {
  const countMap = Object.fromEntries(counts.map(item => [item.status, item.total]));
  document.getElementById("statusCards").innerHTML = statuses.map(status =>
    `<div class="stage"><b>${countMap[status] || 0}</b><span>${status}</span></div>`
  ).join("");
}

function drawRows(rows) {
  const body = document.getElementById("requestRows");
  if (!rows.length) {
    body.innerHTML = '<tr><td colspan="9" class="empty">No service requests found.</td></tr>';
    return;
  }
  body.innerHTML = rows.map(row => {
    const tat = row.tat === null ? "-" : Number(row.tat).toFixed(2);
    const date = row.requestTime ? new Date(row.requestTime).toLocaleString() : "-";
    const statusClass = row.status.toLowerCase().replaceAll("-", "-");
    return `<tr>
      <td><span class="case">S${row.id}</span></td>
      <td><b>${safe(row.name)}</b><small>${safe(row.email || "")}</small></td>
      <td>${safe(row.productType || "-")}<small>${safe(row.subcategoryName || row.issueDescription || "")}</small></td>
      <td>${safe(row.locationName || "-")}</td><td>${safe(row.regionName || "-")}</td><td>${safe(date)}</td>
      <td><span class="pill ${statusClass.toLowerCase()}">${safe(row.status || "-")}</span></td><td>${tat}<small class="tat-label ${row.tat_status === "TAT Breached" ? "tat-breached" : "tat-within"}">${safe(row.tat_status || "-")}</small></td>
      <td><div class="act"><button onclick="viewRequest(${row.id})">View</button><button onclick="editRequest(${row.id})">Edit</button><button class="danger" onclick="removeRequest(${row.id})">Delete</button>${row.status === "CLOSED" ? `<button onclick="reopenRequest(${row.id})">Reopen</button>` : ""}</div></td>
    </tr>`;
  }).join("");
}

// Escape database text before placing it inside the HTML table.
function safe(value) {
  return String(value ?? "").replace(/[&<>"']/g, char => ({"&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#39;"}[char]));
}

async function saveRequest(event) {
  event.preventDefault();
  const form = event.target;
  const data = {};
  for (const [key, value] of new FormData(form).entries()) data[key] = value;
  data.customerManual = form.elements.customerManual.checked;
  for (const key of ["customerID", "subcategoryID", "locationID", "userID"]) data[key] = data[key] ? Number(data[key]) : null;
  data.requestTime = data.requestTime || null;
  const url = editingId ? `/api/requests/${editingId}` : "/api/requests";
  const method = editingId ? "PUT" : "POST";
  try {
    const response = await fetch(url, {method, headers: {"Content-Type": "application/json"}, body: JSON.stringify(data)});
    const result = await response.json();
    if (!response.ok) throw new Error(result.detail || "Could not save request");
    showMessage(result.message);
    showList();
  } catch (error) { showMessage(error.message, true); }
}

async function editRequest(id) {
  const response = await fetch(`/api/requests/${id}`);
  if (!response.ok) return showMessage("Could not open this request", true);
  showForm(await response.json());
}

async function viewRequest(id) {
  const response = await fetch(`/api/requests/${id}`);
  if (!response.ok) return showMessage("Could not open this request", true);
  const record = await response.json();
  const fields = ["name", "email", "phoneNumber", "customerID", "companyName", "productID", "productType", "subcategoryName", "locationName", "regionName", "issueDescription", "remarks", "requestTime", "status"];
  document.getElementById("requestDetails").innerHTML = `<h3>Case S${record.id}</h3><dl>${fields.map(key => `<dt>${key}</dt><dd>${safe(record[key] ?? "-")}</dd>`).join("")}</dl><div class="form-actions"><button class="primary" onclick="editRequest(${record.id})">Edit request</button></div>`;
  document.getElementById("listPage").hidden = true;
  document.getElementById("formPage").hidden = true;
  document.getElementById("viewPage").hidden = false;
}

async function removeRequest(id) {
  if (!confirm(`Delete service request S${id}?`)) return;
  const response = await fetch(`/api/requests/${id}`, {method: "DELETE"});
  const result = await response.json();
  if (!response.ok) return showMessage(result.detail || "Delete failed", true);
  showMessage(result.message);
  loadRequests(currentPage);
}

async function reopenRequest(id) {
  const response = await fetch(`/api/requests/${id}/reopen`, {method: "POST"});
  const result = await response.json();
  if (!response.ok) return showMessage(result.detail || "Reopen failed", true);
  showMessage(result.message);
  loadRequests(currentPage);
}

function toggleCustomDates() {
  const show = document.getElementById("datePreset").value === "custom";
  document.getElementById("customFromWrap").hidden = !show;
  document.getElementById("customToWrap").hidden = !show;
}

function resetFilters() {
  document.getElementById("search").value = "";
  document.getElementById("status").value = "";
  document.getElementById("region").value = "";
  document.getElementById("location").value = "";
  document.getElementById("datePreset").value = "all";
  document.getElementById("dateFrom").value = "";
  document.getElementById("dateTo").value = "";
  document.getElementById("reopenedOnly").checked = false;
  document.getElementById("tatBreached").checked = false;
  toggleCustomDates();
  loadRequests(1);
}

function changePage(amount) { loadRequests(currentPage + amount); }
function downloadCSV() { window.location.href = "/api/export"; }
function printTable() { window.print(); }
loadRequests();
