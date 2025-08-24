CREATE TABLE `citizens` (
  `citizen_id` int PRIMARY KEY,
  `aadhaar_no` varchar(255) UNIQUE NOT NULL,
  `name` varchar(255) NOT NULL,
  `gender` varchar(255) NOT NULL,
  `age` int NOT NULL,
  `mobile_no` varchar(255),
  `email` varchar(255),
  `village_id` int NOT NULL
);

CREATE TABLE `officers` (
  `officer_id` int PRIMARY KEY,
  `name` varchar(255) NOT NULL,
  `designation` varchar(255) NOT NULL,
  `access_level` varchar(255) NOT NULL,
  `email` varchar(255),
  `district_id` int NOT NULL
);

CREATE TABLE `schemes` (
  `scheme_id` int PRIMARY KEY,
  `name` varchar(255) NOT NULL,
  `description` text,
  `sector` varchar(255),
  `frequency` varchar(255),
  `benefit_type` varchar(255)
);

CREATE TABLE `enrollments` (
  `enrollment_id` int PRIMARY KEY,
  `citizen_id` int NOT NULL,
  `scheme_id` int NOT NULL,
  `enrollment_date` date NOT NULL,
  `status` varchar(255) NOT NULL,
  `last_verified_on` date,
  `verified_by` int
);

CREATE TABLE `disbursements` (
  `disbursement_id` int PRIMARY KEY,
  `citizen_id` int NOT NULL,
  `scheme_id` int NOT NULL,
  `amount` decimal NOT NULL,
  `status` varchar(255) NOT NULL,
  `disbursed_on` date NOT NULL,
  `approved_by` int,
  `payment_mode` varchar(255) NOT NULL
);

CREATE TABLE `health_details` (
  `citizen_id` int PRIMARY KEY,
  `chronic_conditions` text,
  `disability_status` varchar(255)
);

CREATE TABLE `bank_accounts` (
  `account_id` int PRIMARY KEY,
  `citizen_id` int NOT NULL,
  `account_no` varchar(255) NOT NULL,
  `bank_name` varchar(255) NOT NULL,
  `ifsc_code` varchar(255) NOT NULL
);

CREATE TABLE `scheme_eligibility` (
  `scheme_id` int PRIMARY KEY,
  `min_age` int,
  `max_age` int,
  `gender` varchar(255),
  `category_required` varchar(255),
  `min_income` decimal,
  `disability_required` varchar(255)
);

CREATE TABLE `eligibility_log` (
  `log_id` int PRIMARY KEY,
  `citizen_id` int NOT NULL,
  `scheme_id` int NOT NULL,
  `eligibility_result` varchar(255) NOT NULL,
  `reason` text,
  `checked_on` datetime NOT NULL
);

CREATE TABLE `access_log` (
  `log_id` int PRIMARY KEY,
  `officer_id` int NOT NULL,
  `entity_accessed` varchar(255) NOT NULL,
  `action` varchar(255) NOT NULL,
  `timestamp` datetime NOT NULL,
  `query_text` text,
  `target_id` int
);

CREATE TABLE `states` (
  `state_id` int PRIMARY KEY,
  `name` varchar(255) NOT NULL
);

CREATE TABLE `districts` (
  `district_id` int PRIMARY KEY,
  `name` varchar(255) NOT NULL,
  `state_id` int NOT NULL
);

CREATE TABLE `villages` (
  `village_id` int PRIMARY KEY,
  `name` varchar(255) NOT NULL,
  `district_id` int NOT NULL
);

-- Foreign Key Constraints with ON DELETE rules

ALTER TABLE `citizens` 
  ADD FOREIGN KEY (`village_id`) REFERENCES `villages` (`village_id`) ON DELETE CASCADE;

ALTER TABLE `officers` 
  ADD FOREIGN KEY (`district_id`) REFERENCES `districts` (`district_id`) ON DELETE SET NULL;

ALTER TABLE `enrollments` 
  ADD FOREIGN KEY (`citizen_id`) REFERENCES `citizens` (`citizen_id`) ON DELETE CASCADE,
  ADD FOREIGN KEY (`scheme_id`) REFERENCES `schemes` (`scheme_id`) ON DELETE CASCADE,
  ADD FOREIGN KEY (`verified_by`) REFERENCES `officers` (`officer_id`) ON DELETE SET NULL;

ALTER TABLE `disbursements` 
  ADD FOREIGN KEY (`citizen_id`) REFERENCES `citizens` (`citizen_id`) ON DELETE SET NULL,
  ADD FOREIGN KEY (`scheme_id`) REFERENCES `schemes` (`scheme_id`) ON DELETE SET NULL,
  ADD FOREIGN KEY (`approved_by`) REFERENCES `officers` (`officer_id`) ON DELETE SET NULL;

ALTER TABLE `health_details` 
  ADD FOREIGN KEY (`citizen_id`) REFERENCES `citizens` (`citizen_id`) ON DELETE CASCADE;

ALTER TABLE `bank_accounts` 
  ADD FOREIGN KEY (`citizen_id`) REFERENCES `citizens` (`citizen_id`) ON DELETE CASCADE;

ALTER TABLE `scheme_eligibility` 
  ADD FOREIGN KEY (`scheme_id`) REFERENCES `schemes` (`scheme_id`) ON DELETE CASCADE;

ALTER TABLE `eligibility_log` 
  ADD FOREIGN KEY (`citizen_id`) REFERENCES `citizens` (`citizen_id`) ON DELETE SET NULL,
  ADD FOREIGN KEY (`scheme_id`) REFERENCES `schemes` (`scheme_id`) ON DELETE SET NULL;

ALTER TABLE `access_log` 
  ADD FOREIGN KEY (`officer_id`) REFERENCES `officers` (`officer_id`) ON DELETE CASCADE;

ALTER TABLE `districts` 
  ADD FOREIGN KEY (`state_id`) REFERENCES `states` (`state_id`) ON DELETE CASCADE;

ALTER TABLE `villages` 
  ADD FOREIGN KEY (`district_id`) REFERENCES `districts` (`district_id`) ON DELETE CASCADE;

/* ----------------------------------------
   Indexing for Performance Optimization
-------------------------------------------*/

-- Citizens Table
CREATE INDEX idx_citizens_aadhaar ON citizens(aadhaar_no);
-- Aadhaar is a unique identifier and will be frequently searched in eligibility and profile checks

CREATE INDEX idx_citizens_village ON citizens(village_id);
-- Helps filter beneficiaries region-wise, especially when generating district/village reports

-- Officers Table
CREATE INDEX idx_officers_district ON officers(district_id);
-- Speeds up queries assigning or verifying disbursements within a district

-- Schemes Table
CREATE INDEX idx_schemes_sector ON schemes(sector);
-- Used in analytics and visual dashboards for sector-wise reporting

CREATE INDEX idx_schemes_benefit_type ON schemes(benefit_type);
-- Helps AI assistant generate queries by benefit type: Cash, Asset, Service

-- Enrollments Table
CREATE INDEX idx_enrollments_status ON enrollments(scheme_id, status);
-- For queries like: "List all pending verifications in PMAY"

-- Disbursements Table
CREATE INDEX idx_disbursements_scheme ON disbursements(scheme_id);
CREATE INDEX idx_disbursements_date ON disbursements(disbursed_on);
CREATE INDEX idx_disbursements_status ON disbursements(status);
-- These indexes optimize queries that track scheme-wise disbursal or time-bound summaries

-- Access Log Table
CREATE INDEX idx_accesslog_timestamp ON access_log(timestamp);
-- Useful for auditing officer access by time window

-- Eligibility Log Table
CREATE INDEX idx_eliglog_result ON eligibility_log(eligibility_result);
-- Useful to track % of citizens found eligible or ineligible in summary queries

-- Bank Account Table
CREATE INDEX idx_bankaccount_ifsc ON bank_accounts(ifsc_code);
-- For backend UPI/NEFT transaction validation if needed

/* -------------------------------------------------
   Schema Features Explained
---------------------------------------------------*/

-- citizens
/*
  Strong entity representing beneficiaries.
  'village_id' links to geographical hierarchy.
  Aadhaar is enforced as unique for real-world identity tracking.
*/

-- officers
/*
  Represents district/block officers.
  Participates in verifying enrollments and approving disbursements.
  District-based filtering is needed for access control and RBAC.
*/

-- schemes
/*
  Master list of all government schemes.
  Includes metadata useful for AI/NLP classification (sector, benefit_type).
*/

-- enrollments
/*
  Weak entity – citizen can enroll in multiple schemes.
  Surrogate key (enrollment_id) used instead of composite key for implementation simplicity.
  Verifier officer is tracked for audit.
*/

-- disbursements
/*
  Transactional table tracking fund release.
  Approved_by links to officers for transparency.
  payment_mode adds real-world transfer mechanism (cash, DBT, UPI).
*/

-- health_details
/*
  Represents specialization/generalization from citizens.
  Only relevant for Ayushman Bharat / NSAP schemes.
*/

-- bank_accounts
/*
  Optional 1:N relationship.
  Necessary for DBT/UPI-based payment validation.
*/

-- scheme_eligibility
/*
  Table stores rules that define whether a citizen is eligible for a scheme.
  Used in AI-based pre-screening and automated verification logic.
*/

-- eligibility_log
/*
  Tracks system-level decision-making outcomes.
  Useful for debugging why a citizen was flagged as ineligible.
*/

-- access_log
/*
  Required for secure system audit trails.
  Stores query activity, timestamp, and officer involved.
*/

-- state, district, village
/*
  Implements full geographical hierarchy.
  Links citizens, officers, and report aggregations.
*/
