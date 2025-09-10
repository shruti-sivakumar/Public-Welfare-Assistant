-- =====================================================
-- TEST QUERIES FOR WELFARE SCHEME DATABASE
-- Fully aligned with schema.sql
-- =====================================================

-- 1. Total disbursement amount for PMAY in Gujarat during 2023
SELECT SUM(d.amount) AS total_disbursement
FROM disbursements d
JOIN citizens c ON d.citizen_id = c.citizen_id
JOIN schemes s ON d.scheme_id = s.scheme_id
JOIN villages v ON c.village_id = v.village_id
JOIN districts dist ON v.district_id = dist.district_id
JOIN states st ON dist.state_id = st.state_id
WHERE s.name = 'PMAY'
  AND st.name = 'Gujarat'
  AND YEAR(d.disbursed_on) = 2023;

-- 2. Female MGNREGA beneficiaries under age 30 in Maharashtra
SELECT COUNT(*) AS female_under30_count
FROM citizens c
JOIN enrollments e ON c.citizen_id = e.citizen_id
JOIN schemes s ON e.scheme_id = s.scheme_id
JOIN villages v ON c.village_id = v.village_id
JOIN districts dist ON v.district_id = dist.district_id
JOIN states st ON dist.state_id = st.state_id
WHERE s.name = 'MGNREGA'
  AND c.gender = 'Female'
  AND c.age < 30
  AND st.name = 'Maharashtra';

-- 3. Citizens enrolled in two or more schemes
SELECT c.citizen_id, c.name, COUNT(DISTINCT e.scheme_id) AS scheme_count
FROM citizens c
JOIN enrollments e ON c.citizen_id = e.citizen_id
GROUP BY c.citizen_id, c.name
HAVING COUNT(DISTINCT e.scheme_id) >= 2;

-- 4. Ayushman Bharat beneficiaries with chronic kidney disease in Kerala
SELECT c.citizen_id, c.name
FROM citizens c
JOIN health_details h ON c.citizen_id = h.citizen_id
JOIN enrollments e ON c.citizen_id = e.citizen_id
JOIN schemes s ON e.scheme_id = s.scheme_id
JOIN villages v ON c.village_id = v.village_id
JOIN districts dist ON v.district_id = dist.district_id
JOIN states st ON dist.state_id = st.state_id
WHERE s.name = 'Ayushman Bharat - PMJAY'
  AND h.chronic_conditions LIKE '%Chronic Kidney Disease%'
  AND st.name = 'Kerala';

-- 5. Citizens with total disbursement above ₹50,000 in 2024
SELECT c.citizen_id, c.name, SUM(d.amount) AS total_amount
FROM citizens c
JOIN disbursements d ON c.citizen_id = d.citizen_id
WHERE YEAR(d.disbursed_on) = 2024
GROUP BY c.citizen_id, c.name
HAVING SUM(d.amount) > 50000;

-- 6. Number of Ujjwala beneficiaries without bank accounts
SELECT COUNT(DISTINCT c.citizen_id) AS no_bank_count
FROM citizens c
JOIN enrollments e ON c.citizen_id = e.citizen_id
JOIN schemes s ON e.scheme_id = s.scheme_id
LEFT JOIN bank_accounts b ON c.citizen_id = b.citizen_id
WHERE s.name = 'Ujjwala Yojana'
  AND b.account_id IS NULL;

-- 7. Officers with the highest number of verifications in 2024
SELECT o.officer_id, o.name, COUNT(*) AS verifications_count
FROM officers o
JOIN enrollments e ON o.officer_id = e.verified_by
WHERE YEAR(e.last_verified_on) = 2024
GROUP BY o.officer_id, o.name
ORDER BY verifications_count DESC
LIMIT 5;

-- 8. Disabled citizens enrolled in more than one scheme
SELECT c.citizen_id, c.name, COUNT(DISTINCT e.scheme_id) AS scheme_count
FROM citizens c
JOIN health_details h ON c.citizen_id = h.citizen_id
JOIN enrollments e ON c.citizen_id = e.citizen_id
WHERE h.disability_status IS NOT NULL
  AND h.disability_status <> 'None'
GROUP BY c.citizen_id, c.name
HAVING COUNT(DISTINCT e.scheme_id) > 1;

-- 9. Top 5 districts by number of Ujjwala Yojana beneficiaries
SELECT dist.name AS district_name, COUNT(DISTINCT c.citizen_id) AS beneficiary_count
FROM citizens c
JOIN enrollments e ON c.citizen_id = e.citizen_id
JOIN schemes s ON e.scheme_id = s.scheme_id
JOIN villages v ON c.village_id = v.village_id
JOIN districts dist ON v.district_id = dist.district_id
WHERE s.name = 'Ujjwala Yojana'
GROUP BY dist.name
ORDER BY beneficiary_count DESC
LIMIT 5;

-- 10. Citizens receiving benefits from all five schemes
SELECT c.citizen_id, c.name
FROM citizens c
JOIN enrollments e ON c.citizen_id = e.citizen_id
GROUP BY c.citizen_id, c.name
HAVING COUNT(DISTINCT e.scheme_id) = 5;

-- 11. State-wise total enrollment counts for all schemes in 2024
SELECT st.name AS state_name, COUNT(DISTINCT e.enrollment_id) AS enrollment_count
FROM enrollments e
JOIN citizens c ON e.citizen_id = c.citizen_id
JOIN villages v ON c.village_id = v.village_id
JOIN districts dist ON v.district_id = dist.district_id
JOIN states st ON dist.state_id = st.state_id
WHERE YEAR(e.enrollment_date) = 2024
GROUP BY st.name
ORDER BY enrollment_count DESC;

-- 12. Citizens with disabilities enrolled in NSAP
SELECT c.citizen_id, c.name, h.disability_status
FROM citizens c
JOIN health_details h ON c.citizen_id = h.citizen_id
JOIN enrollments e ON c.citizen_id = e.citizen_id
JOIN schemes s ON e.scheme_id = s.scheme_id
WHERE s.name = 'NSAP'
  AND h.disability_status IS NOT NULL
  AND h.disability_status <> 'None';

-- 13. Average monthly disbursement per citizen in NSAP for Assam
SELECT AVG(monthly_amount) AS avg_monthly_disbursement
FROM (
    SELECT c.citizen_id, SUM(d.amount) / COUNT(DISTINCT MONTH(d.disbursed_on)) AS monthly_amount
    FROM citizens c
    JOIN disbursements d ON c.citizen_id = d.citizen_id
    JOIN schemes s ON d.scheme_id = s.scheme_id
    JOIN villages v ON c.village_id = v.village_id
    JOIN districts dist ON v.district_id = dist.district_id
    JOIN states st ON dist.state_id = st.state_id
    WHERE s.name = 'NSAP'
      AND st.name = 'Assam'
    GROUP BY c.citizen_id
) AS sub;

-- 14. PMAY enrollments in rural villages of Odisha
SELECT c.citizen_id, c.name, e.enrollment_date
FROM citizens c
JOIN enrollments e ON c.citizen_id = e.citizen_id
JOIN villages v ON c.village_id = v.village_id
JOIN districts dist ON v.district_id = dist.district_id
JOIN states st ON dist.state_id = st.state_id
JOIN schemes s ON e.scheme_id = s.scheme_id
WHERE s.name = 'PMAY'
  AND st.name = 'Odisha';

-- 15. Citizens in multiple schemes with total disbursement above ₹1 lakh
SELECT c.citizen_id, c.name, COUNT(DISTINCT e.scheme_id) AS scheme_count, SUM(d.amount) AS total_amount
FROM citizens c
JOIN enrollments e ON c.citizen_id = e.citizen_id
JOIN disbursements d ON c.citizen_id = d.citizen_id
GROUP BY c.citizen_id, c.name
HAVING COUNT(DISTINCT e.scheme_id) > 1
  AND SUM(d.amount) > 100000;
