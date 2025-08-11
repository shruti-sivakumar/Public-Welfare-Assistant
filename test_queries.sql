-- 1. Total disbursement amount for PMAY in Gujarat during 2023
SELECT SUM(d.amount) AS total_disbursement
FROM disbursements d
JOIN enrollments e ON d.enrollment_id = e.enrollment_id
JOIN citizens c ON e.citizen_id = c.citizen_id
JOIN geographic g ON c.village_id = g.village_id
JOIN schemes s ON e.scheme_id = s.scheme_id
WHERE s.scheme_name = 'PMAY'
  AND g.state_name = 'Gujarat'
  AND YEAR(d.date) = 2023;

-- 2. Female MGNREGA beneficiaries under age 30 in Maharashtra
SELECT COUNT(*) AS female_under30_count
FROM citizens c
JOIN enrollments e ON c.citizen_id = e.citizen_id
JOIN geographic g ON c.village_id = g.village_id
JOIN schemes s ON e.scheme_id = s.scheme_id
WHERE s.scheme_name = 'MGNREGA'
  AND c.gender = 'Female'
  AND TIMESTAMPDIFF(YEAR, c.date_of_birth, CURDATE()) < 30
  AND g.state_name = 'Maharashtra';

-- 3. Citizens enrolled in two or more schemes
SELECT c.citizen_id, c.full_name, COUNT(DISTINCT e.scheme_id) AS scheme_count
FROM citizens c
JOIN enrollments e ON c.citizen_id = e.citizen_id
GROUP BY c.citizen_id, c.full_name
HAVING COUNT(DISTINCT e.scheme_id) >= 2;

-- 4. Ayushman Bharat beneficiaries with chronic kidney disease in Kerala
SELECT c.citizen_id, c.full_name
FROM citizens c
JOIN health_details h ON c.citizen_id = h.citizen_id
JOIN enrollments e ON c.citizen_id = e.citizen_id
JOIN schemes s ON e.scheme_id = s.scheme_id
JOIN geographic g ON c.village_id = g.village_id
WHERE s.scheme_name = 'Ayushman Bharat'
  AND h.chronic_condition = 'Chronic Kidney Disease'
  AND g.state_name = 'Kerala';

-- 5. Citizens with total disbursement above ₹50,000 in 2024
SELECT c.citizen_id, c.full_name, SUM(d.amount) AS total_amount
FROM citizens c
JOIN enrollments e ON c.citizen_id = e.citizen_id
JOIN disbursements d ON e.enrollment_id = d.enrollment_id
WHERE YEAR(d.date) = 2024
GROUP BY c.citizen_id, c.full_name
HAVING SUM(d.amount) > 50000;

-- 6. Number of Ujjwala beneficiaries without bank accounts
SELECT COUNT(DISTINCT c.citizen_id) AS no_bank_count
FROM citizens c
JOIN enrollments e ON c.citizen_id = e.citizen_id
JOIN schemes s ON e.scheme_id = s.scheme_id
LEFT JOIN bank_accounts b ON c.citizen_id = b.citizen_id
WHERE s.scheme_name = 'Ujjwala Yojana'
  AND b.account_number IS NULL;

-- 7. Officers with the highest number of verifications in 2024
SELECT o.officer_id, o.full_name, COUNT(*) AS verifications_count
FROM officers o
JOIN enrollments e ON o.officer_id = e.officer_id
WHERE YEAR(e.last_verification_date) = 2024
GROUP BY o.officer_id, o.full_name
ORDER BY verifications_count DESC
LIMIT 5;

-- 8. Disabled citizens enrolled in more than one scheme
SELECT c.citizen_id, c.full_name, COUNT(DISTINCT e.scheme_id) AS scheme_count
FROM citizens c
JOIN enrollments e ON c.citizen_id = e.citizen_id
WHERE c.disability_status = 'Yes'
GROUP BY c.citizen_id, c.full_name
HAVING COUNT(DISTINCT e.scheme_id) > 1;

-- 9. Top 5 districts by number of Ujjwala Yojana beneficiaries
SELECT g.district_name, COUNT(DISTINCT c.citizen_id) AS beneficiary_count
FROM citizens c
JOIN enrollments e ON c.citizen_id = e.citizen_id
JOIN schemes s ON e.scheme_id = s.scheme_id
JOIN geographic g ON c.village_id = g.village_id
WHERE s.scheme_name = 'Ujjwala Yojana'
GROUP BY g.district_name
ORDER BY beneficiary_count DESC
LIMIT 5;

-- 10. Citizens receiving benefits from all five schemes
SELECT c.citizen_id, c.full_name
FROM citizens c
JOIN enrollments e ON c.citizen_id = e.citizen_id
GROUP BY c.citizen_id, c.full_name
HAVING COUNT(DISTINCT e.scheme_id) = 5;
-- 11. State-wise total enrollment counts for all schemes in 2024
SELECT g.state_name, COUNT(DISTINCT e.enrollment_id) AS enrollment_count
FROM enrollments e
JOIN citizens c ON e.citizen_id = c.citizen_id
JOIN geographic g ON c.village_id = g.village_id
WHERE YEAR(e.enrollment_date) = 2024
GROUP BY g.state_name
ORDER BY enrollment_count DESC;

-- 12. Citizens with disability percentage above 70% enrolled in NSAP
SELECT c.citizen_id, c.full_name, h.disability_percentage
FROM citizens c
JOIN health_details h ON c.citizen_id = h.citizen_id
JOIN enrollments e ON c.citizen_id = e.citizen_id
JOIN schemes s ON e.scheme_id = s.scheme_id
WHERE s.scheme_name = 'NSAP'
  AND h.disability_percentage > 70;

-- 13. Average monthly disbursement per citizen in NSAP for Assam
SELECT AVG(monthly_amount) AS avg_monthly_disbursement
FROM (
    SELECT c.citizen_id, SUM(d.amount) / COUNT(DISTINCT MONTH(d.date)) AS monthly_amount
    FROM citizens c
    JOIN enrollments e ON c.citizen_id = e.citizen_id
    JOIN disbursements d ON e.enrollment_id = d.enrollment_id
    JOIN schemes s ON e.scheme_id = s.scheme_id
    JOIN geographic g ON c.village_id = g.village_id
    WHERE s.scheme_name = 'NSAP'
      AND g.state_name = 'Assam'
    GROUP BY c.citizen_id
) AS sub;

-- 14. PMAY enrollments in rural villages of Odisha
SELECT c.citizen_id, c.full_name, e.enrollment_date
FROM citizens c
JOIN enrollments e ON c.citizen_id = e.citizen_id
JOIN geographic g ON c.village_id = g.village_id
JOIN schemes s ON e.scheme_id = s.scheme_id
WHERE s.scheme_name = 'PMAY'
  AND g.state_name = 'Odisha'
  AND g.area_type = 'Rural';

-- 15. Citizens in multiple schemes with total disbursement above ₹1 lakh
SELECT c.citizen_id, c.full_name, COUNT(DISTINCT e.scheme_id) AS scheme_count, SUM(d.amount) AS total_amount
FROM citizens c
JOIN enrollments e ON c.citizen_id = e.citizen_id
JOIN disbursements d ON e.enrollment_id = d.enrollment_id
GROUP BY c.citizen_id, c.full_name
HAVING COUNT(DISTINCT e.scheme_id) > 1
  AND SUM(d.amount) > 100000;
