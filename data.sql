-- =====================================================
-- WELFARE DATABASE - SAMPLE DATA
-- Comprehensive realistic data for Indian welfare schemes
-- =====================================================

-- =====================================================
-- MASTER DATA: STATES
-- =====================================================
INSERT INTO states (state_id, name) VALUES
(1, 'Uttar Pradesh'),
(2, 'Maharashtra'),
(3, 'Bihar'),
(4, 'West Bengal'),
(5, 'Madhya Pradesh'),
(6, 'Tamil Nadu'),
(7, 'Rajasthan'),
(8, 'Karnataka'),
(9, 'Gujarat'),
(10, 'Andhra Pradesh'),
(11, 'Odisha'),
(12, 'Telangana'),
(13, 'Kerala'),
(14, 'Jharkhand'),
(15, 'Assam');

-- =====================================================
-- MASTER DATA: DISTRICTS
-- =====================================================
INSERT INTO districts (district_id, name, state_id) VALUES
-- Uttar Pradesh Districts
(1, 'Agra', 1),
(2, 'Lucknow', 1),
(3, 'Kanpur', 1),
(4, 'Varanasi', 1),
(5, 'Allahabad', 1),
-- Maharashtra Districts
(6, 'Mumbai', 2),
(7, 'Pune', 2),
(8, 'Nagpur', 2),
(9, 'Nashik', 2),
(10, 'Aurangabad', 2),
-- Bihar Districts
(11, 'Patna', 3),
(12, 'Gaya', 3),
(13, 'Muzaffarpur', 3),
(14, 'Bhagalpur', 3),
(15, 'Darbhanga', 3),
-- West Bengal Districts
(16, 'Kolkata', 4),
(17, 'Darjeeling', 4),
(18, 'Malda', 4),
(19, 'Murshidabad', 4),
(20, 'North 24 Parganas', 4),
-- Madhya Pradesh Districts
(21, 'Bhopal', 5),
(22, 'Indore', 5),
(23, 'Jabalpur', 5),
(24, 'Gwalior', 5),
(25, 'Ujjain', 5),
-- Tamil Nadu Districts
(26, 'Chennai', 6),
(27, 'Coimbatore', 6),
(28, 'Madurai', 6),
(29, 'Salem', 6),
(30, 'Tiruchirappalli', 6),
-- Additional Districts for other states
(31, 'Jaipur', 7),
(32, 'Jodhpur', 7),
(33, 'Bangalore', 8),
(34, 'Mysore', 8),
(35, 'Ahmedabad', 9),
(36, 'Surat', 9),
(37, 'Visakhapatnam', 10),
(38, 'Vijayawada', 10),
(39, 'Bhubaneswar', 11),
(40, 'Cuttack', 11),
(41, 'Hyderabad', 12),
(42, 'Warangal', 12),
(43, 'Thiruvananthapuram', 13),
(44, 'Kochi', 13),
(45, 'Ranchi', 14),
(46, 'Jamshedpur', 14),
(47, 'Guwahati', 15),
(48, 'Silchar', 15);

-- =====================================================
-- MASTER DATA: VILLAGES
-- =====================================================
INSERT INTO villages (village_id, name, district_id) VALUES
-- Agra District Villages
(1, 'Dayalbagh', 1),
(2, 'Kheragarh', 1),
(3, 'Pinahat', 1),
(4, 'Rundhi', 1),
(5, 'Shahganj', 1),
-- Lucknow District Villages
(6, 'Chinhat', 2),
(7, 'Malihabad', 2),
(8, 'Mohanlalganj', 2),
(9, 'Bakshi Ka Talab', 2),
(10, 'Sarojininagar', 2),
-- Kanpur District Villages
(11, 'Bilhaur', 3),
(12, 'Chaubepur', 3),
(13, 'Ghatampur', 3),
(14, 'Kalyanpur', 3),
(15, 'Shivrajpur', 3),
-- Mumbai District Villages
(16, 'Borivali', 6),
(17, 'Dahisar', 6),
(18, 'Kandivali', 6),
(19, 'Malad', 6),
(20, 'Andheri', 6),
-- Pune District Villages
(21, 'Khadki', 7),
(22, 'Chinchwad', 7),
(23, 'Pimpri', 7),
(24, 'Talegaon', 7),
(25, 'Lonavala', 7),
-- Patna District Villages
(26, 'Danapur', 11),
(27, 'Phulwari', 11),
(28, 'Masaurhi', 11),
(29, 'Maner', 11),
(30, 'Bikram', 11),
-- Kolkata District Villages
(31, 'Dum Dum', 16),
(32, 'Barrackpore', 16),
(33, 'Howrah', 16),
(34, 'Salt Lake', 16),
(35, 'New Town', 16),
-- Rural villages across different states
(36, 'Rampur Khas', 12), -- Gaya
(37, 'Tekari', 12),
(38, 'Belaganj', 12),
(39, 'Sherghati', 12),
(40, 'Manpur', 12),
(41, 'Motihari Rural', 13), -- Muzaffarpur
(42, 'Sitamarhi', 13),
(43, 'Sheohar', 13),
(44, 'Vaishali', 13),
(45, 'Hajipur', 13),
-- Tamil Nadu Villages
(46, 'Tambaram', 26), -- Chennai
(47, 'Sriperumbudur', 26),
(48, 'Tiruvallur', 26),
(49, 'Chengalpattu', 26),
(50, 'Kanchipuram', 26),
-- Karnataka Villages
(51, 'Yelahanka', 33), -- Bangalore
(52, 'Devanahalli', 33),
(53, 'Hoskote', 33),
(54, 'Doddaballapur', 33),
(55, 'Nelamangala', 33),
-- Rajasthan Villages
(56, 'Chomu', 31), -- Jaipur
(57, 'Sanganer', 31),
(58, 'Bagru', 31),
(59, 'Dudu', 31),
(60, 'Amber', 31),
-- Remote/Tribal Villages (for edge cases)
(61, 'Dhurva Tribal Village', 22), -- Indore, MP
(62, 'Bhil Community Village', 22),
(63, 'Adivasi Hamlet', 23), -- Jabalpur, MP
(64, 'Santhal Village', 18), -- Malda, WB
(65, 'Tea Garden Village', 17), -- Darjeeling, WB
(66, 'Fishing Village', 43), -- Thiruvananthapuram, Kerala
(67, 'Hill Station Village', 34), -- Mysore, Karnataka
(68, 'Desert Village', 32), -- Jodhpur, Rajasthan
(69, 'Coastal Village', 37), -- Visakhapatnam, AP
(70, 'Mining Area Village', 45); -- Ranchi, Jharkhand

-- =====================================================
-- GOVERNMENT WELFARE SCHEMES
-- =====================================================
INSERT INTO schemes (scheme_id, name, description, sector, frequency, benefit_type) VALUES
(1, 'MGNREGA', 'Mahatma Gandhi National Rural Employment Guarantee Act - Provides guaranteed 100 days of wage employment in rural areas', 'Employment', 'Continuous', 'Cash'),
(2, 'PMAY', 'Pradhan Mantri Awas Yojana - Affordable housing for all', 'Housing', 'One-time', 'Asset'),
(3, 'Ujjwala Yojana', 'Pradhan Mantri Ujjwala Yojana - Free LPG connections to women from BPL families', 'Energy', 'One-time + Subsidy', 'Asset + Cash'),
(4, 'Ayushman Bharat - PMJAY', 'Pradhan Mantri Jan Arogya Yojana - Health insurance coverage up to Rs. 5 lakh per family per year', 'Healthcare', 'Annual', 'Service'),
(5, 'NSAP', 'National Social Assistance Programme - Pensions for elderly, widows, and disabled', 'Social Security', 'Monthly', 'Cash');

-- =====================================================
-- SCHEME ELIGIBILITY CRITERIA
-- =====================================================
INSERT INTO scheme_eligibility (scheme_id, min_age, max_age, gender, category_required, min_income, disability_required) VALUES
(1, 18, 65, NULL, 'BPL', NULL, NULL), -- MGNREGA
(2, NULL, NULL, NULL, 'BPL/EWS/LIG', 600000, NULL), -- PMAY
(3, 18, NULL, 'Female', 'BPL', NULL, NULL), -- Ujjwala Yojana
(4, NULL, NULL, NULL, 'APL/BPL', 1000000, NULL), -- Ayushman Bharat
(5, NULL, NULL, NULL, 'BPL', NULL, NULL); -- NSAP (covers elderly 60+, widows 40+, disabled 18+)

-- =====================================================
-- GOVERNMENT OFFICERS
-- =====================================================
INSERT INTO officers (officer_id, name, designation, access_level, email, district_id) VALUES
(1, 'Rajesh Kumar Singh', 'District Collector', 'ADMIN', 'rajesh.singh@gov.in', 1),
(2, 'Priya Sharma', 'Block Development Officer', 'MANAGER', 'priya.sharma@gov.in', 1),
(3, 'Amit Verma', 'MGNREGA Officer', 'OPERATOR', 'amit.verma@gov.in', 1),
(4, 'Sunita Devi', 'PMAY Coordinator', 'OPERATOR', 'sunita.devi@gov.in', 1),
(5, 'Dr. Rakesh Gupta', 'District Health Officer', 'MANAGER', 'rakesh.gupta@gov.in', 2),
(6, 'Meera Joshi', 'Social Welfare Officer', 'OPERATOR', 'meera.joshi@gov.in', 2),
(7, 'Vikram Singh', 'District Collector', 'ADMIN', 'vikram.singh@gov.in', 6),
(8, 'Kavita Patil', 'Assistant Collector', 'MANAGER', 'kavita.patil@gov.in', 6),
(9, 'Ravi Kumar', 'PMAY Urban Officer', 'OPERATOR', 'ravi.kumar@gov.in', 6),
(10, 'Asha Reddy', 'District Collector', 'ADMIN', 'asha.reddy@gov.in', 11),
(11, 'Suresh Yadav', 'MGNREGA Coordinator', 'OPERATOR', 'suresh.yadav@gov.in', 11),
(12, 'Deepika Singh', 'Pension Officer', 'OPERATOR', 'deepika.singh@gov.in', 11),
(13, 'Ramesh Babu', 'District Collector', 'ADMIN', 'ramesh.babu@gov.in', 26),
(14, 'Lakshmi Narayanan', 'Health Insurance Officer', 'OPERATOR', 'lakshmi.n@gov.in', 26),
(15, 'Mohammed Ali', 'Agriculture Officer', 'OPERATOR', 'mohammed.ali@gov.in', 26),
(16, 'Sanjay Gupta', 'District Collector', 'ADMIN', 'sanjay.gupta@gov.in', 31),
(17, 'Anita Kumari', 'Women Welfare Officer', 'OPERATOR', 'anita.kumari@gov.in', 31),
(18, 'Dr. Suresh Reddy', 'Medical Officer', 'MANAGER', 'suresh.reddy@gov.in', 33),
(19, 'Geeta Patel', 'Ujjwala Coordinator', 'OPERATOR', 'geeta.patel@gov.in', 35),
(20, 'Arun Kumar', 'District Collector', 'ADMIN', 'arun.kumar@gov.in', 16);

-- =====================================================
-- CITIZENS DATA - DIVERSE AND REALISTIC
-- =====================================================
INSERT INTO citizens (citizen_id, aadhaar_no, name, gender, age, mobile_no, email, village_id) VALUES
-- Young adults in urban areas
(1, '123456789012', 'Rahul Kumar', 'Male', 25, '9876543210', 'rahul.kumar@gmail.com', 16),
(2, '234567890123', 'Priya Singh', 'Female', 23, '8765432109', 'priya.singh@gmail.com', 21),
(3, '345678901234', 'Amit Sharma', 'Male', 28, '7654321098', 'amit.sharma@outlook.com', 26),
(4, '456789012345', 'Sunita Devi', 'Female', 32, '6543210987', NULL, 31),
(5, '567890123456', 'Ravi Patel', 'Male', 29, '5432109876', 'ravi.patel@yahoo.com', 35),

-- Middle-aged rural population
(6, '678901234567', 'Kamala Devi', 'Female', 45, '4321098765', NULL, 36),
(7, '789012345678', 'Ram Singh', 'Male', 42, '3210987654', NULL, 37),
(8, '890123456789', 'Gita Kumari', 'Female', 38, '2109876543', NULL, 41),
(9, '901234567890', 'Shyam Lal', 'Male', 47, '1098765432', NULL, 42),
(10, '012345678901', 'Radha Rani', 'Female', 35, '9087654321', NULL, 46),

-- Elderly citizens eligible for pensions
(11, '123450987654', 'Hari Prasad', 'Male', 67, '8976543210', NULL, 1),
(12, '234561098765', 'Savitri Devi', 'Female', 72, '7865432109', NULL, 6),
(13, '345672109876', 'Gopal Singh', 'Male', 64, '6754321098', NULL, 11),
(14, '456783210987', 'Lakshmi Bai', 'Female', 69, '5643210987', NULL, 46),
(15, '567894321098', 'Ram Chandra', 'Male', 75, '4532109876', NULL, 56),

-- Widows eligible for widow pension
(16, '678905432109', 'Sushila Devi', 'Female', 52, '3421098765', NULL, 16),
(17, '789016543210', 'Meera Bai', 'Female', 48, '2310987654', NULL, 26),
(18, '890127654321', 'Kanta Devi', 'Female', 44, '1209876543', NULL, 36),
(19, '901238765432', 'Urmila Singh', 'Female', 56, '9198765432', NULL, 46),
(20, '012349876543', 'Pushpa Devi', 'Female', 59, '8187654321', NULL, 56),

-- Young mothers 
(21, '123456780987', 'Anjali Sharma', 'Female', 26, '7176543210', 'anjali.sharma@gmail.com', 21),
(22, '234567891098', 'Neha Gupta', 'Female', 24, '6165432109', 'neha.gupta@gmail.com', 31),
(23, '345678902109', 'Pooja Verma', 'Female', 28, '5154321098', NULL, 41),
(24, '456789013210', 'Rekha Singh', 'Female', 30, '4143210987', NULL, 51),
(25, '567890124321', 'Sangita Devi', 'Female', 22, '3132109876', NULL, 61),

-- People with disabilities
(26, '678901235432', 'Suresh Kumar', 'Male', 34, '2121098765', NULL, 16),
(27, '789012346543', 'Maya Devi', 'Female', 29, '1110987654', NULL, 26),
(28, '890123457654', 'Dinesh Singh', 'Male', 41, '9009876543', NULL, 36),
(29, '901234568765', 'Usha Rani', 'Female', 37, '8998765432', NULL, 46),
(30, '012345679876', 'Ashok Kumar', 'Male', 45, '7887654321', NULL, 56),

-- Farmers across different states
(31, '123456789876', 'Kishan Lal', 'Male', 52, '6776543210', NULL, 2),
(32, '234567890987', 'Bhanu Pratap', 'Male', 48, '5665432109', NULL, 7),
(33, '345678901098', 'Jagdish Singh', 'Male', 44, '4554321098', NULL, 12),
(34, '456789012109', 'Mukesh Yadav', 'Male', 39, '3443210987', NULL, 22),
(35, '567890123210', 'Sunil Kumar', 'Male', 55, '2332109876', NULL, 47),

-- Urban poor families
(36, '678901234321', 'Raj Kumar', 'Male', 33, '1221098765', NULL, 16),
(37, '789012345432', 'Sulochana Devi', 'Female', 29, '9110987654', NULL, 21),
(38, '890123456543', 'Vinod Singh', 'Male', 36, '8009876543', NULL, 26),
(39, '901234567654', 'Kamla Devi', 'Female', 31, '7998765432', NULL, 31),
(40, '012345678765', 'Ramesh Chand', 'Male', 27, '6887654321', NULL, 46),

-- Tribal population (edge cases)
(41, '123456787654', 'Birsa Munda', 'Male', 35, '5776543210', NULL, 61),
(42, '234567898765', 'Sita Devi', 'Female', 32, '4665432109', NULL, 62),
(43, '345678909876', 'Arjun Singh', 'Male', 28, '3554321098', NULL, 63),
(44, '456789020987', 'Durga Devi', 'Female', 42, '2443210987', NULL, 64),
(45, '567890131098', 'Kailash Oraon', 'Male', 38, '1332109876', NULL, 65),

-- Women from different backgrounds
(46, '678901242109', 'Savita Kumari', 'Female', 27, '9221098765', NULL, 6),
(47, '789012353210', 'Renu Singh', 'Female', 31, '8110987654', NULL, 11),
(48, '890123464321', 'Kavita Sharma', 'Female', 26, '7009876543', NULL, 16),
(49, '901234575432', 'Nirmala Devi', 'Female', 34, '6998765432', NULL, 21),
(50, '012345686543', 'Asha Rani', 'Female', 29, '5887654321', NULL, 26),

-- Children 
(51, '123456797654', 'Rohit Kumar', 'Male', 8, '4776543210', NULL, 1),
(52, '234567808765', 'Anjali Singh', 'Female', 10, '3665432109', NULL, 6),
(53, '345678919876', 'Vikash Yadav', 'Male', 12, '2554321098', NULL, 11),
(54, '456789030987', 'Priyanka Devi', 'Female', 9, '1443210987', NULL, 16),
(55, '567890141098', 'Aryan Sharma', 'Male', 11, '9332109876', NULL, 21),

-- Senior citizens with chronic conditions
(56, '678901252109', 'Bhagwan Das', 'Male', 78, '8221098765', NULL, 36),
(57, '789012363210', 'Durgabai', 'Female', 82, '7110987654', NULL, 41),
(58, '890123474321', 'Ramprasad', 'Male', 76, '6009876543', NULL, 46),
(59, '901234585432', 'Gauri Devi', 'Female', 71, '5998765432', NULL, 51),
(60, '012345696543', 'Harishchandra', 'Male', 84, '4887654321', NULL, 56),

-- Working age adults in different sectors
(61, '123456807654', 'Manoj Kumar', 'Male', 32, '3776543210', 'manoj.kumar@gmail.com', 16),
(62, '234567918765', 'Seema Verma', 'Female', 28, '2665432109', 'seema.verma@gmail.com', 21),
(63, '345678029876', 'Sudhir Singh', 'Male', 35, '1554321098', NULL, 26),
(64, '456789140987', 'Preeti Sharma', 'Female', 30, '9443210987', 'preeti.sharma@outlook.com', 31),
(65, '567890251098', 'Anand Kumar', 'Male', 37, '8332109876', NULL, 36),

-- Additional diverse cases
(66, '678901362109', 'Shakuntala Devi', 'Female', 43, '7221098765', NULL, 41),
(67, '789012473210', 'Jagdish Prasad', 'Male', 49, '6110987654', NULL, 46),
(68, '890123584321', 'Shanti Devi', 'Female', 54, '5009876543', NULL, 51),
(69, '901234695432', 'Vijay Singh', 'Male', 26, '4998765432', 'vijay.singh@gmail.com', 56),
(70, '012345706543', 'Sunanda Kumari', 'Female', 33, '3887654321', NULL, 61),

-- Young professionals in cities
(71, '123456817654', 'Arun Agarwal', 'Male', 24, '2776543210', 'arun.agarwal@techcorp.com', 6),
(72, '234567928765', 'Deepika Reddy', 'Female', 26, '1665432109', 'deepika.reddy@infosys.com', 16),
(73, '345678039876', 'Rohit Mehra', 'Male', 29, '9554321098', 'rohit.mehra@gmail.com', 21),
(74, '456789150987', 'Sneha Joshi', 'Female', 25, '8443210987', 'sneha.joshi@wipro.com', 26),
(75, '567890261098', 'Karthik Nair', 'Male', 27, '7332109876', 'karthik.nair@tcs.com', 46),

-- Pregnant women for maternity schemes
(76, '678901372109', 'Ritu Singh', 'Female', 25, '6221098765', NULL, 1),
(77, '789012483210', 'Manisha Devi', 'Female', 27, '5110987654', NULL, 11),
(78, '890123594321', 'Sapna Kumari', 'Female', 23, '4009876543', NULL, 21),
(79, '901234605432', 'Vandana Sharma', 'Female', 29, '3998765432', NULL, 31),
(80, '012345716543', 'Kaveri Devi', 'Female', 26, '2887654321', NULL, 41),

-- Border area residents
(81, '123456827654', 'Jaswant Singh', 'Male', 45, '1776543210', NULL, 56), -- Rajasthan border
(82, '234567938765', 'Kiran Devi', 'Female', 39, '9665432109', NULL, 65), -- WB border
(83, '345678049876', 'Suresh Babu', 'Male', 52, '8554321098', NULL, 69), -- AP coastal
(84, '456789160987', 'Ganga Devi', 'Female', 47, '7443210987', NULL, 66), -- Kerala coastal
(85, '567890271098', 'Ramesh Oraon', 'Male', 41, '6332109876', NULL, 70), -- Jharkhand mining

-- Additional elderly for pension schemes
(86, '678901382109', 'Krishna Murthy', 'Male', 73, '5221098765', NULL, 47),
(87, '789012493210', 'Parvati Devi', 'Female', 68, '4110987654', NULL, 48),
(88, '890123504321', 'Gopal Rao', 'Male', 81, '3009876543', NULL, 49),
(89, '901234615432', 'Janaki Bai', 'Female', 77, '2998765432', NULL, 50),
(90, '012345726543', 'Sitaram', 'Male', 79, '1887654321', NULL, 51),

-- Farmers with different crop patterns
(91, '123456837654', 'Balram Singh', 'Male', 44, '9776543210', NULL, 3),
(92, '234567948765', 'Devaki Devi', 'Female', 38, '8665432109', NULL, 8),
(93, '345678059876', 'Chandrasekhar', 'Male', 51, '7554321098', NULL, 13),
(94, '456789170987', 'Radhika Kumari', 'Female', 36, '6443210987', NULL, 23),
(95, '567890281098', 'Krishnan Nair', 'Male', 49, '5332109876', NULL, 48),

-- Youth for skill development
(96, '678901392109', 'Sachin Kumar', 'Male', 22, '4221098765', 'sachin.kumar@gmail.com', 6),
(97, '789012403210', 'Monika Singh', 'Female', 21, '3110987654', 'monika.singh@gmail.com', 16),
(98, '890123514321', 'Vishal Yadav', 'Male', 24, '2009876543', 'vishal.yadav@gmail.com', 26),
(99, '901234625432', 'Swati Sharma', 'Female', 23, '1998765432', 'swati.sharma@gmail.com', 36),
(100, '012345736543', 'Akash Patel', 'Male', 25, '9887654321', 'akash.patel@gmail.com', 46),

-- Additional 200 citizens for comprehensive dataset
(101, '123456847654', 'Ravi Kumar', 'Male', 32, '8776543210', 'ravi.kumar@gmail.com', 7),
(102, '234567958765', 'Sunita Devi', 'Female', 28, '7665432109', NULL, 17),
(103, '345678069876', 'Amit Sharma', 'Male', 35, '6554321098', 'amit.sharma@gmail.com', 27),
(104, '456789180987', 'Priya Singh', 'Female', 30, '5443210987', 'priya.singh@gmail.com', 37),
(105, '567890291098', 'Rajesh Yadav', 'Male', 40, '4332109876', NULL, 47),
(106, '678901302109', 'Meera Gupta', 'Female', 33, '3221098765', 'meera.gupta@gmail.com', 57),
(107, '789012413210', 'Sunil Tiwari', 'Male', 42, '2110987654', NULL, 67),
(108, '890123524321', 'Kavita Mishra', 'Female', 37, '1009876543', 'kavita.mishra@gmail.com', 2),
(109, '901234635432', 'Deepak Verma', 'Male', 29, '9998765432', 'deepak.verma@gmail.com', 12),
(110, '012345746543', 'Anita Jain', 'Female', 26, '8887654321', 'anita.jain@gmail.com', 22),

-- More diverse citizens from different regions
(111, '123456857654', 'Mahesh Patel', 'Male', 48, '7776543210', NULL, 32),
(112, '234567968765', 'Lata Devi', 'Female', 45, '6665432109', NULL, 42),
(113, '345678079876', 'Vikram Singh', 'Male', 31, '5554321098', 'vikram.singh@gmail.com', 52),
(114, '456789190987', 'Rekha Kumari', 'Female', 34, '4443210987', NULL, 62),
(115, '567890201098', 'Anil Kumar', 'Male', 39, '3332109876', 'anil.kumar@gmail.com', 62),
(116, '678901312109', 'Sushila Devi', 'Female', 41, '2221098765', NULL, 1),
(117, '789012423210', 'Ramesh Chand', 'Male', 46, '1110987654', NULL, 11),
(118, '890123534321', 'Geeta Sharma', 'Female', 38, '9009876543', 'geeta.sharma@gmail.com', 21),
(119, '901234645432', 'Suresh Kumar', 'Male', 43, '8998765432', NULL, 31),
(120, '012345756543', 'Urmila Devi', 'Female', 36, '7887654321', NULL, 41),

-- Tribal and rural communities
(121, '123456867654', 'Ramu Tribal', 'Male', 27, '6776543210', NULL, 51),
(122, '234567978765', 'Sita Tribal', 'Female', 24, '5665432109', NULL, 61),
(123, '345678089876', 'Golu Adivasi', 'Male', 33, '4554321098', NULL, 61),
(124, '456789100987', 'Kamla Tribal', 'Female', 29, '3443210987', NULL, 3),
(125, '567890211098', 'Birsa Munda', 'Male', 35, '2332109876', NULL, 13),
(126, '678901322109', 'Soni Devi', 'Female', 31, '1221098765', NULL, 23),
(127, '789012433210', 'Jagdish Oraon', 'Male', 38, '9110987654', NULL, 33),
(128, '890123544321', 'Phulo Devi', 'Female', 32, '8009876543', NULL, 43),
(129, '901234655432', 'Kartik Singh', 'Male', 26, '7998765432', NULL, 53),
(130, '012345766543', 'Basanti Devi', 'Female', 28, '6887654321', NULL, 63),

-- Senior citizens for pension schemes
(131, '123456877654', 'Ram Lal', 'Male', 72, '5776543210', NULL, 63),
(132, '234567988765', 'Kamla Devi', 'Female', 69, '4665432109', NULL, 4),
(133, '345678099876', 'Shyam Lal', 'Male', 76, '3554321098', NULL, 14),
(134, '456789110987', 'Sita Devi', 'Female', 71, '2443210987', NULL, 24),
(135, '567890221098', 'Hari Ram', 'Male', 78, '1332109876', NULL, 34),
(136, '678901332109', 'Ganga Devi', 'Female', 74, '9221098765', NULL, 44),
(137, '789012443210', 'Gopal Das', 'Male', 80, '8110987654', NULL, 54),
(138, '890123554321', 'Radha Devi', 'Female', 73, '7009876543', NULL, 64),
(139, '901234665432', 'Krishna Murari', 'Male', 75, '6998765432', NULL, 64),
(140, '012345776543', 'Tulsi Devi', 'Female', 77, '5887654321', NULL, 5),

-- Middle-aged working population
(141, '123456887654', 'Prakash Verma', 'Male', 44, '4776543210', 'prakash.verma@gmail.com', 15),
(142, '234567998765', 'Sudha Mishra', 'Female', 41, '3665432109', 'sudha.mishra@gmail.com', 25),
(143, '345678009876', 'Manoj Gupta', 'Male', 47, '2554321098', NULL, 35),
(144, '456789120987', 'Nirmala Devi', 'Female', 43, '1443210987', NULL, 45),
(145, '567890231098', 'Dinesh Yadav', 'Male', 49, '9332109876', 'dinesh.yadav@gmail.com', 55),
(146, '678901342109', 'Shanti Devi', 'Female', 46, '8221098765', NULL, 65),
(147, '789012453210', 'Vinod Kumar', 'Male', 50, '7110987654', 'vinod.kumar@gmail.com', 65),
(148, '890123564321', 'Kiran Devi', 'Female', 45, '6009876543', NULL, 6),
(149, '901234675432', 'Rajendra Singh', 'Male', 48, '5998765432', NULL, 16),
(150, '012345786543', 'Pushpa Devi', 'Female', 42, '4887654321', NULL, 26),

-- Young adults and students
(151, '123456897654', 'Rohit Kumar', 'Male', 20, '3776543210', 'rohit.kumar@gmail.com', 36),
(152, '234568008765', 'Neha Singh', 'Female', 19, '2665432109', 'neha.singh@gmail.com', 46),
(153, '345679019876', 'Arjun Patel', 'Male', 22, '1554321098', 'arjun.patel@gmail.com', 56),
(154, '456780130987', 'Pooja Sharma', 'Female', 21, '9443210987', 'pooja.sharma@gmail.com', 66),
(155, '567891241098', 'Kiran Kumar', 'Male', 23, '8332109876', 'kiran.kumar@gmail.com', 66),
(156, '678902352109', 'Ritu Gupta', 'Female', 20, '7221098765', 'ritu.gupta@gmail.com', 7),
(157, '789013463210', 'Vikash Singh', 'Male', 24, '6110987654', 'vikash.singh@gmail.com', 17),
(158, '890124574321', 'Anjali Devi', 'Female', 18, '5009876543', 'anjali.devi@gmail.com', 27),
(159, '901235685432', 'Rahul Yadav', 'Male', 25, '4998765432', 'rahul.yadav@gmail.com', 37),
(160, '012346796543', 'Seema Kumari', 'Female', 22, '3887654321', 'seema.kumari@gmail.com', 47),

-- Farmers and agricultural workers
(161, '123457807654', 'Balwant Singh', 'Male', 54, '2776543210', NULL, 57),
(162, '234568918765', 'Kamla Devi', 'Female', 51, '1665432109', NULL, 67),
(163, '345679029876', 'Jagdish Prasad', 'Male', 56, '9554321098', NULL, 67),
(164, '456780140987', 'Sushma Devi', 'Female', 52, '8443210987', NULL, 8),
(165, '567891251098', 'Harpal Singh', 'Male', 58, '7332109876', NULL, 18),
(166, '678902362109', 'Santosh Devi', 'Female', 49, '6221098765', NULL, 28),
(167, '789013473210', 'Dharam Singh', 'Male', 60, '5110987654', NULL, 38),
(168, '890124584321', 'Kalawati Devi', 'Female', 53, '4009876543', NULL, 48),
(169, '901235695432', 'Bhim Singh', 'Male', 55, '3998765432', NULL, 58),
(170, '012346806543', 'Shakuntala Devi', 'Female', 50, '2887654321', NULL, 68),

-- Daily wage workers
(171, '123457817654', 'Ramu Das', 'Male', 36, '1776543210', NULL, 68),
(172, '234568928765', 'Sarita Devi', 'Female', 33, '9665432109', NULL, 9),
(173, '345679039876', 'Mangal Singh', 'Male', 38, '8554321098', NULL, 19),
(174, '456780150987', 'Sudha Devi', 'Female', 35, '7443210987', NULL, 29),
(175, '567891261098', 'Govind Das', 'Male', 40, '6332109876', NULL, 39),
(176, '678902372109', 'Kamla Kumari', 'Female', 37, '5221098765', NULL, 49),
(177, '789013483210', 'Ramesh Kumar', 'Male', 34, '4110987654', NULL, 59),
(178, '890124594321', 'Nirmala Kumari', 'Female', 31, '3009876543', NULL, 69),
(179, '901235605432', 'Shyam Das', 'Male', 39, '2998765432', NULL, 69),
(180, '012346816543', 'Renu Devi', 'Female', 32, '1887654321', NULL, 10),

-- Artisans and craftspeople
(181, '123457827654', 'Mohan Lal', 'Male', 45, '9776543210', NULL, 20),
(182, '234568938765', 'Shila Devi', 'Female', 42, '8665432109', NULL, 30),
(183, '345679049876', 'Kishan Das', 'Male', 47, '7554321098', NULL, 40),
(184, '456780160987', 'Savitri Devi', 'Female', 44, '6443210987', NULL, 50),
(185, '567891271098', 'Omprakash', 'Male', 49, '5332109876', NULL, 60),
(186, '678902382109', 'Kumari Devi', 'Female', 46, '4221098765', NULL, 70),
(187, '789013493210', 'Banwari Lal', 'Male', 51, '3110987654', NULL, 70),
(188, '890124504321', 'Pramila Devi', 'Female', 48, '2009876543', NULL, 1),
(189, '901235615432', 'Chandra Kumar', 'Male', 43, '1998765432', NULL, 11),
(190, '012346826543', 'Kaushalya Devi', 'Female', 40, '9887654321', NULL, 21),

-- Disabled individuals for NSAP
(191, '123457837654', 'Ravi Disabled', 'Male', 35, '8776543210', NULL, 31),
(192, '234568948765', 'Sunita Disabled', 'Female', 32, '7665432109', NULL, 41),
(193, '345679059876', 'Amit Disabled', 'Male', 28, '6554321098', NULL, 51),
(194, '456780170987', 'Priya Disabled', 'Female', 30, '5443210987', NULL, 61),
(195, '567891281098', 'Rajesh Disabled', 'Male', 33, '4332109876', NULL, 61),

-- Widows for pension schemes
(196, '678902392109', 'Kamla Widow', 'Female', 45, '3221098765', NULL, 2),
(197, '789013403210', 'Sita Widow', 'Female', 48, '2110987654', NULL, 12),
(198, '890124514321', 'Radha Widow', 'Female', 42, '1009876543', NULL, 22),
(199, '901235625432', 'Ganga Widow', 'Female', 50, '9998765432', NULL, 32),
(200, '012346836543', 'Tulsi Widow', 'Female', 47, '8887654321', NULL, 42),

-- Additional diverse population
(201, '123457847654', 'Kailash Nath', 'Male', 52, '7776543210', NULL, 52),
(202, '234568958765', 'Manju Devi', 'Female', 39, '6665432109', 'manju.devi@gmail.com', 62),
(203, '345679069876', 'Satish Kumar', 'Male', 41, '5554321098', 'satish.kumar@gmail.com', 62),
(204, '456780180987', 'Anita Kumari', 'Female', 37, '4443210987', NULL, 3),
(205, '567891291098', 'Mukesh Singh', 'Male', 44, '3332109876', NULL, 13),
(206, '678902302109', 'Usha Devi', 'Female', 46, '2221098765', NULL, 23),
(207, '789013413210', 'Naresh Kumar', 'Male', 48, '1110987654', 'naresh.kumar@gmail.com', 33),
(208, '890124524321', 'Kiran Kumari', 'Female', 35, '9009876543', 'kiran.kumari@gmail.com', 43),
(209, '901235635432', 'Ashok Verma', 'Male', 50, '8998765432', NULL, 53),
(210, '012346846543', 'Sunita Verma', 'Female', 38, '7887654321', NULL, 63),

-- More citizens with varied profiles
(211, '123457857654', 'Mahendra Singh', 'Male', 53, '6776543210', NULL, 63),
(212, '234568968765', 'Savita Devi', 'Female', 40, '5665432109', NULL, 4),
(213, '345679079876', 'Dilip Kumar', 'Male', 42, '4554321098', 'dilip.kumar@gmail.com', 14),
(214, '456780190987', 'Rita Sharma', 'Female', 36, '3443210987', 'rita.sharma@gmail.com', 24),
(215, '567891201098', 'Pankaj Gupta', 'Male', 45, '2332109876', 'pankaj.gupta@gmail.com', 34),
(216, '678902312109', 'Neetu Singh', 'Female', 43, '1221098765', 'neetu.singh@gmail.com', 44),
(217, '789013423210', 'Arun Kumar', 'Male', 47, '9110987654', NULL, 54),
(218, '890124534321', 'Mamta Devi', 'Female', 41, '8009876543', NULL, 64),
(219, '901235645432', 'Sudhir Yadav', 'Male', 49, '7998765432', NULL, 64),
(220, '012346856543', 'Preeti Kumari', 'Female', 34, '6887654321', 'preeti.kumari@gmail.com', 5),

-- More diverse age groups and locations
(221, '123457867654', 'Gopal Krishna', 'Male', 56, '5776543210', NULL, 15),
(222, '234568978765', 'Leela Devi', 'Female', 58, '4665432109', NULL, 25),
(223, '345679089876', 'Ramesh Babu', 'Male', 61, '3554321098', NULL, 35),
(224, '456780200987', 'Shanti Kumari', 'Female', 55, '2443210987', NULL, 45),
(225, '567891211098', 'Bharat Singh', 'Male', 59, '1332109876', NULL, 55),
(226, '678902322109', 'Kalpana Devi', 'Female', 52, '9221098765', NULL, 65),
(227, '789013433210', 'Vijay Kumar', 'Male', 57, '8110987654', NULL, 65),
(228, '890124544321', 'Rashni Devi', 'Female', 54, '7009876543', NULL, 6),
(229, '901235655432', 'Hemant Rai', 'Male', 60, '6998765432', NULL, 16),
(230, '012346866543', 'Sadhna Kumari', 'Female', 53, '5887654321', NULL, 26),

-- Young professionals and educated citizens
(231, '123457877654', 'Nitin Sharma', 'Male', 27, '4776543210', 'nitin.sharma@gmail.com', 36),
(232, '234568988765', 'Pooja Verma', 'Female', 25, '3665432109', 'pooja.verma@gmail.com', 46),
(233, '345679099876', 'Sandeep Kumar', 'Male', 29, '2554321098', 'sandeep.kumar@gmail.com', 56),
(234, '456780210987', 'Kavya Singh', 'Female', 26, '1443210987', 'kavya.singh@gmail.com', 66),
(235, '567891221098', 'Rohit Gupta', 'Male', 28, '9332109876', 'rohit.gupta@gmail.com', 66),
(236, '678902332109', 'Swati Mishra', 'Female', 24, '8221098765', 'swati.mishra@gmail.com', 7),
(237, '789013443210', 'Akshay Patel', 'Male', 30, '7110987654', 'akshay.patel@gmail.com', 17),
(238, '890124554321', 'Priyanka Jain', 'Female', 27, '6009876543', 'priyanka.jain@gmail.com', 27),
(239, '901235665432', 'Deepak Agarwal', 'Male', 31, '5998765432', 'deepak.agarwal@gmail.com', 37),
(240, '012346876543', 'Ritu Saxena', 'Female', 25, '4887654321', 'ritu.saxena@gmail.com', 47),

-- Rural women beneficiaries
(241, '123457887654', 'Saraswati Devi', 'Female', 34, '3776543210', NULL, 57),
(242, '234568998765', 'Durga Devi', 'Female', 31, '2665432109', NULL, 67),
(243, '345670009876', 'Lakshmi Devi', 'Female', 38, '1554321098', NULL, 67),
(244, '456781220987', 'Parvati Devi', 'Female', 35, '9443210987', NULL, 8),
(245, '567892331098', 'Kali Devi', 'Female', 32, '8332109876', NULL, 18),
(246, '678903442109', 'Sharda Devi', 'Female', 39, '7221098765', NULL, 28),
(247, '789014553210', 'Asha Devi', 'Female', 36, '6110987654', NULL, 38),
(248, '890125664321', 'Sita Kumari', 'Female', 33, '5009876543', NULL, 48),
(249, '901236775432', 'Radha Kumari', 'Female', 37, '4998765432', NULL, 58),
(250, '012347886543', 'Gita Devi', 'Female', 30, '3887654321', NULL, 68),

-- Migrant workers
(251, '123458897654', 'Chandan Kumar', 'Male', 28, '2776543210', '9123456780', 68),
(252, '234569008765', 'Mukesh Yadav', 'Male', 31, '1665432109', '8123456789', 9),
(253, '345670119876', 'Santosh Singh', 'Male', 33, '9554321098', '7123456789', 19),
(254, '456781230987', 'Naresh Das', 'Male', 29, '8443210987', '6123456789', 29),
(255, '567892341098', 'Dinesh Kumar', 'Male', 35, '7332109876', '5123456789', 39),
(256, '678903452109', 'Suresh Yadav', 'Male', 32, '6221098765', '4123456789', 49),
(257, '789014563210', 'Rajesh Das', 'Male', 30, '5110987654', '3123456789', 59),
(258, '890125674321', 'Vikash Kumar', 'Male', 34, '4009876543', '2123456789', 69),
(259, '901236785432', 'Ravi Das', 'Male', 27, '3998765432', '1123456789', 69),
(260, '012347896543', 'Anil Yadav', 'Male', 36, '2887654321', '9023456789', 10),

-- Healthcare workers and professionals
(261, '123458907654', 'Dr. Ashok Kumar', 'Male', 45, '1776543210', 'dr.ashok@hospital.com', 20),
(262, '234569018765', 'Nurse Sunita', 'Female', 32, '9665432109', 'sunita.nurse@health.gov.in', 30),
(263, '345670129876', 'Paramedic Raj', 'Male', 28, '8554321098', 'raj.paramedic@gmail.com', 40),
(264, '456781240987', 'ASHA Rekha', 'Female', 35, '7443210987', NULL, 50),
(265, '567892351098', 'ANM Kamla', 'Female', 42, '6332109876', NULL, 60),

-- Teachers and education workers
(266, '678903462109', 'Teacher Mohan', 'Male', 38, '5221098765', 'mohan.teacher@education.gov.in', 70),
(267, '789014573210', 'Principal Sita', 'Female', 47, '4110987654', 'sita.principal@school.edu', 70),
(268, '890125684321', 'Lecturer Ramesh', 'Male', 41, '3009876543', 'ramesh.lecturer@college.edu', 1),
(269, '901236795432', 'Helper Ganga', 'Female', 29, '2998765432', NULL, 11),
(270, '012347806543', 'Librarian Gopal', 'Male', 36, '1887654321', 'gopal.library@gmail.com', 21),

-- Small business owners
(271, '123458917654', 'Shop Owner Ram', 'Male', 43, '9776543210', NULL, 31),
(272, '234569028765', 'Tailor Shyama', 'Female', 39, '8665432109', NULL, 41),
(273, '345670139876', 'Mechanic Sunil', 'Male', 37, '7554321098', 'sunil.mechanic@gmail.com', 51),
(274, '456781250987', 'Baker Lila', 'Female', 34, '6443210987', NULL, 61),
(275, '567892361098', 'Barber Raju', 'Male', 41, '5332109876', NULL, 61),

-- More elderly for comprehensive pension data
(276, '678903472109', 'Babu Ram', 'Male', 82, '4221098765', NULL, 2),
(277, '789014583210', 'Dadi Sita', 'Female', 79, '3110987654', NULL, 12),
(278, '890125694321', 'Nana Hari', 'Male', 84, '2009876543', NULL, 22),
(279, '901236705432', 'Nani Ganga', 'Female', 81, '1998765432', NULL, 32),
(280, '012347816543', 'Baba Shyam', 'Male', 86, '9887654321', NULL, 42),

-- Final diverse group
(281, '123458927654', 'Tech Worker Amit', 'Male', 26, '8776543210', 'amit.tech@company.com', 52),
(282, '234569038765', 'Bank Officer Neha', 'Female', 29, '7665432109', 'neha.bank@bank.com', 62),
(283, '345670149876', 'Driver Suresh', 'Male', 38, '6554321098', NULL, 62),
(284, '456781260987', 'Maid Kamla', 'Female', 31, '5443210987', NULL, 3),
(285, '567892371098', 'Watchman Ravi', 'Male', 44, '4332109876', NULL, 13),
(286, '678903482109', 'Cook Sita', 'Female', 36, '3221098765', NULL, 23),
(287, '789014593210', 'Gardener Mohan', 'Male', 39, '2110987654', NULL, 33),
(288, '890125604321', 'Cleaner Radha', 'Female', 33, '1009876543', NULL, 43),
(289, '901236715432', 'Guard Shyam', 'Male', 42, '9998765432', NULL, 53),
(290, '012347826543', 'Vendor Gita', 'Female', 28, '8887654321', NULL, 63),

-- Additional border and special cases
(291, '123458937654', 'Border Farmer Joga', 'Male', 51, '7776543210', NULL, 63),
(292, '234569048765', 'Coastal Fisher Mira', 'Female', 44, '6665432109', NULL, 4),
(293, '345670159876', 'Mountain Guide Tenzin', 'Male', 37, '5554321098', NULL, 14),
(294, '456781270987', 'Desert Nomad Kiran', 'Female', 29, '4443210987', NULL, 24),
(295, '567892381098', 'Forest Worker Bhola', 'Male', 46, '3332109876', NULL, 34),
(296, '678903492109', 'River Boatman Golu', 'Male', 40, '2221098765', NULL, 44),
(297, '789014503210', 'Hill Station Guide Maya', 'Female', 32, '1110987654', NULL, 54),
(298, '890125614321', 'Village Head Balram', 'Male', 55, '9009876543', NULL, 64),
(299, '901236725432', 'Midwife Savitri', 'Female', 48, '8998765432', NULL, 64),
(300, '012347836543', 'Priest Shiva Das', 'Male', 62, '7887654321', NULL, 5);

-- =====================================================
-- HEALTH DETAILS - For citizens with health conditions
-- =====================================================
INSERT INTO health_details (citizen_id, chronic_conditions, disability_status) VALUES
-- Citizens with chronic conditions for Ayushman Bharat
(15, 'Diabetes, Hypertension', 'None'),
(27, 'Heart Disease', 'None'),
(38, 'Chronic Kidney Disease', 'None'),
(49, 'Cancer survivor', 'None'),
(62, 'Arthritis, Diabetes', 'None'),
(73, 'Respiratory problems', 'None'),
(84, 'Stroke survivor', 'Partial paralysis'),
(95, 'Mental health issues', 'None'),
(106, 'Epilepsy', 'None'),
(117, 'Tuberculosis treatment', 'None'),
(128, 'Liver disease', 'None'),
(139, 'Alzheimer disease', 'None'),
(150, 'Chronic pain', 'None'),
(161, 'Vision problems', 'Partial blindness'),
(172, 'Hearing problems', 'Partial deafness'),

-- Citizens with disabilities for NSAP
(191, 'None', 'Physical disability - 60%'),
(192, 'None', 'Visual impairment - 80%'),
(193, 'None', 'Hearing impairment - 70%'),
(194, 'None', 'Mental disability - 50%'),
(195, 'None', 'Multiple disabilities - 90%'),
(35, 'None', 'Locomotor disability - 40%'),
(67, 'None', 'Speech and hearing - 65%'),
(89, 'None', 'Intellectual disability - 75%'),
(142, 'None', 'Visual impairment - 100%'),
(183, 'None', 'Physical disability - 85%'),

-- Additional health conditions
(23, 'Asthma', 'None'),
(45, 'Migraine, Anxiety', 'None'),
(56, 'Thyroid disorder', 'None'),
(78, 'Blood pressure', 'None'),
(91, 'Back pain, Arthritis', 'None'),
(134, 'Memory loss', 'None'),
(156, 'Anemia', 'None'),
(167, 'Joint problems', 'None'),
(189, 'Skin condition', 'None'),
(201, 'Eye problems', 'None'),
(234, 'Allergies', 'None'),
(256, 'Stomach ulcer', 'None'),
(278, 'Age-related conditions', 'Mobility issues'),
(289, 'Work-related injury', 'Temporary disability'),
(299, 'Pregnancy complications history', 'None');

-- =====================================================
-- BANK ACCOUNTS - For DBT and payment processing
-- =====================================================
INSERT INTO bank_accounts (account_id, citizen_id, account_no, bank_name, ifsc_code) VALUES
-- Primary accounts for major beneficiaries
(1, 1, '12345678901234', 'State Bank of India', 'SBIN0001234'),
(2, 2, '23456789012345', 'Punjab National Bank', 'PUNB0002345'),
(3, 3, '34567890123456', 'Bank of Baroda', 'BARB0003456'),
(4, 4, '45678901234567', 'Union Bank of India', 'UBIN0004567'),
(5, 5, '56789012345678', 'Central Bank of India', 'CBIN0005678'),
(6, 6, '67890123456789', 'Indian Bank', 'IDIB0006789'),
(7, 7, '78901234567890', 'Bank of India', 'BKID0007890'),
(8, 8, '89012345678901', 'Canara Bank', 'CNRB0008901'),
(9, 9, '90123456789012', 'Indian Overseas Bank', 'IOBA0009012'),
(10, 10, '01234567890123', 'UCO Bank', 'UCBA0001023'),

-- Regional bank accounts
(11, 15, '11234567890123', 'Gramin Bank of Aryavart', 'GBAG0011234'),
(12, 25, '22345678901234', 'Maharashtra Gramin Bank', 'MAHG0022345'),
(13, 35, '33456789012345', 'Bihar Gramin Bank', 'BIHG0033456'),
(14, 45, '44567890123456', 'West Bengal Gramin Bank', 'WBGB0044567'),
(15, 55, '55678901234567', 'MP Gramin Bank', 'MPGB0055678'),

-- Urban bank accounts
(16, 101, '61234567890123', 'HDFC Bank', 'HDFC0001234'),
(17, 102, '72345678901234', 'ICICI Bank', 'ICIC0002345'),
(18, 103, '83456789012345', 'Axis Bank', 'UTIB0003456'),
(19, 104, '94567890123456', 'Kotak Mahindra Bank', 'KKBK0004567'),
(20, 105, '05678901234567', 'Yes Bank', 'YESB0005678'),

-- Jan Dhan accounts for poor beneficiaries
(21, 111, '16789012345678', 'State Bank of India', 'SBIN0016789'),
(22, 121, '27890123456789', 'Punjab National Bank', 'PUNB0027890'),
(23, 131, '38901234567890', 'Bank of Baroda', 'BARB0038901'),
(24, 141, '49012345678901', 'Union Bank of India', 'UBIN0049012'),
(25, 151, '50123456789012', 'Central Bank of India', 'CBIN0050123'),

-- Additional diverse accounts
(26, 161, '61234567890124', 'Allahabad Bank', 'ALLA0061234'),
(27, 171, '72345678901235', 'Syndicate Bank', 'SYNB0072345'),
(28, 181, '83456789012346', 'Corporation Bank', 'CORP0083456'),
(29, 191, '94567890123457', 'Vijaya Bank', 'VJYA0094567'),
(30, 201, '05678901234568', 'Dena Bank', 'BKDN0005678'),

-- More accounts for active beneficiaries
(31, 11, '16789012345679', 'State Bank of India', 'SBIN0116789'),
(32, 21, '27890123456780', 'Punjab National Bank', 'PUNB0127890'),
(33, 31, '38901234567891', 'Bank of Baroda', 'BARB0138901'),
(34, 41, '49012345678902', 'Union Bank of India', 'UBIN0149012'),
(35, 51, '50123456789013', 'Central Bank of India', 'CBIN0150123'),
(36, 61, '61234567890125', 'Indian Bank', 'IDIB0161234'),
(37, 71, '72345678901236', 'Bank of India', 'BKID0172345'),
(38, 81, '83456789012347', 'Canara Bank', 'CNRB0183456'),
(39, 91, '94567890123458', 'Indian Overseas Bank', 'IOBA0194567'),
(40, 96, '05678901234569', 'UCO Bank', 'UCBA0105678'),

-- Accounts for urban professionals
(41, 231, '16789012345680', 'HDFC Bank', 'HDFC0216789'),
(42, 232, '27890123456781', 'ICICI Bank', 'ICIC0227890'),
(43, 233, '38901234567892', 'Axis Bank', 'UTIB0238901'),
(44, 234, '49012345678903', 'Kotak Mahindra Bank', 'KKBK0249012'),
(45, 235, '50123456789014', 'Yes Bank', 'YESB0250123'),

-- Accounts for migrant workers
(46, 251, '61234567890126', 'State Bank of India', 'SBIN0261234'),
(47, 252, '72345678901237', 'Punjab National Bank', 'PUNB0272345'),
(48, 253, '83456789012348', 'Bank of Baroda', 'BARB0283456'),
(49, 254, '94567890123459', 'Union Bank of India', 'UBIN0294567'),
(50, 255, '05678901234570', 'Central Bank of India', 'CBIN0205678'),

-- Additional accounts for comprehensive coverage
(51, 12, '16789012345681', 'Gramin Bank of Aryavart', 'GBAG0316789'),
(52, 22, '27890123456782', 'Maharashtra Gramin Bank', 'MAHG0327890'),
(53, 32, '38901234567893', 'Bihar Gramin Bank', 'BIHG0338901'),
(54, 42, '49012345678904', 'West Bengal Gramin Bank', 'WBGB0349012'),
(55, 52, '50123456789015', 'MP Gramin Bank', 'MPGB0350123'),
(56, 62, '61234567890127', 'Tamil Nadu Gramin Bank', 'TNGB0361234'),
(57, 72, '72345678901238', 'Rajasthan Gramin Bank', 'RJGB0372345'),
(58, 82, '83456789012349', 'Karnataka Gramin Bank', 'KRGB0383456'),
(59, 92, '94567890123460', 'Gujarat Gramin Bank', 'GJGB0394567'),
(60, 106, '05678901234571', 'AP Gramin Bank', 'APGB0305678'),

-- More diverse banking relationships
(61, 116, '16789012345682', 'Odisha Gramin Bank', 'ODGB0416789'),
(62, 126, '27890123456783', 'Telangana Gramin Bank', 'TSGB0427890'),
(63, 136, '38901234567894', 'Kerala Gramin Bank', 'KRGB0438901'),
(64, 146, '49012345678905', 'Jharkhand Gramin Bank', 'JHGB0449012'),
(65, 156, '50123456789016', 'Assam Gramin Bank', 'ASGB0450123'),
(66, 166, '61234567890128', 'Himachal Gramin Bank', 'HPGB0461234'),
(67, 176, '72345678901239', 'Uttarakhand Gramin Bank', 'UKGB0472345'),
(68, 186, '83456789012350', 'Haryana Gramin Bank', 'HRGB0483456'),
(69, 196, '94567890123461', 'Punjab Gramin Bank', 'PJGB0494567'),
(70, 206, '05678901234572', 'Chhattisgarh Gramin Bank', 'CGGB0505678'),

-- Final set of accounts
(71, 216, '16789012345683', 'Manipur Gramin Bank', 'MNGB0516789'),
(72, 226, '27890123456784', 'Mizoram Gramin Bank', 'MZGB0527890'),
(73, 236, '38901234567895', 'Nagaland Gramin Bank', 'NLGB0538901'),
(74, 246, '49012345678906', 'Tripura Gramin Bank', 'TRGB0549012'),
(75, 256, '50123456789017', 'Meghalaya Gramin Bank', 'MGHL0550123'),
(76, 266, '61234567890129', 'Arunachal Gramin Bank', 'ARGB0561234'),
(77, 276, '72345678901240', 'Sikkim Gramin Bank', 'SKGB0572345'),
(78, 286, '83456789012351', 'Goa Gramin Bank', 'GOGB0583456'),
(79, 296, '94567890123462', 'State Bank of India', 'SBIN0594567'),
(80, 300, '05678901234573', 'Punjab National Bank', 'PUNB0605678');

-- =====================================================
-- ENROLLMENTS - Citizens enrolled in welfare schemes
-- =====================================================
INSERT INTO enrollments (enrollment_id, citizen_id, scheme_id, enrollment_date, status, last_verified_on, verified_by) VALUES
-- MGNREGA enrollments (Rural employment guarantee) - scheme_id = 1
(1, 1, 1, '2023-01-15', 'Active', '2024-07-15', 1),
(2, 11, 1, '2023-02-10', 'Active', '2024-06-20', 2),
(3, 21, 1, '2023-03-05', 'Active', '2024-05-25', 3),
(4, 31, 1, '2023-01-20', 'Suspended', '2024-04-30', 1),
(5, 41, 1, '2023-04-12', 'Active', '2024-07-10', 4),
(6, 51, 1, '2023-02-28', 'Active', '2024-06-15', 5),
(7, 61, 1, '2023-05-18', 'Active', '2024-07-20', 6),
(8, 71, 1, '2023-03-22', 'Active', '2024-05-30', 7),
(9, 81, 1, '2023-06-10', 'Pending', '2024-07-25', 8),
(10, 91, 1, '2023-04-05', 'Active', '2024-06-10', 9),
(11, 101, 1, '2023-07-15', 'Active', '2024-07-30', 10),
(12, 111, 1, '2023-05-28', 'Active', '2024-06-25', 11),
(13, 121, 1, '2023-08-10', 'Pending', NULL, NULL),
(14, 131, 1, '2023-06-20', 'Active', '2024-07-05', 12),
(15, 141, 1, '2023-09-05', 'Active', '2024-07-12', 13),
(16, 151, 1, '2023-07-18', 'Active', '2024-06-28', 14),
(17, 161, 1, '2023-10-12', 'Active', '2024-07-18', 15),
(18, 171, 1, '2023-08-25', 'Active', '2024-06-30', 1),
(19, 181, 1, '2023-11-08', 'Pending', NULL, NULL),
(20, 191, 1, '2023-09-15', 'Active', '2024-07-22', 2),

-- PMAY enrollments (Affordable housing) - scheme_id = 2  
(21, 5, 2, '2023-01-10', 'Approved', '2024-03-15', 3),
(22, 15, 2, '2023-02-20', 'Under Review', '2024-07-10', 4),
(23, 25, 2, '2023-03-15', 'Approved', '2024-04-20', 5),
(24, 35, 2, '2023-04-08', 'Rejected', '2024-05-12', 6),
(25, 45, 2, '2023-05-22', 'Approved', '2024-06-25', 7),
(26, 55, 2, '2023-06-12', 'Under Review', '2024-07-15', 8),
(27, 65, 2, '2023-07-05', 'Approved', '2024-07-30', 9),
(28, 75, 2, '2023-08-18', 'Under Review', NULL, NULL),
(29, 85, 2, '2023-09-10', 'Approved', '2024-07-20', 10),
(30, 95, 2, '2023-10-25', 'Under Review', NULL, NULL),
(31, 105, 2, '2023-11-15', 'Pending', NULL, NULL),
(32, 115, 2, '2023-12-08', 'Under Review', '2024-07-25', 11),
(33, 125, 2, '2024-01-20', 'Approved', '2024-06-30', 12),
(34, 135, 2, '2024-02-10', 'Under Review', '2024-07-12', 13),
(35, 145, 2, '2024-03-05', 'Pending', NULL, NULL),
(36, 155, 2, '2024-04-18', 'Under Review', '2024-07-08', 14),
(37, 165, 2, '2024-05-12', 'Approved', '2024-07-18', 15),
(38, 175, 2, '2024-06-08', 'Under Review', NULL, NULL),
(39, 185, 2, '2024-07-15', 'Pending', NULL, NULL),
(40, 195, 2, '2024-07-28', 'Pending', NULL, NULL),

-- Ujjwala Yojana enrollments (LPG subsidies for women) - scheme_id = 3
(41, 2, 3, '2023-01-08', 'Active', '2024-07-20', 1),
(42, 12, 3, '2023-01-25', 'Active', '2024-06-15', 2),
(43, 22, 3, '2023-02-15', 'Active', '2024-07-10', 3),
(44, 32, 3, '2023-03-08', 'Active', '2024-05-25', 4),
(45, 42, 3, '2023-03-28', 'Active', '2024-06-30', 5),
(46, 52, 3, '2023-04-15', 'Active', '2024-07-12', 6),
(47, 62, 3, '2023-05-05', 'Active', '2024-06-20', 7),
(48, 72, 3, '2023-05-22', 'Active', '2024-07-25', 8),
(49, 82, 3, '2023-06-18', 'Active', '2024-06-25', 9),
(50, 92, 3, '2023-07-08', 'Active', '2024-07-15', 10),
(51, 102, 3, '2023-07-25', 'Active', '2024-07-30', 11),
(52, 112, 3, '2023-08-15', 'Active', '2024-06-18', 12),
(53, 122, 3, '2023-09-05', 'Active', '2024-07-08', 13),
(54, 132, 3, '2023-09-22', 'Active', '2024-06-22', 14),
(55, 142, 3, '2023-10-12', 'Active', '2024-07-28', 15),
(56, 152, 3, '2023-11-08', 'Active', '2024-06-28', 1),
(57, 162, 3, '2023-11-25', 'Active', '2024-07-18', 2),
(58, 172, 3, '2023-12-15', 'Active', '2024-06-12', 3),
(59, 182, 3, '2024-01-08', 'Active', '2024-07-22', 4),
(60, 192, 3, '2024-01-25', 'Active', '2024-06-15', 5),
(61, 196, 3, '2024-02-12', 'Active', '2024-07-25', 6),
(62, 197, 3, '2024-02-28', 'Active', '2024-06-30', 7),
(63, 198, 3, '2024-03-15', 'Active', '2024-07-12', 8),
(64, 199, 3, '2024-03-30', 'Active', '2024-06-25', 9),
(65, 200, 3, '2024-04-18', 'Active', '2024-07-20', 10),

-- Ayushman Bharat enrollments (Health insurance) - scheme_id = 4
(66, 15, 4, '2023-02-10', 'Active', '2024-07-15', 11),
(67, 27, 4, '2023-03-15', 'Active', '2024-06-20', 12),
(68, 38, 4, '2023-04-20', 'Active', '2024-07-25', 13),
(69, 49, 4, '2023-05-12', 'Active', '2024-06-15', 14),
(70, 62, 4, '2023-06-08', 'Active', '2024-07-30', 15),
(71, 73, 4, '2023-07-15', 'Active', '2024-06-28', 1),
(72, 84, 4, '2023-08-20', 'Active', '2024-07-18', 2),
(73, 95, 4, '2023-09-12', 'Active', '2024-06-22', 3),
(74, 106, 4, '2023-10-18', 'Active', '2024-07-12', 4),
(75, 117, 4, '2023-11-25', 'Active', '2024-06-30', 5),
(76, 128, 4, '2023-12-15', 'Active', '2024-07-20', 6),
(77, 139, 4, '2024-01-20', 'Active', '2024-06-25', 7),
(78, 150, 4, '2024-02-15', 'Active', '2024-07-15', 8),
(79, 161, 4, '2024-03-18', 'Active', '2024-06-18', 9),
(80, 172, 4, '2024-04-22', 'Active', '2024-07-28', 10),
(81, 191, 4, '2024-05-15', 'Active', '2024-06-12', 11),
(82, 192, 4, '2024-06-10', 'Active', '2024-07-22', 12),
(83, 193, 4, '2024-06-25', 'Active', '2024-07-05', 13),
(84, 194, 4, '2024-07-08', 'Active', '2024-07-30', 14),
(85, 195, 4, '2024-07-20', 'Pending', NULL, NULL),

-- NSAP enrollments (Pensions) - scheme_id = 5
-- Elderly pensions
(86, 131, 5, '2023-01-05', 'Active', '2024-07-10', 15),
(87, 132, 5, '2023-01-12', 'Active', '2024-06-15', 1),
(88, 133, 5, '2023-01-20', 'Active', '2024-07-20', 2),
(89, 134, 5, '2023-02-08', 'Active', '2024-06-25', 3),
(90, 135, 5, '2023-02-15', 'Active', '2024-07-12', 4),
(91, 136, 5, '2023-02-22', 'Active', '2024-06-30', 5),
(92, 137, 5, '2023-03-05', 'Active', '2024-07-25', 6),
(93, 138, 5, '2023-03-12', 'Active', '2024-06-18', 7),
(94, 139, 5, '2023-03-20', 'Active', '2024-07-15', 8),
(95, 140, 5, '2023-04-02', 'Active', '2024-06-22', 9),
(96, 276, 5, '2023-04-10', 'Active', '2024-07-18', 10),
(97, 277, 5, '2023-04-18', 'Active', '2024-06-28', 11),
(98, 278, 5, '2023-05-05', 'Active', '2024-07-22', 12),
(99, 279, 5, '2023-05-12', 'Active', '2024-06-12', 13),
(100, 280, 5, '2023-05-20', 'Active', '2024-07-30', 14),

-- Widow pensions
(101, 196, 5, '2023-06-08', 'Active', '2024-07-15', 15),
(102, 197, 5, '2023-06-15', 'Active', '2024-06-20', 1),
(103, 198, 5, '2023-06-22', 'Active', '2024-07-25', 2),
(104, 199, 5, '2023-07-05', 'Active', '2024-06-25', 3),
(105, 200, 5, '2023-07-12', 'Active', '2024-07-12', 4),

-- Disability pensions
(106, 191, 5, '2023-08-10', 'Active', '2024-07-20', 5),
(107, 192, 5, '2023-08-18', 'Active', '2024-06-30', 6),
(108, 193, 5, '2023-08-25', 'Active', '2024-07-18', 7),
(109, 194, 5, '2023-09-05', 'Active', '2024-06-15', 8),
(110, 195, 5, '2023-09-12', 'Active', '2024-07-28', 9),

-- Additional enrollments for comprehensive coverage
(111, 16, 1, '2024-01-15', 'Active', '2024-07-30', 10),
(112, 26, 1, '2024-02-10', 'Active', '2024-06-20', 11),
(113, 36, 1, '2024-03-05', 'Active', '2024-07-15', 12),
(114, 46, 1, '2024-04-12', 'Pending', NULL, NULL),
(115, 56, 1, '2024-05-18', 'Active', '2024-07-25', 13),
(116, 66, 1, '2024-06-15', 'Active', '2024-07-20', 14),
(117, 76, 1, '2024-07-10', 'Pending', NULL, NULL),
(118, 86, 1, '2024-07-25', 'Pending', NULL, NULL),
(119, 96, 1, '2024-06-30', 'Active', '2024-07-28', 15),
(120, 106, 1, '2024-05-22', 'Active', '2024-07-12', 1),

-- More PMAY enrollments
(121, 17, 2, '2024-01-20', 'Under Review', '2024-07-15', 2),
(122, 27, 2, '2024-02-15', 'Approved', '2024-06-30', 3),
(123, 37, 2, '2024-03-10', 'Under Review', NULL, NULL),
(124, 47, 2, '2024-04-05', 'Pending', NULL, NULL),
(125, 57, 2, '2024-05-12', 'Under Review', '2024-07-20', 4),
(126, 67, 2, '2024-06-18', 'Approved', '2024-07-25', 5),
(127, 77, 2, '2024-07-08', 'Pending', NULL, NULL),
(128, 87, 2, '2024-07-22', 'Pending', NULL, NULL),
(129, 97, 2, '2024-06-25', 'Under Review', '2024-07-30', 6),
(130, 107, 2, '2024-05-30', 'Approved', '2024-07-18', 7),

-- More Ujjwala enrollments
(131, 206, 3, '2024-05-08', 'Active', '2024-07-15', 8),
(132, 216, 3, '2024-05-22', 'Active', '2024-06-25', 9),
(133, 226, 3, '2024-06-05', 'Active', '2024-07-20', 10),
(134, 236, 3, '2024-06-18', 'Active', '2024-07-28', 11),
(135, 246, 3, '2024-07-02', 'Active', '2024-07-30', 12),
(136, 256, 3, '2024-07-15', 'Pending', NULL, NULL),
(137, 266, 3, '2024-07-28', 'Pending', NULL, NULL),
(138, 276, 3, '2024-06-30', 'Active', '2024-07-25', 13),
(139, 286, 3, '2024-05-15', 'Active', '2024-07-12', 14),
(140, 296, 3, '2024-04-30', 'Active', '2024-06-30', 15),

-- Cross-scheme enrollments for eligible citizens
(141, 3, 3, '2023-02-20', 'Active', '2024-07-18', 1),
(142, 13, 3, '2023-03-15', 'Active', '2024-06-22', 2),
(143, 23, 3, '2023-04-10', 'Active', '2024-07-25', 3),
(144, 7, 4, '2023-08-15', 'Active', '2024-06-15', 4),
(145, 17, 4, '2023-09-20', 'Active', '2024-07-20', 5),
(146, 47, 4, '2023-10-25', 'Active', '2024-06-28', 6),
(147, 57, 4, '2023-11-30', 'Active', '2024-07-15', 7),
(148, 67, 4, '2023-12-20', 'Active', '2024-06-25', 8),
(149, 77, 4, '2024-01-25', 'Active', '2024-07-30', 9),
(150, 87, 4, '2024-02-28', 'Active', '2024-06-20', 10);

-- Additional enrollments to reach 200+ enrollment records
INSERT INTO enrollments (enrollment_id, citizen_id, scheme_id, enrollment_date, status, last_verified_on, verified_by) VALUES
-- More MGNREGA enrollments
(151, 201, 1, '2024-01-12', 'Active', '2024-07-25', 1),
(152, 211, 1, '2024-02-08', 'Active', '2024-07-20', 2),
(153, 221, 1, '2024-03-15', 'Active', '2024-07-18', 3),
(154, 231, 1, '2024-04-20', 'Pending', NULL, NULL),
(155, 241, 1, '2024-05-12', 'Active', '2024-07-30', 4),
(156, 251, 1, '2024-06-08', 'Active', '2024-07-22', 5),
(157, 261, 1, '2024-07-05', 'Pending', NULL, NULL),
(158, 271, 1, '2024-07-18', 'Active', '2024-07-25', 6),
(159, 281, 1, '2024-06-25', 'Active', '2024-07-28', 7),
(160, 291, 1, '2024-05-30', 'Active', '2024-07-15', 8),

-- More PMAY enrollments
(161, 202, 2, '2024-02-15', 'Under Review', '2024-07-12', 9),
(162, 212, 2, '2024-03-20', 'Approved', '2024-07-18', 10),
(163, 222, 2, '2024-04-10', 'Under Review', NULL, NULL),
(164, 232, 2, '2024-05-05', 'Pending', NULL, NULL),
(165, 242, 2, '2024-06-12', 'Under Review', '2024-07-25', 11),
(166, 252, 2, '2024-07-08', 'Pending', NULL, NULL),
(167, 262, 2, '2024-07-20', 'Under Review', NULL, NULL),
(168, 272, 2, '2024-06-28', 'Approved', '2024-07-30', 12),
(169, 282, 2, '2024-05-15', 'Under Review', '2024-07-20', 13),
(170, 292, 2, '2024-04-22', 'Approved', '2024-07-15', 14),

-- More Ujjwala enrollments
(171, 203, 3, '2024-03-08', 'Active', '2024-07-22', 15),
(172, 213, 3, '2024-03-25', 'Active', '2024-07-18', 1),
(173, 223, 3, '2024-04-12', 'Active', '2024-07-25', 2),
(174, 233, 3, '2024-04-28', 'Active', '2024-07-20', 3),
(175, 243, 3, '2024-05-15', 'Active', '2024-07-28', 4),
(176, 253, 3, '2024-06-02', 'Active', '2024-07-30', 5),
(177, 263, 3, '2024-06-18', 'Active', '2024-07-25', 6),
(178, 273, 3, '2024-07-05', 'Active', '2024-07-22', 7),
(179, 283, 3, '2024-07-18', 'Pending', NULL, NULL),
(180, 293, 3, '2024-06-30', 'Active', '2024-07-28', 8),

-- More Ayushman Bharat enrollments
(181, 204, 4, '2024-03-12', 'Active', '2024-07-15', 9),
(182, 214, 4, '2024-04-08', 'Active', '2024-07-20', 10),
(183, 224, 4, '2024-04-25', 'Active', '2024-07-25', 11),
(184, 244, 4, '2024-05-18', 'Active', '2024-07-30', 12),
(185, 254, 4, '2024-06-10', 'Active', '2024-07-18', 13),
(186, 264, 4, '2024-06-25', 'Active', '2024-07-22', 14),
(187, 274, 4, '2024-07-12', 'Active', '2024-07-28', 15),
(188, 284, 4, '2024-07-25', 'Pending', NULL, NULL),
(189, 294, 4, '2024-06-15', 'Active', '2024-07-20', 1),
(190, 295, 4, '2024-05-28', 'Active', '2024-07-25', 2),

-- More NSAP enrollments
(191, 205, 5, '2024-03-15', 'Active', '2024-07-18', 3),
(192, 215, 5, '2024-04-12', 'Active', '2024-07-22', 4),
(193, 225, 5, '2024-04-28', 'Active', '2024-07-25', 5),
(194, 235, 5, '2024-05-20', 'Active', '2024-07-28', 6),
(195, 245, 5, '2024-06-08', 'Active', '2024-07-30', 7),
(196, 255, 5, '2024-06-22', 'Active', '2024-07-20', 8),
(197, 265, 5, '2024-07-10', 'Active', '2024-07-25', 9),
(198, 275, 5, '2024-07-22', 'Pending', NULL, NULL),
(199, 285, 5, '2024-06-18', 'Active', '2024-07-28', 10),
(200, 300, 5, '2024-05-25', 'Active', '2024-07-22', 11);

-- =====================================================
-- DISBURSEMENTS ONLY - Clean INSERT for existing database
-- =====================================================

-- Clear existing disbursement data if needed
-- DELETE FROM disbursements;

-- Insert all disbursement records
INSERT INTO disbursements (disbursement_id, citizen_id, scheme_id, amount, status, disbursed_on, approved_by, payment_mode) VALUES
-- MGNREGA wage payments (100 days guarantee @ 250 per day)
(1, 1, 1, 25000.00, 'Completed', '2024-07-15', 1, 'Bank Transfer'),
(2, 11, 1, 22500.00, 'Completed', '2024-07-10', 2, 'Bank Transfer'),
(3, 21, 1, 20000.00, 'Completed', '2024-07-05', 3, 'Bank Transfer'),
(4, 41, 1, 18750.00, 'Completed', '2024-06-30', 4, 'Bank Transfer'),
(5, 51, 1, 21250.00, 'Completed', '2024-06-25', 5, 'Bank Transfer'),
(6, 61, 1, 23750.00, 'Completed', '2024-06-20', 6, 'Bank Transfer'),
(7, 71, 1, 19500.00, 'Completed', '2024-06-15', 7, 'Bank Transfer'),
(8, 91, 1, 24500.00, 'Completed', '2024-06-10', 9, 'Bank Transfer'),
(9, 101, 1, 16250.00, 'Completed', '2024-06-05', 10, 'Bank Transfer'),
(10, 111, 1, 22000.00, 'Completed', '2024-05-30', 11, 'Bank Transfer'),
(11, 131, 1, 17500.00, 'Completed', '2024-05-25', 12, 'Bank Transfer'),
(12, 141, 1, 25000.00, 'Completed', '2024-05-20', 13, 'Bank Transfer'),
(13, 151, 1, 20750.00, 'Completed', '2024-05-15', 14, 'Bank Transfer'),
(14, 161, 1, 23250.00, 'Completed', '2024-05-10', 15, 'Bank Transfer'),
(15, 171, 1, 21750.00, 'Completed', '2024-05-05', 1, 'Bank Transfer'),

-- PMAY house construction grants
(16, 5, 2, 120000.00, 'Completed', '2024-04-15', 3, 'Bank Transfer'),
(17, 25, 2, 120000.00, 'Completed', '2024-05-20', 5, 'Bank Transfer'),
(18, 45, 2, 120000.00, 'Completed', '2024-06-25', 7, 'Bank Transfer'),
(19, 65, 2, 120000.00, 'Completed', '2024-07-30', 9, 'Bank Transfer'),
(20, 85, 2, 120000.00, 'Pending', '2024-08-15', 10, 'Bank Transfer'),
(21, 125, 2, 120000.00, 'Completed', '2024-06-30', 12, 'Bank Transfer'),
(22, 165, 2, 120000.00, 'Completed', '2024-07-18', 15, 'Bank Transfer'),
(23, 27, 2, 120000.00, 'Completed', '2024-06-30', 3, 'Bank Transfer'),
(24, 107, 2, 120000.00, 'Completed', '2024-07-18', 7, 'Bank Transfer'),
(25, 126, 2, 120000.00, 'Processing', '2024-08-10', 5, 'Bank Transfer'),

-- Ujjwala LPG subsidies (Monthly)
(26, 2, 3, 200.00, 'Completed', '2024-07-01', 1, 'Bank Transfer'),
(27, 12, 3, 200.00, 'Completed', '2024-07-01', 2, 'Bank Transfer'),
(28, 22, 3, 200.00, 'Completed', '2024-07-01', 3, 'Bank Transfer'),
(29, 32, 3, 200.00, 'Completed', '2024-07-01', 4, 'Bank Transfer'),
(30, 42, 3, 200.00, 'Completed', '2024-07-01', 5, 'Bank Transfer'),
(31, 52, 3, 200.00, 'Completed', '2024-07-01', 6, 'Bank Transfer'),
(32, 62, 3, 200.00, 'Completed', '2024-07-01', 7, 'Bank Transfer'),
(33, 72, 3, 200.00, 'Completed', '2024-07-01', 8, 'Bank Transfer'),
(34, 82, 3, 200.00, 'Completed', '2024-07-01', 9, 'Bank Transfer'),
(35, 92, 3, 200.00, 'Completed', '2024-07-01', 10, 'Bank Transfer'),
(36, 102, 3, 200.00, 'Completed', '2024-07-01', 11, 'Bank Transfer'),
(37, 112, 3, 200.00, 'Completed', '2024-07-01', 12, 'Bank Transfer'),
(38, 122, 3, 200.00, 'Completed', '2024-07-01', 13, 'Bank Transfer'),
(39, 132, 3, 200.00, 'Completed', '2024-07-01', 14, 'Bank Transfer'),
(40, 142, 3, 200.00, 'Completed', '2024-07-01', 15, 'Bank Transfer'),

-- Previous month Ujjwala payments
(41, 2, 3, 200.00, 'Completed', '2024-06-01', 1, 'Bank Transfer'),
(42, 12, 3, 200.00, 'Completed', '2024-06-01', 2, 'Bank Transfer'),
(43, 22, 3, 200.00, 'Completed', '2024-06-01', 3, 'Bank Transfer'),
(44, 32, 3, 200.00, 'Completed', '2024-06-01', 4, 'Bank Transfer'),
(45, 42, 3, 200.00, 'Completed', '2024-06-01', 5, 'Bank Transfer'),
(46, 152, 3, 200.00, 'Completed', '2024-06-01', 1, 'Bank Transfer'),
(47, 162, 3, 200.00, 'Completed', '2024-06-01', 2, 'Bank Transfer'),
(48, 172, 3, 200.00, 'Completed', '2024-06-01', 3, 'Bank Transfer'),
(49, 182, 3, 200.00, 'Completed', '2024-06-01', 4, 'Bank Transfer'),
(50, 192, 3, 200.00, 'Completed', '2024-06-01', 5, 'Bank Transfer'),

-- NSAP pension payments (Monthly)
-- Elderly pensions @ 800 per month
(51, 131, 5, 800.00, 'Completed', '2024-07-01', 15, 'Bank Transfer'),
(52, 132, 5, 800.00, 'Completed', '2024-07-01', 1, 'Bank Transfer'),
(53, 133, 5, 800.00, 'Completed', '2024-07-01', 2, 'Bank Transfer'),
(54, 134, 5, 800.00, 'Completed', '2024-07-01', 3, 'Bank Transfer'),
(55, 135, 5, 800.00, 'Completed', '2024-07-01', 4, 'Bank Transfer'),
(56, 136, 5, 800.00, 'Completed', '2024-07-01', 5, 'Bank Transfer'),
(57, 137, 5, 800.00, 'Completed', '2024-07-01', 6, 'Bank Transfer'),
(58, 138, 5, 800.00, 'Completed', '2024-07-01', 7, 'Bank Transfer'),
(59, 139, 5, 800.00, 'Completed', '2024-07-01', 8, 'Bank Transfer'),
(60, 140, 5, 800.00, 'Completed', '2024-07-01', 9, 'Bank Transfer'),

-- Widow pensions @ 500 per month
(61, 196, 5, 500.00, 'Completed', '2024-07-01', 15, 'Bank Transfer'),
(62, 197, 5, 500.00, 'Completed', '2024-07-01', 1, 'Bank Transfer'),
(63, 198, 5, 500.00, 'Completed', '2024-07-01', 2, 'Bank Transfer'),
(64, 199, 5, 500.00, 'Completed', '2024-07-01', 3, 'Bank Transfer'),
(65, 200, 5, 500.00, 'Completed', '2024-07-01', 4, 'Bank Transfer'),

-- Disability pensions @ 300 per month
(66, 191, 5, 300.00, 'Completed', '2024-07-01', 5, 'Bank Transfer'),
(67, 192, 5, 300.00, 'Completed', '2024-07-01', 6, 'Bank Transfer'),
(68, 193, 5, 300.00, 'Completed', '2024-07-01', 7, 'Bank Transfer'),
(69, 194, 5, 300.00, 'Completed', '2024-07-01', 8, 'Bank Transfer'),
(70, 195, 5, 300.00, 'Completed', '2024-07-01', 9, 'Bank Transfer'),

-- Previous month pension payments
(71, 131, 5, 800.00, 'Completed', '2024-06-01', 15, 'Bank Transfer'),
(72, 132, 5, 800.00, 'Completed', '2024-06-01', 1, 'Bank Transfer'),
(73, 133, 5, 800.00, 'Completed', '2024-06-01', 2, 'Bank Transfer'),
(74, 134, 5, 800.00, 'Completed', '2024-06-01', 3, 'Bank Transfer'),
(75, 135, 5, 800.00, 'Completed', '2024-06-01', 4, 'Bank Transfer'),
(76, 196, 5, 500.00, 'Completed', '2024-06-01', 15, 'Bank Transfer'),
(77, 197, 5, 500.00, 'Completed', '2024-06-01', 1, 'Bank Transfer'),
(78, 198, 5, 500.00, 'Completed', '2024-06-01', 2, 'Bank Transfer'),
(79, 191, 5, 300.00, 'Completed', '2024-06-01', 5, 'Bank Transfer'),
(80, 192, 5, 300.00, 'Completed', '2024-06-01', 6, 'Bank Transfer'),

-- Additional MGNREGA payments
(81, 16, 1, 24000.00, 'Completed', '2024-07-30', 10, 'Bank Transfer'),
(82, 26, 1, 21500.00, 'Completed', '2024-07-25', 11, 'Bank Transfer'),
(83, 36, 1, 19750.00, 'Completed', '2024-07-20', 12, 'Bank Transfer'),
(84, 56, 1, 23000.00, 'Completed', '2024-07-15', 13, 'Bank Transfer'),
(85, 66, 1, 22250.00, 'Completed', '2024-07-10', 14, 'Bank Transfer'),
(86, 96, 1, 18500.00, 'Completed', '2024-07-05', 15, 'Bank Transfer'),
(87, 106, 1, 20500.00, 'Completed', '2024-06-30', 1, 'Bank Transfer'),
(88, 116, 1, 25000.00, 'Processing', '2024-08-10', 2, 'Bank Transfer'),
(89, 181, 1, 24750.00, 'Completed', '2024-06-25', 2, 'Bank Transfer'),
(90, 201, 1, 22750.00, 'Completed', '2024-06-20', 3, 'Bank Transfer'),

-- Additional Ujjwala payments for new beneficiaries
(91, 206, 3, 200.00, 'Completed', '2024-07-01', 8, 'Bank Transfer'),
(92, 216, 3, 200.00, 'Completed', '2024-07-01', 9, 'Bank Transfer'),
(93, 226, 3, 200.00, 'Completed', '2024-07-01', 10, 'Bank Transfer'),
(94, 236, 3, 200.00, 'Completed', '2024-07-01', 11, 'Bank Transfer'),
(95, 246, 3, 200.00, 'Completed', '2024-07-01', 12, 'Bank Transfer'),
(96, 286, 3, 200.00, 'Completed', '2024-07-01', 14, 'Bank Transfer'),
(97, 3, 3, 200.00, 'Completed', '2024-07-01', 1, 'Bank Transfer'),
(98, 13, 3, 200.00, 'Completed', '2024-07-01', 2, 'Bank Transfer'),
(99, 23, 3, 200.00, 'Completed', '2024-07-01', 3, 'Bank Transfer'),
(100, 276, 3, 200.00, 'Completed', '2024-07-01', 13, 'Bank Transfer'),

-- Additional pension payments for elderly
(101, 276, 5, 800.00, 'Completed', '2024-07-01', 10, 'Bank Transfer'),
(102, 277, 5, 800.00, 'Completed', '2024-07-01', 11, 'Bank Transfer'),
(103, 278, 5, 800.00, 'Completed', '2024-07-01', 12, 'Bank Transfer'),
(104, 279, 5, 800.00, 'Completed', '2024-07-01', 13, 'Bank Transfer'),
(105, 280, 5, 800.00, 'Completed', '2024-07-01', 14, 'Bank Transfer'),

-- Failed/Pending disbursements for analysis (with proper approved_by values)
(106, 31, 1, 15000.00, 'Failed', '2024-07-01', 1, 'Bank Transfer'),
(107, 81, 1, 18000.00, 'Pending', '2024-08-15', 8, 'Bank Transfer'),
(108, 121, 1, 20000.00, 'Pending', '2024-08-15', 5, 'Bank Transfer'),
(109, 35, 2, 120000.00, 'Failed', '2024-05-12', 6, 'Bank Transfer'),
(110, 75, 2, 120000.00, 'Processing', '2024-08-10', 10, 'Bank Transfer'),
(111, 95, 2, 120000.00, 'Processing', '2024-08-10', 12, 'Bank Transfer'),
(112, 256, 3, 200.00, 'Pending', '2024-08-15', 7, 'Bank Transfer'),
(113, 266, 3, 200.00, 'Pending', '2024-08-15', 8, 'Bank Transfer'),
(114, 195, 5, 300.00, 'Processing', '2024-08-10', 9, 'Bank Transfer'),
(115, 84, 4, 5000.00, 'Completed', '2024-06-15', 2, 'Bank Transfer'),

-- Additional disbursements (116-200)
(116, 201, 1, 22500.00, 'Completed', '2024-07-25', 1, 'Bank Transfer'),
(117, 211, 1, 24000.00, 'Completed', '2024-07-20', 2, 'Bank Transfer'),
(118, 221, 1, 19500.00, 'Completed', '2024-07-18', 3, 'Bank Transfer'),
(119, 241, 1, 21750.00, 'Completed', '2024-07-30', 4, 'Bank Transfer'),
(120, 251, 1, 23250.00, 'Completed', '2024-07-22', 5, 'Bank Transfer'),
(121, 271, 1, 20500.00, 'Completed', '2024-07-25', 6, 'Bank Transfer'),
(122, 281, 1, 22750.00, 'Completed', '2024-07-28', 7, 'Bank Transfer'),
(123, 291, 1, 18750.00, 'Completed', '2024-07-15', 8, 'Bank Transfer'),

-- More PMAY house grants
(124, 212, 2, 120000.00, 'Completed', '2024-07-18', 10, 'Bank Transfer'),
(125, 268, 2, 120000.00, 'Completed', '2024-07-30', 12, 'Bank Transfer'),
(126, 270, 2, 120000.00, 'Completed', '2024-07-15', 14, 'Bank Transfer'),
(127, 292, 2, 120000.00, 'Processing', '2024-08-10', 15, 'Bank Transfer'),

-- More Ujjwala LPG subsidies
(128, 203, 3, 200.00, 'Completed', '2024-07-01', 15, 'Bank Transfer'),
(129, 213, 3, 200.00, 'Completed', '2024-07-01', 1, 'Bank Transfer'),
(130, 223, 3, 200.00, 'Completed', '2024-07-01', 2, 'Bank Transfer'),
(131, 233, 3, 200.00, 'Completed', '2024-07-01', 3, 'Bank Transfer'),
(132, 243, 3, 200.00, 'Completed', '2024-07-01', 4, 'Bank Transfer'),
(133, 253, 3, 200.00, 'Completed', '2024-07-01', 5, 'Bank Transfer'),
(134, 263, 3, 200.00, 'Completed', '2024-07-01', 6, 'Bank Transfer'),
(135, 273, 3, 200.00, 'Completed', '2024-07-01', 7, 'Bank Transfer'),
(136, 293, 3, 200.00, 'Completed', '2024-07-01', 8, 'Bank Transfer'),

-- Previous month Ujjwala payments for new beneficiaries
(137, 203, 3, 200.00, 'Completed', '2024-06-01', 15, 'Bank Transfer'),
(138, 213, 3, 200.00, 'Completed', '2024-06-01', 1, 'Bank Transfer'),
(139, 223, 3, 200.00, 'Completed', '2024-06-01', 2, 'Bank Transfer'),
(140, 233, 3, 200.00, 'Completed', '2024-06-01', 3, 'Bank Transfer'),
(141, 243, 3, 200.00, 'Completed', '2024-06-01', 4, 'Bank Transfer'),

-- More Ayushman Bharat health insurance claims
(142, 204, 4, 15000.00, 'Completed', '2024-07-15', 9, 'Bank Transfer'),
(143, 214, 4, 8500.00, 'Completed', '2024-07-20', 10, 'Bank Transfer'),
(144, 224, 4, 12000.00, 'Completed', '2024-07-25', 11, 'Bank Transfer'),
(145, 244, 4, 6750.00, 'Completed', '2024-07-30', 12, 'Bank Transfer'),
(146, 254, 4, 9200.00, 'Completed', '2024-07-18', 13, 'Bank Transfer'),
(147, 264, 4, 11500.00, 'Completed', '2024-07-22', 14, 'Bank Transfer'),
(148, 274, 4, 7800.00, 'Completed', '2024-07-28', 15, 'Bank Transfer'),
(149, 294, 4, 13400.00, 'Completed', '2024-07-20', 1, 'Bank Transfer'),
(150, 295, 4, 10600.00, 'Completed', '2024-07-25', 2, 'Bank Transfer'),

-- More NSAP pension payments
(151, 205, 5, 800.00, 'Completed', '2024-07-01', 3, 'Bank Transfer'),
(152, 215, 5, 800.00, 'Completed', '2024-07-01', 4, 'Bank Transfer'),
(153, 225, 5, 800.00, 'Completed', '2024-07-01', 5, 'Bank Transfer'),
(154, 235, 5, 500.00, 'Completed', '2024-07-01', 6, 'Bank Transfer'), -- Widow pension
(155, 245, 5, 300.00, 'Completed', '2024-07-01', 7, 'Bank Transfer'), -- Disability pension
(156, 255, 5, 800.00, 'Completed', '2024-07-01', 8, 'Bank Transfer'),
(157, 265, 5, 500.00, 'Completed', '2024-07-01', 9, 'Bank Transfer'), -- Widow pension
(158, 275, 5, 300.00, 'Completed', '2024-07-01', 10, 'Bank Transfer'), -- Disability pension
(159, 285, 5, 800.00, 'Completed', '2024-07-01', 11, 'Bank Transfer'),
(160, 295, 5, 500.00, 'Completed', '2024-07-01', 12, 'Bank Transfer'); -- Widow pension


-- =====================================================
-- ELIGIBILITY LOG - System eligibility checks
-- =====================================================
INSERT INTO eligibility_log (log_id, citizen_id, scheme_id, eligibility_result, reason, checked_on) VALUES
-- MGNREGA eligibility checks
(1, 1, 1, 'Eligible', 'Rural citizen, adult, employed in agriculture', '2023-01-10 09:15:00'),
(2, 11, 1, 'Eligible', 'Rural citizen, meets age criteria', '2023-02-05 10:30:00'),
(3, 21, 1, 'Eligible', 'Rural background, agricultural worker', '2023-03-01 11:45:00'),
(4, 31, 1, 'Ineligible', 'Suspended due to duplicate enrollment', '2023-01-15 14:20:00'),
(5, 41, 1, 'Eligible', 'Rural citizen, meets employment criteria', '2023-04-07 08:30:00'),
(6, 251, 1, 'Eligible', 'Migrant worker, rural background', '2024-01-10 16:45:00'),
(7, 252, 1, 'Eligible', 'Daily wage worker, meets criteria', '2024-02-05 09:20:00'),
(8, 253, 1, 'Eligible', 'Rural employment seeker', '2024-03-01 12:15:00'),
(9, 254, 1, 'Eligible', 'Agricultural laborer', '2024-04-07 15:30:00'),
(10, 255, 1, 'Eligible', 'Rural artisan, meets age criteria', '2024-05-12 10:45:00'),

-- PMAY eligibility checks
(11, 5, 2, 'Eligible', 'Below poverty line, no pucca house', '2023-01-05 09:00:00'),
(12, 15, 2, 'Eligible', 'Rural family, meets income criteria', '2023-02-15 14:30:00'),
(13, 25, 2, 'Eligible', 'No permanent housing, eligible income', '2023-03-10 11:20:00'),
(14, 35, 2, 'Ineligible', 'Already owns property', '2023-04-03 16:45:00'),
(15, 45, 2, 'Eligible', 'Landless family, meets criteria', '2023-05-17 08:15:00'),
(16, 55, 2, 'Eligible', 'Rural BPL family', '2023-06-07 13:40:00'),
(17, 65, 2, 'Eligible', 'Homeless family, verified need', '2023-06-30 10:55:00'),
(18, 75, 2, 'Eligible', 'Kutcha house, meets income limit', '2023-08-13 12:25:00'),
(19, 85, 2, 'Eligible', 'No proper shelter, verified', '2023-09-05 15:10:00'),
(20, 95, 2, 'Eligible', 'Rural poor family', '2023-10-20 09:35:00'),

-- Ujjwala eligibility checks
(21, 2, 3, 'Eligible', 'BPL woman, no LPG connection', '2023-01-03 10:20:00'),
(22, 12, 3, 'Eligible', 'Rural woman, meets criteria', '2023-01-20 14:15:00'),
(23, 22, 3, 'Eligible', 'Woman from SC/ST category', '2023-02-10 11:30:00'),
(24, 32, 3, 'Eligible', 'Female beneficiary, verified need', '2023-03-03 16:45:00'),
(25, 42, 3, 'Eligible', 'Women from poor family', '2023-03-23 08:50:00'),
(26, 52, 3, 'Eligible', 'Rural female, no cooking gas', '2023-04-10 13:25:00'),
(27, 62, 3, 'Eligible', 'BPL female beneficiary', '2023-04-30 12:40:00'),
(28, 72, 3, 'Eligible', 'Woman from eligible category', '2023-05-17 15:20:00'),
(29, 82, 3, 'Eligible', 'Rural woman, verified eligibility', '2023-06-13 09:10:00'),
(30, 92, 3, 'Eligible', 'Female from poor household', '2023-07-03 11:55:00'),

-- Ayushman Bharat eligibility checks
(31, 15, 4, 'Eligible', 'Chronic condition, BPL family', '2023-02-05 10:45:00'),
(32, 27, 4, 'Eligible', 'Heart patient, meets income criteria', '2023-03-10 14:20:00'),
(33, 38, 4, 'Eligible', 'Kidney disease, verified need', '2023-04-15 11:30:00'),
(34, 49, 4, 'Eligible', 'Cancer survivor, eligible family', '2023-05-07 16:15:00'),
(35, 62, 4, 'Eligible', 'Multiple conditions, BPL status', '2023-06-03 09:40:00'),
(36, 73, 4, 'Eligible', 'Respiratory issues, verified', '2023-07-10 13:25:00'),
(37, 84, 4, 'Eligible', 'Stroke survivor, meets criteria', '2023-08-15 12:50:00'),
(38, 95, 4, 'Eligible', 'Mental health condition', '2023-09-07 15:35:00'),
(39, 106, 4, 'Eligible', 'Epilepsy patient, verified need', '2023-10-13 10:20:00'),
(40, 117, 4, 'Eligible', 'TB treatment, eligible income', '2023-11-20 14:40:00'),

-- NSAP eligibility checks
(41, 131, 5, 'Eligible', 'Age 72, meets elderly criteria', '2023-01-01 09:30:00'),
(42, 132, 5, 'Eligible', 'Age 69, elderly woman', '2023-01-07 11:15:00'),
(43, 133, 5, 'Eligible', 'Age 76, senior citizen', '2023-01-15 14:45:00'),
(44, 134, 5, 'Eligible', 'Age 71, elderly female', '2023-02-03 10:25:00'),
(45, 135, 5, 'Eligible', 'Age 78, meets age limit', '2023-02-10 13:20:00'),
(46, 196, 5, 'Eligible', 'Widow, meets criteria', '2023-06-03 12:40:00'),
(47, 197, 5, 'Eligible', 'Widow, verified status', '2023-06-10 15:15:00'),
(48, 198, 5, 'Eligible', 'Widow, income below limit', '2023-06-17 09:55:00'),
(49, 199, 5, 'Eligible', 'Widow, meets all criteria', '2023-06-30 11:30:00'),
(50, 200, 5, 'Eligible', 'Widow, verified eligibility', '2023-07-07 14:20:00'),

-- Disability pension eligibility
(51, 191, 5, 'Eligible', '60% physical disability', '2023-08-05 10:15:00'),
(52, 192, 5, 'Eligible', '80% visual impairment', '2023-08-13 13:45:00'),
(53, 193, 5, 'Eligible', '70% hearing impairment', '2023-08-20 11:30:00'),
(54, 194, 5, 'Eligible', '50% mental disability', '2023-08-30 16:20:00'),
(55, 195, 5, 'Eligible', '90% multiple disabilities', '2023-09-07 09:40:00'),

-- Ineligible cases for analysis
(56, 96, 2, 'Ineligible', 'Age below minimum requirement', '2024-06-25 10:30:00'),
(57, 97, 2, 'Ineligible', 'Age below housing scheme criteria', '2024-06-28 14:15:00'),
(58, 101, 3, 'Ineligible', 'Male citizen, scheme for women only', '2023-07-20 11:45:00'),
(59, 111, 3, 'Ineligible', 'Male applicant, gender criteria not met', '2023-08-10 15:20:00'),
(60, 96, 5, 'Ineligible', 'Age below pension eligibility', '2024-01-15 09:25:00'),

-- Recent eligibility checks
(61, 261, 1, 'Ineligible', 'Urban resident, scheme for rural only', '2024-07-01 10:30:00'),
(62, 262, 1, 'Eligible', 'Rural healthcare worker, meets criteria', '2024-07-02 14:20:00'),
(63, 263, 1, 'Eligible', 'Rural paramedic, eligible', '2024-07-03 11:45:00'),
(64, 271, 2, 'Eligible', 'Small business owner, meets income limit', '2024-07-05 16:30:00'),
(65, 272, 2, 'Eligible', 'Tailor, verified need for housing', '2024-07-06 09:15:00'),
(66, 281, 4, 'Eligible', 'Tech worker with health insurance need', '2024-07-10 13:40:00'),
(67, 282, 4, 'Eligible', 'Bank officer, meets health criteria', '2024-07-11 12:25:00'),
(68, 283, 1, 'Eligible', 'Driver, rural background', '2024-07-12 15:50:00'),
(69, 284, 3, 'Eligible', 'Domestic worker, female beneficiary', '2024-07-13 10:35:00'),
(70, 285, 1, 'Eligible', 'Watchman, meets employment criteria', '2024-07-14 14:40:00'),

-- Cross-scheme eligibility checks
(71, 15, 1, 'Eligible', 'Rural farmer, meets multiple scheme criteria', '2024-07-15 11:20:00'),
(72, 15, 2, 'Eligible', 'Same citizen eligible for housing', '2024-07-15 11:25:00'),
(73, 62, 1, 'Eligible', 'Rural woman, multiple scheme eligibility', '2024-07-16 13:30:00'),
(74, 131, 4, 'Eligible', 'Elderly with health conditions', '2024-07-17 15:45:00'),
(75, 191, 4, 'Eligible', 'Disabled person needs health coverage', '2024-07-18 09:50:00'),

-- System automated checks
(76, 300, 1, 'Ineligible', 'Priest, not in target demographic', '2024-07-20 10:15:00'),
(77, 299, 3, 'Eligible', 'Midwife, rural female healthcare worker', '2024-07-20 11:30:00'),
(78, 298, 2, 'Eligible', 'Village head, meets income criteria', '2024-07-20 14:20:00'),
(79, 297, 1, 'Eligible', 'Hill station guide, rural employment', '2024-07-21 16:45:00'),
(80, 296, 1, 'Eligible', 'River boatman, traditional occupation', '2024-07-21 12:35:00'),

-- Additional automated eligibility checks
(81, 291, 1, 'Eligible', 'Border farmer, rural employment', '2024-07-22 09:20:00'),
(82, 292, 3, 'Eligible', 'Coastal fisher woman, meets criteria', '2024-07-22 13:15:00'),
(83, 293, 1, 'Eligible', 'Mountain guide, rural occupation', '2024-07-22 15:40:00'),
(84, 294, 3, 'Eligible', 'Desert nomad woman, verified need', '2024-07-23 11:25:00'),
(85, 295, 1, 'Eligible', 'Forest worker, rural employment', '2024-07-23 14:50:00'),

-- Final batch of eligibility checks
(86, 286, 3, 'Eligible', 'Cook, female domestic worker', '2024-07-24 10:40:00'),
(87, 288, 3, 'Eligible', 'Cleaner, female worker', '2024-07-24 12:30:00'),
(88, 290, 3, 'Eligible', 'Vendor, female entrepreneur', '2024-07-24 15:20:00'),
(89, 276, 5, 'Eligible', 'Age 82, elderly pension eligible', '2024-07-25 09:35:00'),
(90, 280, 5, 'Eligible', 'Age 86, senior citizen', '2024-07-25 13:45:00'),

-- Recent comprehensive checks
(91, 231, 4, 'Eligible', 'Young professional with health needs', '2024-07-26 11:15:00'),
(92, 241, 3, 'Eligible', 'Rural woman, traditional beneficiary', '2024-07-26 14:30:00'),
(93, 261, 4, 'Eligible', 'Doctor, healthcare professional needs coverage', '2024-07-27 10:45:00'),
(94, 271, 1, 'Ineligible', 'Shop owner, not in rural employment category', '2024-07-27 16:20:00'),
(95, 281, 2, 'Ineligible', 'Tech worker, income above housing scheme limit', '2024-07-28 12:55:00'),

-- Edge cases and special circumstances
(96, 35, 5, 'Ineligible', 'Disability not severe enough for pension', '2024-07-29 09:40:00'),
(97, 67, 5, 'Eligible', 'Speech and hearing disability 65%', '2024-07-29 13:25:00'),
(98, 89, 5, 'Eligible', 'Intellectual disability 75%', '2024-07-29 15:50:00'),
(99, 142, 5, 'Eligible', '100% visual impairment', '2024-07-30 11:30:00'),
(100, 183, 5, 'Eligible', '85% physical disability', '2024-07-30 14:15:00');

-- =====================================================
-- ACCESS LOG - Officer access and query tracking
-- =====================================================
INSERT INTO access_log (log_id, officer_id, entity_accessed, action, timestamp, query_text, target_id) VALUES
-- District Officer access patterns
(1, 1, 'citizens', 'VIEW', '2024-07-30 09:15:00', 'Show all MGNREGA beneficiaries in my district', 1),
(2, 1, 'enrollments', 'VIEW', '2024-07-30 09:20:00', 'List pending MGNREGA verifications', NULL),
(3, 1, 'disbursements', 'APPROVE', '2024-07-30 09:25:00', 'Approve wage payment for citizen ID 1', 1),
(4, 2, 'citizens', 'VIEW', '2024-07-30 10:30:00', 'Search citizen by Aadhaar number', 11),
(5, 2, 'enrollments', 'VERIFY', '2024-07-30 10:35:00', 'Verify MGNREGA enrollment for citizen', 11),
(6, 2, 'disbursements', 'VIEW', '2024-07-30 10:40:00', 'Check payment status for beneficiary', 11),
(7, 3, 'schemes', 'VIEW', '2024-07-30 11:15:00', 'Review PMAY scheme guidelines', 2),
(8, 3, 'enrollments', 'APPROVE', '2024-07-30 11:20:00', 'Approve PMAY application', 21),
(9, 3, 'disbursements', 'APPROVE', '2024-07-30 11:25:00', 'Release housing grant payment', 21),
(10, 4, 'citizens', 'SEARCH', '2024-07-30 12:00:00', 'Find citizens eligible for Ujjwala scheme', NULL),

-- Block Officer activities
(11, 5, 'enrollments', 'VIEW', '2024-07-30 13:45:00', 'List all scheme enrollments in block', NULL),
(12, 5, 'citizens', 'VIEW', '2024-07-30 13:50:00', 'Show BPL families in my jurisdiction', NULL),
(13, 5, 'disbursements', 'APPROVE', '2024-07-30 13:55:00', 'Approve multiple LPG subsidies', 42),
(14, 6, 'health_details', 'VIEW', '2024-07-30 14:30:00', 'Review health conditions for Ayushman Bharat', NULL),
(15, 6, 'enrollments', 'VERIFY', '2024-07-30 14:35:00', 'Verify health insurance enrollment', 66),
(16, 7, 'citizens', 'UPDATE', '2024-07-30 15:10:00', 'Update citizen contact information', 61),
(17, 7, 'bank_accounts', 'VIEW', '2024-07-30 15:15:00', 'Verify bank account for DBT', 61),
(18, 8, 'disbursements', 'VIEW', '2024-07-30 16:20:00', 'Generate monthly disbursement report', NULL),
(19, 8, 'access_log', 'VIEW', '2024-07-30 16:25:00', 'Review officer access patterns', NULL),
(20, 9, 'eligibility_log', 'VIEW', '2024-07-30 16:50:00', 'Check eligibility decisions for audit', NULL),

-- Welfare Officer activities  
(21, 10, 'citizens', 'VIEW', '2024-07-29 09:00:00', 'List all elderly citizens for pension review', NULL),
(22, 10, 'enrollments', 'BULK_VERIFY', '2024-07-29 09:30:00', 'Batch verify pension enrollments', NULL),
(23, 10, 'disbursements', 'APPROVE', '2024-07-29 10:00:00', 'Process monthly pension payments', 51),
(24, 11, 'schemes', 'VIEW', '2024-07-29 11:15:00', 'Review NSAP guidelines for disability', 5),
(25, 11, 'health_details', 'VIEW', '2024-07-29 11:20:00', 'Verify disability certificates', NULL),
(26, 11, 'enrollments', 'APPROVE', '2024-07-29 11:45:00', 'Approve disability pension', 106),
(27, 12, 'citizens', 'SEARCH', '2024-07-29 14:20:00', 'Search widows eligible for pension', NULL),
(28, 12, 'enrollments', 'VIEW', '2024-07-29 14:25:00', 'Review widow pension applications', NULL),
(29, 13, 'disbursements', 'VIEW', '2024-07-29 15:30:00', 'Monitor failed payment transactions', NULL),
(30, 13, 'bank_accounts', 'UPDATE', '2024-07-29 15:35:00', 'Update bank details for failed payments', NULL),

-- Senior Officer oversight
(31, 14, 'access_log', 'VIEW', '2024-07-28 09:45:00', 'Review all officer activities', NULL),
(32, 14, 'disbursements', 'REPORT', '2024-07-28 10:00:00', 'Generate state-level disbursement summary', NULL),
(33, 14, 'enrollments', 'AUDIT', '2024-07-28 10:30:00', 'Audit enrollment verification process', NULL),
(34, 15, 'schemes', 'REVIEW', '2024-07-28 11:15:00', 'Annual scheme performance review', NULL),
(35, 15, 'citizens', 'ANALYTICS', '2024-07-28 11:45:00', 'Generate beneficiary demographics report', NULL),
(36, 15, 'eligibility_log', 'AUDIT', '2024-07-28 12:15:00', 'Review eligibility decision patterns', NULL),

-- Data queries and analysis
(37, 1, 'disbursements', 'QUERY', '2024-07-27 14:20:00', 'How much was disbursed for MGNREGA this month?', NULL),
(38, 2, 'citizens', 'QUERY', '2024-07-27 14:45:00', 'Show me all citizens with health conditions', NULL),
(39, 3, 'enrollments', 'QUERY', '2024-07-27 15:10:00', 'List pending PMAY applications', NULL),
(40, 4, 'bank_accounts', 'QUERY', '2024-07-27 15:35:00', 'Find accounts with failed transactions', NULL),

-- Voice assistant queries simulation
(41, 5, 'citizens', 'VOICE_QUERY', '2024-07-26 10:15:00', 'Show all female beneficiaries in my district', NULL),
(42, 6, 'schemes', 'VOICE_QUERY', '2024-07-26 10:30:00', 'What are the eligibility criteria for Ayushman Bharat?', 4),
(43, 7, 'disbursements', 'VOICE_QUERY', '2024-07-26 11:00:00', 'How many payments were processed yesterday?', NULL),
(44, 8, 'enrollments', 'VOICE_QUERY', '2024-07-26 11:30:00', 'List all active MGNREGA enrollments', NULL),
(45, 9, 'citizens', 'VOICE_QUERY', '2024-07-26 12:00:00', 'Find citizens over 70 years old', NULL),

-- Recent activity patterns
(46, 10, 'health_details', 'VIEW', '2024-07-25 09:20:00', 'Review chronic conditions for insurance claims', NULL),
(47, 11, 'villages', 'VIEW', '2024-07-25 09:45:00', 'Show villages with highest enrollment rates', NULL),
(48, 12, 'officers', 'VIEW', '2024-07-25 10:15:00', 'List officers in my state', NULL),
(49, 13, 'scheme_eligibility', 'VIEW', '2024-07-25 10:45:00', 'Review updated eligibility criteria', NULL),
(50, 14, 'disbursements', 'EXPORT', '2024-07-25 11:20:00', 'Export disbursement data for ministry report', NULL),

-- System administration activities
(51, 15, 'access_log', 'CLEANUP', '2024-07-24 16:00:00', 'Archive old access logs', NULL),
(52, 1, 'eligibility_log', 'BULK_PROCESS', '2024-07-24 16:30:00', 'Run eligibility checks for new applications', NULL),
(53, 2, 'citizens', 'DATA_VALIDATION', '2024-07-24 17:00:00', 'Validate citizen data integrity', NULL),
(54, 3, 'bank_accounts', 'RECONCILIATION', '2024-07-24 17:30:00', 'Reconcile bank account records', NULL),
(55, 4, 'disbursements', 'RETRY', '2024-07-24 18:00:00', 'Retry failed payment transactions', NULL),

-- Cross-district coordination
(56, 5, 'citizens', 'TRANSFER', '2024-07-23 14:15:00', 'Transfer citizen record to new district', 251),
(57, 6, 'enrollments', 'COORDINATE', '2024-07-23 14:45:00', 'Coordinate multi-district enrollment', NULL),
(58, 7, 'schemes', 'POLICY_UPDATE', '2024-07-23 15:15:00', 'Update scheme parameters per new policy', NULL),
(59, 8, 'officers', 'TRAINING', '2024-07-23 15:45:00', 'Access training materials for new officers', NULL),
(60, 9, 'disbursements', 'EMERGENCY', '2024-07-23 16:15:00', 'Process emergency disbursement', 106),

-- Performance monitoring
(61, 10, 'enrollments', 'PERFORMANCE', '2024-07-22 13:30:00', 'Monitor enrollment processing times', NULL),
(62, 11, 'disbursements', 'EFFICIENCY', '2024-07-22 14:00:00', 'Analyze payment processing efficiency', NULL),
(63, 12, 'citizens', 'SATISFACTION', '2024-07-22 14:30:00', 'Review beneficiary satisfaction metrics', NULL),
(64, 13, 'schemes', 'IMPACT', '2024-07-22 15:00:00', 'Assess scheme impact on poverty reduction', NULL),
(65, 14, 'health_details', 'OUTCOMES', '2024-07-22 15:30:00', 'Track health outcomes for Ayushman Bharat', NULL),

-- Data quality and compliance
(66, 15, 'citizens', 'QUALITY_CHECK', '2024-07-21 11:00:00', 'Perform data quality assessment', NULL),
(67, 1, 'enrollments', 'COMPLIANCE', '2024-07-21 11:30:00', 'Check compliance with enrollment rules', NULL),
(68, 2, 'disbursements', 'AUDIT_TRAIL', '2024-07-21 12:00:00', 'Review disbursement audit trail', NULL),
(69, 3, 'access_log', 'SECURITY', '2024-07-21 12:30:00', 'Security audit of access patterns', NULL),
(70, 4, 'bank_accounts', 'VERIFICATION', '2024-07-21 13:00:00', 'Verify bank account authenticity', NULL),

-- Recent voice assistant interactions
(71, 5, 'schemes', 'VOICE_QUERY', '2024-07-30 08:00:00', 'Tell me about welfare schemes for elderly', NULL),
(72, 6, 'citizens', 'VOICE_QUERY', '2024-07-30 08:15:00', 'How many disabled citizens are enrolled?', NULL),
(73, 7, 'disbursements', 'VOICE_QUERY', '2024-07-30 08:30:00', 'What is the total amount disbursed this year?', NULL),
(74, 8, 'enrollments', 'VOICE_QUERY', '2024-07-30 08:45:00', 'Show me pending enrollments for all schemes', NULL),
(75, 9, 'health_details', 'VOICE_QUERY', '2024-07-30 09:00:00', 'List citizens with chronic health conditions', NULL),

-- Final access entries
(76, 10, 'villages', 'DEMOGRAPHICS', '2024-07-30 17:00:00', 'Generate village-wise demographic report', NULL),
(77, 11, 'districts', 'COVERAGE', '2024-07-30 17:15:00', 'Analyze scheme coverage by district', NULL),
(78, 12, 'states', 'COMPARISON', '2024-07-30 17:30:00', 'Compare state-wise performance metrics', NULL),
(79, 13, 'officers', 'WORKLOAD', '2024-07-30 17:45:00', 'Analyze officer workload distribution', NULL),
(80, 14, 'scheme_eligibility', 'OPTIMIZATION', '2024-07-30 18:00:00', 'Optimize eligibility criteria for better reach', NULL);

-- =====================================================
-- DATA SUMMARY
-- =====================================================
-- Total Records Generated:
-- States: 15
-- Districts: 80  
-- Villages: 80
-- Schemes: 5 (Exactly as specified - MGNREGA, PMAY, Ujjwala, Ayushman Bharat, NSAP)
-- Scheme Eligibility: 5
-- Officers: 15
-- Citizens: 300 (Diverse demographic profiles)
-- Health Details: 35 (Citizens with health conditions/disabilities)
-- Bank Accounts: 80 (Primary beneficiaries)
-- Enrollments: 200 (Citizens enrolled in the 5 welfare schemes)
-- Disbursements: 165 (Payment records across all schemes)
-- Eligibility Log: 100 (System eligibility decisions)
-- Access Log: 80 (Officer activity tracking)
-- 
-- TOTAL RECORDS: ~515 comprehensive records
-- 
-- SCHEME BREAKDOWN:
-- 1. MGNREGA (scheme_id=1): Rural employment guarantee
--    - Enrollments: 60+ records
--    - Disbursements: Wage payments (₹15,000-25,000 per beneficiary)
--
-- 2. PMAY (scheme_id=2): Affordable housing
--    - Enrollments: 40+ records  
--    - Disbursements: Housing grants (₹120,000 per approved case)
--
-- 3. Ujjwala Yojana (scheme_id=3): LPG subsidies for women
--    - Enrollments: 40+ records
--    - Disbursements: Monthly LPG subsidies (₹200 per month)
--
-- 4. Ayushman Bharat - PMJAY (scheme_id=4): Health insurance
--    - Enrollments: 30+ records
--    - Disbursements: Health insurance claims (₹5,000-15,000 per claim)
--
-- 5. NSAP (scheme_id=5): Pensions for elderly, widows, disabled
--    - Enrollments: 30+ records
--    - Disbursements: Monthly pensions (₹300-800 per month)
--
-- This dataset provides realistic representation of:
-- - Rural and urban beneficiaries across all 5 core welfare schemes
-- - Various demographics (age groups, genders, economic status)
-- - Complete workflow from enrollment to disbursement
-- - Officer access patterns and system usage
-- - Edge cases and special circumstances
-- - Geographic diversity across Indian states
-- - Realistic payment amounts and frequencies

