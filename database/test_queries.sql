-- Test Queries - These will work with your actual schema


-- 1. Total disbursement amount by scheme in 2024 
SELECT s.name AS scheme_name, SUM(d.amount) AS total_disbursement_amount 
FROM disbursements d 
JOIN schemes s ON d.scheme_id = s.scheme_id 
WHERE YEAR(d.disbursed_on) = 2024 
GROUP BY s.scheme_id, s.name 
ORDER BY total_disbursement_amount DESC;

-- 2. Citizens enrolled in multiple schemes with their bank account details 
SELECT c.citizen_id, c.name AS citizen_name, c.aadhaar_no, ba.account_no, ba.bank_name, COUNT(DISTINCT e.scheme_id) AS scheme_count
FROM citizens c 
JOIN enrollments e ON c.citizen_id = e.citizen_id
LEFT JOIN bank_accounts ba ON c.citizen_id = ba.citizen_id 
GROUP BY c.citizen_id, c.name, c.aadhaar_no, ba.account_no, ba.bank_name
HAVING COUNT(DISTINCT e.scheme_id) > 1
ORDER BY scheme_count DESC;

-- 3.  Officers with the highest number of verifications in 2024
SELECT o.officer_id, o.name, COUNT(v.verification_id) AS verification_count
FROM officers o
JOIN verifications v ON o.officer_id = v.officer_id
WHERE YEAR(v.date) = 2024
GROUP BY o.officer_id, o.name
ORDER BY verification_count DESC
LIMIT 1;


-- 4. Female citizens aged 18-30 enrolled in MGNREGA employment scheme 
SELECT c.citizen_id, c.name, c.age, c.mobile_no, e.enrollment_date, e.status
FROM citizens c
JOIN enrollments e ON c.citizen_id = e.citizen_id
JOIN schemes s ON e.scheme_id = s.scheme_id
WHERE c.gender = 'Female' 
  AND c.age BETWEEN 18 AND 30
  AND (s.name LIKE '%MGNREGA%' OR s.name LIKE '%employment%')
ORDER BY c.age;

-- 5. Disbursement summary for citizens with chronic health conditions 
SELECT c.citizen_id, c.name, h.chronic_conditions, s.name AS scheme_name, 
       SUM(d.amount) AS total_received, COUNT(d.disbursement_id) AS payment_count
FROM citizens c
JOIN health_details h ON c.citizen_id = h.citizen_id
JOIN disbursements d ON c.citizen_id = d.citizen_id
JOIN schemes s ON d.scheme_id = s.scheme_id
WHERE h.chronic_conditions IS NOT NULL AND h.chronic_conditions != 'None'
GROUP BY c.citizen_id, c.name, h.chronic_conditions, s.scheme_id, s.name
ORDER BY total_received DESC;

-- 6. Village-wise enrollment statistics for Ayushman Bharat health scheme 
SELECT v.name AS village_name, dt.name AS district_name, st.name AS state_name,
       COUNT(e.enrollment_id) AS total_enrollments,
       COUNT(CASE WHEN e.status = 'Active' THEN 1 END) AS active_enrollments
FROM villages v
JOIN districts dt ON v.district_id = dt.district_id
JOIN states st ON dt.state_id = st.state_id
JOIN citizens c ON v.village_id = c.village_id
JOIN enrollments e ON c.citizen_id = e.citizen_id
JOIN schemes s ON e.scheme_id = s.scheme_id
WHERE s.name LIKE '%Ayushman%' OR s.name LIKE '%health%'
GROUP BY v.village_id, v.name, dt.district_id, dt.name, st.state_id, st.name
ORDER BY total_enrollments DESC;

-- 7. Citizens without bank accounts who received disbursements 
SELECT c.citizen_id, c.name, c.mobile_no, c.email, 
       SUM(d.amount) AS total_disbursed, d.payment_method
FROM citizens c
JOIN disbursements d ON c.citizen_id = d.citizen_id
LEFT JOIN bank_accounts ba ON c.citizen_id = ba.citizen_id
WHERE ba.account_id IS NULL
GROUP BY c.citizen_id, c.name, c.mobile_no, c.email, d.payment_method
ORDER BY total_disbursed DESC;

-- 8. Monthly disbursement trends for NSAP pension scheme in 2024 
SELECT MONTH(d.disbursed_on) AS month_number, 
       FORMAT(d.disbursed_on, 'MMMM') AS month_name,
       COUNT(d.disbursement_id) AS disbursement_count,
       SUM(d.amount) AS monthly_total,
       AVG(d.amount) AS average_amount
FROM disbursements d
JOIN schemes s ON d.scheme_id = s.scheme_id
WHERE (s.name LIKE '%NSAP%' OR s.name LIKE '%pension%') AND YEAR(d.disbursed_on) = 2024
GROUP BY MONTH(d.disbursed_on), FORMAT(d.disbursed_on, 'MMMM')
ORDER BY month_number;

-- 9. Citizens enrolled in all available schemes 
SELECT c.citizen_id, c.name, c.aadhaar_no, COUNT(DISTINCT e.scheme_id) AS schemes_enrolled
FROM citizens c
JOIN enrollments e ON c.citizen_id = e.citizen_id
GROUP BY c.citizen_id, c.name, c.aadhaar_no
HAVING COUNT(DISTINCT e.scheme_id) = (SELECT COUNT(*) FROM schemes)
ORDER BY c.name;

-- 10. Age group analysis of Ujjwala gas scheme beneficiaries 
SELECT 
    CASE 
        WHEN c.age < 25 THEN '18-24'
        WHEN c.age < 35 THEN '25-34' 
        WHEN c.age < 45 THEN '35-44'
        WHEN c.age < 55 THEN '45-54'
        WHEN c.age < 65 THEN '55-64'
        ELSE '65+'
    END AS age_group,
    COUNT(c.citizen_id) AS beneficiary_count,
    AVG(d.amount) AS average_disbursement
FROM citizens c
JOIN enrollments e ON c.citizen_id = e.citizen_id
JOIN schemes s ON e.scheme_id = s.scheme_id
LEFT JOIN disbursements d ON c.citizen_id = d.citizen_id AND d.scheme_id = s.scheme_id
WHERE s.name LIKE '%Ujjwala%' OR s.name LIKE '%gas%'
GROUP BY 
    CASE 
        WHEN c.age < 25 THEN '18-24'
        WHEN c.age < 35 THEN '25-34' 
        WHEN c.age < 45 THEN '35-44'
        WHEN c.age < 55 THEN '45-54'
        WHEN c.age < 65 THEN '55-64'
        ELSE '65+'
    END
ORDER BY beneficiary_count DESC;

-- 11. Verification backlog by officer and scheme 
SELECT o.name AS officer_name, o.designation, s.name AS scheme_name,
       COUNT(e.enrollment_id) AS pending_verifications,
       MIN(e.enrollment_date) AS oldest_pending,
       AVG(DATEDIFF(day, e.enrollment_date, GETDATE())) AS avg_days_pending
FROM officers o
JOIN enrollments e ON o.officer_id = e.verified_by
JOIN schemes s ON e.scheme_id = s.scheme_id
WHERE e.last_verified IS NULL OR e.status = 'Pending Verification'
GROUP BY o.officer_id, o.name, o.designation, s.scheme_id, s.name
ORDER BY pending_verifications DESC;

-- 12. State-wise gender distribution in housing schemes (PMAY) 
SELECT st.name AS state_name,
       COUNT(CASE WHEN c.gender = 'Male' THEN 1 END) AS male_beneficiaries,
       COUNT(CASE WHEN c.gender = 'Female' THEN 1 END) AS female_beneficiaries,
       COUNT(CASE WHEN c.gender = 'Other' THEN 1 END) AS other_gender,
       COUNT(c.citizen_id) AS total_beneficiaries,
       ROUND(COUNT(CASE WHEN c.gender = 'Female' THEN 1 END) * 100.0 / COUNT(c.citizen_id), 2) AS female_percentage
FROM citizens c
JOIN villages v ON c.village_id = v.village_id
JOIN districts dt ON v.district_id = dt.district_id
JOIN states st ON dt.state_id = st.state_id
JOIN enrollments e ON c.citizen_id = e.citizen_id
JOIN schemes s ON e.scheme_id = s.scheme_id
WHERE s.name LIKE '%PMAY%' OR s.name LIKE '%housing%'
GROUP BY st.state_id, st.name
ORDER BY total_beneficiaries DESC;

-- 13. Count disabled citizens with disability above 70% by state 
SELECT st.name AS state_name, COUNT(c.citizen_id) AS disabled_citizens_count
FROM citizens c
JOIN health_details h ON c.citizen_id = h.citizen_id
JOIN villages v ON c.village_id = v.village_id
JOIN districts dt ON v.district_id = dt.district_id
JOIN states st ON dt.state_id = st.state_id
WHERE h.disability_status LIKE '%80%' OR h.disability_status LIKE '%90%' OR h.disability_status LIKE '%100%'
GROUP BY st.state_id, st.name
ORDER BY disabled_citizens_count DESC;

-- 14. Complex multi-scheme analysis - Citizens receiving maximum benefits 
SELECT TOP 10 
    c.citizen_id, c.name, c.aadhaar_no, c.gender, c.age,
    st.name AS state_name, dt.name AS district_name,
    COUNT(DISTINCT e.scheme_id) AS schemes_count,
    SUM(d.amount) AS total_amount_received,
    MAX(d.disbursed_on) AS last_disbursement_date
FROM citizens c
JOIN villages v ON c.village_id = v.village_id
JOIN districts dt ON v.district_id = dt.district_id
JOIN states st ON dt.state_id = st.state_id
JOIN enrollments e ON c.citizen_id = e.citizen_id
JOIN schemes s ON e.scheme_id = s.scheme_id
LEFT JOIN disbursements d ON c.citizen_id = d.citizen_id
GROUP BY c.citizen_id, c.name, c.aadhaar_no, c.gender, c.age, st.state_id, st.name, dt.district_id, dt.name
HAVING COUNT(DISTINCT e.scheme_id) >= 3 AND SUM(d.amount) > 75000
ORDER BY total_amount_received DESC, schemes_count DESC;