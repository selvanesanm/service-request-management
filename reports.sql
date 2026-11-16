USE service_request_db;

-- 1. Full service request listing
SELECT * FROM serviceInfo ORDER BY requestTime DESC;

-- 2. Status-wise request count
SELECT status, COUNT(*) AS total_requests
FROM serviceInfo GROUP BY status ORDER BY total_requests DESC;

-- 3. Region-wise request count
SELECT regionName, COUNT(*) AS total_requests
FROM serviceInfo GROUP BY regionName ORDER BY total_requests DESC;

-- 4. Customer-wise request count
SELECT customerID, name, companyName, phoneNumber, COUNT(*) AS request_count
FROM serviceInfo GROUP BY customerID, name, companyName, phoneNumber
ORDER BY request_count DESC;

-- 5. Turnaround time (TAT) in days
SELECT id, name, status,
       ROUND(TIMESTAMPDIFF(MINUTE, requestTime, COALESCE(closedAt, NOW())) / 1440, 2) AS tat_days
FROM serviceInfo ORDER BY tat_days DESC;

-- 6. Requests received in the last 7 days
SELECT id, name, productType, issueDescription, requestTime, status
FROM serviceInfo WHERE requestTime >= NOW() - INTERVAL 7 DAY
ORDER BY requestTime DESC;
