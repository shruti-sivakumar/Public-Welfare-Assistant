"""
Pure AI-driven natural language to SQL conversion
Uses Azure OpenAI exclusively for intelligent query processing
"""
import re
import os
from typing import Dict, List, Any, Optional, Tuple
import logging
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from openai import AzureOpenAI
except ImportError:
    logger.error("OpenAI library not installed. Install with: pip install openai")
    AzureOpenAI = None

class PromptEngine:
    """Pure AI-driven natural language to SQL conversion engine"""
    
    def __init__(self):
        """Initialize the AI-driven prompt engine"""
        # Azure OpenAI configuration
        self.azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.azure_openai_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.azure_openai_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-35-turbo")
        
        # Initialize table schemas with complete structure
        self.table_schemas = self._initialize_table_schemas()
        
        logger.info("PromptEngine initialized with AI-driven processing")

    def _initialize_table_schemas(self) -> Dict[str, List[str]]:
        """Initialize complete table schemas from actual database"""
        return {
            "citizens": [
                "citizen_id (INT, PRIMARY KEY)",
                "aadhaar_no (VARCHAR(12), UNIQUE)",
                "name (VARCHAR(100))",
                "gender (VARCHAR(10))",
                "age (INT)",
                "mobile_no (VARCHAR(15))",
                "email (VARCHAR(100))",
                "village_id (INT, FOREIGN KEY to villages)",
                "date_of_birth (DATE)"
            ],
            "villages": [
                "village_id (INT, PRIMARY KEY)",
                "name (VARCHAR(100))",
                "district_id (INT, FOREIGN KEY to districts)"
            ],
            "districts": [
                "district_id (INT, PRIMARY KEY)",
                "name (VARCHAR(100))",
                "state_id (INT, FOREIGN KEY to states)"
            ],
            "states": [
                "state_id (INT, PRIMARY KEY)",
                "name (VARCHAR(100))"
            ],
            "schemes": [
                "scheme_id (INT, PRIMARY KEY)",
                "name (VARCHAR(100))",
                "description (TEXT)",
                "sector (VARCHAR(50))",
                "frequency (VARCHAR(20))",
                "benefit_type (VARCHAR(50))"
            ],
            "enrollments": [
                "enrollment_id (INT, PRIMARY KEY)",
                "citizen_id (INT, FOREIGN KEY to citizens)",
                "scheme_id (INT, FOREIGN KEY to schemes)",
                "enrollment_date (DATE)",
                "status (VARCHAR(20))",
                "last_verified (DATE)",
                "verified_by (INT, FOREIGN KEY to officers)"
            ],
            "disbursements": [
                "disbursement_id (INT, PRIMARY KEY)",
                "citizen_id (INT, FOREIGN KEY to citizens)",
                "scheme_id (INT, FOREIGN KEY to schemes)",
                "amount (DECIMAL(12,2))",
                "status (VARCHAR(20))",
                "disbursed_on (DATE)",
                "verified_by (INT, FOREIGN KEY to officers)",
                "payment_method (VARCHAR(50))"
            ],
            "health_details": [
                "health_id (INT, PRIMARY KEY)",
                "citizen_id (INT, FOREIGN KEY to citizens)",
                "chronic_conditions (TEXT)",
                "disability_status (VARCHAR(100))"
            ],
            "bank_accounts": [
                "account_id (INT, PRIMARY KEY)",
                "citizen_id (INT, FOREIGN KEY to citizens)",
                "account_no (VARCHAR(20))",
                "bank_name (VARCHAR(100))",
                "ifsc_code (VARCHAR(15))"
            ],
            "officers": [
                "officer_id (INT, PRIMARY KEY)", 
                "name (VARCHAR(100))",
                "designation (VARCHAR(100))",
                "role (VARCHAR(50))",
                "email (VARCHAR(100))",
                "district_id (INT, FOREIGN KEY to districts)"
            ],
            "verifications": [
                "verification_id (INT, PRIMARY KEY)",
                "citizen_id (INT, FOREIGN KEY to citizens)",
                "scheme_id (INT, FOREIGN KEY to schemes)",
                "status (VARCHAR(20))",
                "comments (TEXT)",
                "verified_on (DATETIME)",
                "officer_id (INT, FOREIGN KEY to officers)"
            ]
        }

    def _preprocess_query(self, query: str) -> str:
        """Intelligently preprocess the query to improve understanding"""
        # Normalize common terms
        original_query = query
        query = query.lower().strip()
        
        # Dynamic year handling - don't hardcode years
        current_year = datetime.now().year
        query = re.sub(r'\b(this year|current year)\b', f'{current_year}', query)
        query = re.sub(r'\blast year\b', f'{current_year - 1}', query)
        query = re.sub(r'\bnext year\b', f'{current_year + 1}', query)
        
        # Scheme name normalization (keep flexible)
        query = re.sub(r'\bpmay\b', 'PMAY housing scheme', query)
        query = re.sub(r'\bnsap\b', 'NSAP pension scheme', query)
        query = re.sub(r'\bmgnrega\b', 'MGNREGA employment scheme', query)
        query = re.sub(r'\bujjwala\b', 'Ujjwala gas scheme', query)
        query = re.sub(r'\bayushman\b', 'Ayushman Bharat health scheme', query)
        
        # Location normalization
        query = re.sub(r'\brural\b', 'rural villages', query)
        query = re.sub(r'\burban\b', 'urban areas', query)
        
        # Disability normalization (make more flexible)
        query = re.sub(r'disability.*above.*(\d+)%', r'severe disability conditions above \1 percent', query)
        query = re.sub(r'disabled.*citizens', 'citizens with disabilities', query)
        
        # Amount normalization (keep flexible)
        query = re.sub(r'(\d+)\s*lakh', r'\1 hundred thousand rupees', query)
        query = re.sub(r'₹\s*(\d+)', r'\1 rupees', query)
        
        # Time period normalization
        query = re.sub(r'\bin\s+(\d{4})\b', r'during year \1', query)
        query = re.sub(r'\bfor\s+(\d{4})\b', r'during year \1', query)
        
        # Make query more SQL-friendly
        query = re.sub(r'\bhow many\b', 'count', query)
        query = re.sub(r'\bshow me\b', 'list', query)
        query = re.sub(r'\bfind\b', 'select', query)
        
        return query
        
    def _try_azure_openai(self, query: str) -> Optional[str]:
        """Use Azure OpenAI to convert natural language to SQL"""
        if not self.azure_openai_key or not self.azure_openai_endpoint:
            logger.error("Azure OpenAI credentials not configured")
            return None
            
        # Preprocess query for better understanding
        processed_query = self._preprocess_query(query)
            
        try:
            client = AzureOpenAI(
                api_key=self.azure_openai_key,
                api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
                azure_endpoint=self.azure_openai_endpoint,
            )
            
            # Create complete schema context
            schema_context = self._build_schema_context()
            
            prompt = f"""
            You are an expert SQL Server developer. Convert this natural language query to syntactically perfect SQL.

            QUERY: "{processed_query}"
            ORIGINAL: "{query}"

            {schema_context}

            🎯 MANDATORY SQL SERVER REQUIREMENTS:

            1. ABSOLUTE SYNTAX RULES:
            - Use TOP N instead of LIMIT N (SQL Server doesn't support LIMIT)
            - Every non-aggregate column in SELECT MUST be in GROUP BY
            - Use proper JOIN syntax with table aliases
            - Handle NULL values with proper LEFT JOIN or IS NULL checks
            
            2. DISBURSEMENTS TABLE CRITICAL:
            - disbursements table has NO enrollment_id column!
            - JOIN disbursements: FROM citizens c JOIN disbursements d ON c.citizen_id = d.citizen_id
            - For scheme filtering: JOIN schemes s ON d.scheme_id = s.scheme_id
            - NEVER write: d.enrollment_id = e.enrollment_id (this column doesn't exist!)
            
            3. GROUP BY LOGIC:
            - If SELECT has: c.name, c.citizen_id, COUNT(e.scheme_id)
            - Then GROUP BY must have: c.citizen_id, c.name
            - All non-aggregate SELECT columns must be in GROUP BY
            - Use HAVING for aggregate filtering (not WHERE)
            
            4. DYNAMIC DATE HANDLING:
            - Don't hardcode years like 2024
            - Use YEAR(GETDATE()) for current year
            - Use YEAR(date_column) = YEAR(GETDATE()) for current year filtering
            - Use DATEPART or YEAR() functions properly
            
            5. FLEXIBLE SCHEME MATCHING:
            - Use LIKE patterns, not hardcoded IDs
            - PMAY/housing: (s.name LIKE '%PMAY%' OR s.name LIKE '%housing%' OR s.name LIKE '%Awas%')
            - Employment: (s.name LIKE '%MGNREGA%' OR s.name LIKE '%employment%' OR s.name LIKE '%work%')
            - Pension: (s.name LIKE '%NSAP%' OR s.name LIKE '%pension%' OR s.name LIKE '%elderly%')
            - Gas: (s.name LIKE '%Ujjwala%' OR s.name LIKE '%gas%' OR s.name LIKE '%LPG%')
            - Health: (s.name LIKE '%Ayushman%' OR s.name LIKE '%health%' OR s.name LIKE '%medical%')
            
            6. ROBUST TABLE RELATIONSHIPS:
            - Geographic hierarchy: citizens → villages → districts → states
            - Program data: citizens → enrollments → schemes
            - Financial data: citizens → disbursements → schemes (NO enrollment_id link!)
            - Personal data: citizens → health_details, citizens → bank_accounts
            
            7. ERROR PREVENTION:
            - Always use table aliases (c, e, s, d, v, dt, st, h, ba, o)
            - Include proper WHERE clauses for data filtering
            - Use ORDER BY for meaningful result sorting
            - Handle empty results gracefully
            
            Generate ONLY the SQL query (no explanations):
            """
            
            response = client.chat.completions.create(
                model=self.azure_openai_deployment,
                messages=[
                    {"role": "system", "content": "You are a SQL expert. Convert natural language to SQL queries using the provided schema."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.1
            )
            
            sql = response.choices[0].message.content.strip()
            # Clean up the response
            sql = sql.replace("```sql", "").replace("```", "").strip()
            
            return self._auto_correct_sql_dialect(sql)
            
        except Exception as e:
            logger.error(f"Azure OpenAI processing failed: {e}")
            return None

    def _build_schema_context(self) -> str:
        """Build complete schema context for OpenAI prompt"""
        context = "DATABASE SCHEMA:\n"
        for table, columns in self.table_schemas.items():
            context += f"\n{table.upper()}:\n"
            for column in columns:
                context += f"  - {column}\n"
        
        context += "\nKEY RELATIONSHIPS:\n"
        context += "- citizens.village_id -> villages.village_id\n"
        context += "- villages.district_id -> districts.district_id\n" 
        context += "- districts.state_id -> states.state_id\n"
        context += "- enrollments.citizen_id -> citizens.citizen_id\n"
        context += "- enrollments.scheme_id -> schemes.scheme_id\n"
        context += "- disbursements.citizen_id -> citizens.citizen_id\n"
        context += "- disbursements.scheme_id -> schemes.scheme_id\n"
        context += "- health_details.citizen_id -> citizens.citizen_id\n"
        context += "- bank_accounts.citizen_id -> citizens.citizen_id\n"
        
        context += "\n🎯 INTELLIGENT QUERY PATTERNS:\n"
        context += "SCHEME RECOGNITION (Use LIKE patterns, NO hardcoded IDs):\n"
        context += "- 'PMAY' = 'housing' = 'Awas' → s.name LIKE '%PMAY%' OR s.name LIKE '%housing%'\n"  
        context += "- 'MGNREGA' = 'employment' = 'work' → s.name LIKE '%MGNREGA%' OR s.name LIKE '%employment%'\n"
        context += "- 'NSAP' = 'pension' = 'elderly' → s.name LIKE '%NSAP%' OR s.name LIKE '%pension%'\n"
        context += "- 'Ujjwala' = 'gas' = 'LPG' → s.name LIKE '%Ujjwala%' OR s.name LIKE '%gas%'\n"
        context += "- 'Ayushman' = 'health' = 'medical' → s.name LIKE '%Ayushman%' OR s.name LIKE '%health%'\n"
        
        context += "\nLOCATION INTELLIGENCE:\n"
        context += "- For 'Gujarat citizens': JOIN to states.name LIKE '%Gujarat%'\n"
        context += "- For 'Mumbai district': JOIN to districts.name LIKE '%Mumbai%'\n"
        context += "- For 'rural areas': villages.name LIKE '%Rural%'\n"
        
        context += "\nDISABILITY INTELLIGENCE:\n"
        context += "- 'above 70%': disability_status LIKE '%80%' OR LIKE '%90%' OR LIKE '%100%'\n"
        context += "- 'disabled': disability_status IS NOT NULL AND != 'None'\n"
        context += "- Values: 'Physical disability - 60%', 'Visual impairment - 80%', etc.\n"
        
        context += "\nCRITICAL TABLE STRUCTURE:\n"
        context += "- disbursements: NO enrollment_id column! Join using citizen_id + scheme_id\n"
        context += "- citizens: Use village_id to join with villages table\n"
        context += "- health_details: disability_status field (text like 'Physical disability - 60%')\n"
        context += "- Date fields: disbursed_on, enrollment_date, verified_on\n"
        context += "- All JOINs must use proper foreign key relationships\n"
        
        context += "\nCORRECT JOIN PATTERNS:\n"
        context += "- Disbursements: FROM citizens c JOIN disbursements d ON c.citizen_id = d.citizen_id\n"
        context += "- With Schemes: JOIN schemes s ON d.scheme_id = s.scheme_id\n"
        context += "- Location: JOIN villages v ON c.village_id = v.village_id\n"
        context += "- Districts: JOIN districts dt ON v.district_id = dt.district_id\n"
        context += "- States: JOIN states st ON dt.state_id = st.state_id\n"
        
        return context

    def _validate_and_fix_sql(self, sql: str) -> str:
        """Intelligently validate and fix SQL query"""
        # Remove duplicate spaces and normalize
        sql = re.sub(r'\s+', ' ', sql.strip())
        
        # SQL Server specific corrections - LIMIT to TOP
        limit_match = re.search(r"LIMIT\s+(\d+)", sql, re.IGNORECASE)
        if limit_match:
            n = limit_match.group(1)
            sql = re.sub(r"\s*LIMIT\s+\d+\s*;?\s*$", "", sql, flags=re.IGNORECASE)
            if not re.search(r"SELECT\s+TOP\s+\d+", sql, re.IGNORECASE):
                sql = re.sub(r"SELECT\b", f"SELECT TOP {n}", sql, flags=re.IGNORECASE)
        
        # Fix common column name errors based on actual schema
        sql = re.sub(r'\benrollment_id\b', 'e.enrollment_id', sql, flags=re.IGNORECASE)
        sql = re.sub(r'\bdisability_percentage\b', 'disability_status', sql, flags=re.IGNORECASE)
        
        # Fix disbursements table - NO enrollment_id column exists
        # disbursements table has: citizen_id, scheme_id directly (not through enrollment_id)
        sql = re.sub(r'disbursements\s+d\s+ON\s+d\.enrollment_id\s*=\s*e\.enrollment_id', 
                    'disbursements d ON d.citizen_id = e.citizen_id AND d.scheme_id = e.scheme_id', sql, flags=re.IGNORECASE)
        
        # Fix GROUP BY issues - add missing columns to GROUP BY
        sql = self._fix_group_by_issues(sql)
        
        # Fix column aliases and references
        sql = self._fix_column_references(sql)
        
        # Auto-add required JOINs if missing
        if 'village' in sql.lower() and 'citizens' in sql.lower() and 'join villages' not in sql.lower():
            sql = self._add_missing_joins(sql, 'villages')
        
        if 'district' in sql.lower() and 'join districts' not in sql.lower():
            sql = self._add_missing_joins(sql, 'districts')
            
        if 'state' in sql.lower() and 'join states' not in sql.lower():
            sql = self._add_missing_joins(sql, 'states')
            
        if 'disability' in sql.lower() and 'join health_details' not in sql.lower():
            sql = self._add_missing_joins(sql, 'health_details')
        
        return sql.strip()
    
    def _fix_group_by_issues(self, sql: str) -> str:
        """Fix GROUP BY clause to include all non-aggregate columns"""
        # More robust GROUP BY fixing
        if 'GROUP BY' not in sql.upper():
            return sql
            
        # Find SELECT and GROUP BY clauses
        select_match = re.search(r'SELECT\s+(TOP\s+\d+\s+)?(.*?)\s+FROM', sql, re.IGNORECASE | re.DOTALL)
        group_by_match = re.search(r'GROUP\s+BY\s+(.*?)(?:\s+HAVING|\s+ORDER|\s*$)', sql, re.IGNORECASE | re.DOTALL)
        
        if not select_match or not group_by_match:
            return sql
            
        select_part = select_match.group(2) if select_match.group(2) else select_match.group(1)
        group_by_part = group_by_match.group(1).strip()
        
        # Extract non-aggregate columns from SELECT
        select_columns = []
        for col in select_part.split(','):
            col = col.strip()
            # Skip aggregate functions, CASE statements, and literals
            if not re.search(r'\b(COUNT|SUM|AVG|MAX|MIN|STRING_AGG|FORMAT)\s*\(', col, re.IGNORECASE):
                if not re.search(r'^\s*CASE\s+', col, re.IGNORECASE):
                    if not re.search(r'^\s*[\'"]\w+[\'"]\s*$', col):  # Skip string literals
                        # Extract column name (handle aliases)
                        base_col = col
                        if ' AS ' in col.upper():
                            base_col = col.split(' AS ')[0].strip()
                        if base_col and base_col not in ['*']:
                            select_columns.append(base_col)
        
        # Get existing GROUP BY columns
        existing_group_by = [col.strip() for col in group_by_part.split(',') if col.strip()]
        
        # Add missing columns to GROUP BY
        for col in select_columns:
            # Check if column is already in GROUP BY (partial match)
            col_found = False
            for existing_col in existing_group_by:
                if col in existing_col or existing_col in col:
                    col_found = True
                    break
            
            if not col_found and col not in group_by_part:
                if group_by_part:
                    group_by_part += f", {col}"
                else:
                    group_by_part = col
        
        # Replace GROUP BY clause
        if group_by_part:
            sql = re.sub(r'GROUP\s+BY\s+.*?(?=\s+HAVING|\s+ORDER|\s*$)', 
                        f'GROUP BY {group_by_part}', sql, flags=re.IGNORECASE)
        
        return sql
    
    def _fix_column_references(self, sql: str) -> str:
        """Fix common column reference issues"""
        # Fix citizens.name references (should be just 'name' based on schema)
        sql = re.sub(r'citizens\.name', 'c.name', sql, flags=re.IGNORECASE)
        sql = re.sub(r'citizens\.citizen_id', 'c.citizen_id', sql, flags=re.IGNORECASE)
        
        # Fix scheme name references
        sql = re.sub(r'schemes\.name', 's.name', sql, flags=re.IGNORECASE)
        
        # Fix common issues with HAVING COUNT
        sql = re.sub(r'HAVING\s+COUNT\s*\(\s*ba\.account_id\s*\)\s*>\s*1', 
                    'HAVING COUNT(DISTINCT ba.account_id) > 1', sql, flags=re.IGNORECASE)
        
        return sql
    
    def _add_missing_joins(self, sql: str, target_table: str) -> str:
        """Intelligently add missing JOINs"""
        if target_table == 'villages':
            if 'FROM citizens' in sql and 'JOIN villages' not in sql:
                sql = sql.replace('FROM citizens', 'FROM citizens JOIN villages ON citizens.village_id = villages.village_id')
        elif target_table == 'districts':
            if 'JOIN villages' in sql and 'JOIN districts' not in sql:
                sql = sql.replace('JOIN villages ON', 'JOIN villages ON citizens.village_id = villages.village_id JOIN districts ON villages.district_id = districts.district_id')
        elif target_table == 'states':
            if 'JOIN districts' in sql and 'JOIN states' not in sql:
                sql = sql.replace('JOIN districts ON', 'JOIN districts ON villages.district_id = districts.district_id JOIN states ON districts.state_id = states.state_id')
        elif target_table == 'health_details':
            if 'FROM citizens' in sql and 'JOIN health_details' not in sql:
                sql = sql.replace('FROM citizens', 'FROM citizens LEFT JOIN health_details ON citizens.citizen_id = health_details.citizen_id')
        
        return sql
    
    def _auto_correct_sql_dialect(self, sql: str) -> str:
        """Auto-correct SQL syntax for SQL Server (legacy method)"""
        return self._validate_and_fix_sql(sql)

    def _try_pattern_based_sql(self, query: str) -> Optional[str]:
        """Fallback pattern-based SQL generation when Azure OpenAI is not available"""
        query_lower = query.lower()
        
        # Pattern 1: Total disbursement by scheme
        if re.search(r'total.*disbursement.*scheme', query_lower):
            return """SELECT s.name AS scheme_name, SUM(d.amount) AS total_disbursement_amount 
FROM disbursements d 
JOIN schemes s ON d.scheme_id = s.scheme_id 
GROUP BY s.scheme_id, s.name 
ORDER BY total_disbursement_amount DESC"""
        
        # Pattern 2: Citizens receiving maximum benefits
        if re.search(r'citizens.*receiv.*maximum.*benefit', query_lower):
            return """SELECT TOP 100 c.citizen_id, c.name, SUM(d.amount) AS total_benefit 
FROM citizens c 
JOIN disbursements d ON c.citizen_id = d.citizen_id 
GROUP BY c.citizen_id, c.name 
ORDER BY total_benefit DESC"""
        
        # Pattern 3: Citizens in multiple schemes
        if re.search(r'citizens.*multiple.*scheme', query_lower):
            return """SELECT c.citizen_id, c.name AS citizen_name, c.aadhaar_no, COUNT(DISTINCT e.scheme_id) AS scheme_count
FROM citizens c 
JOIN enrollments e ON c.citizen_id = e.citizen_id
GROUP BY c.citizen_id, c.name, c.aadhaar_no
HAVING COUNT(DISTINCT e.scheme_id) > 1
ORDER BY scheme_count DESC"""
        
        # Pattern 4: Officers verification activity
        if re.search(r'officer.*verification.*activity', query_lower):
            return """SELECT dt.name AS district_name, o.name AS officer_name, o.designation, COUNT(v.verification_id) AS verification_activity_count 
FROM officers o 
JOIN districts dt ON o.district_id = dt.district_id 
JOIN verifications v ON o.officer_id = v.officer_id 
GROUP BY dt.district_id, dt.name, o.officer_id, o.name, o.designation
ORDER BY district_name, verification_activity_count DESC"""
        
        # Pattern 5: Female citizens with age filter
        if re.search(r'female.*citizen', query_lower) and re.search(r'age|aged', query_lower):
            return """SELECT c.citizen_id, c.name, c.age, c.mobile_no, e.enrollment_date, e.status
FROM citizens c
JOIN enrollments e ON c.citizen_id = e.citizen_id
JOIN schemes s ON e.scheme_id = s.scheme_id
WHERE c.gender = 'Female' 
  AND c.age BETWEEN 18 AND 30
ORDER BY c.age"""
        
        # Pattern 6: Monthly disbursement trends
        if re.search(r'monthly.*disbursement.*trend', query_lower):
            return """SELECT MONTH(d.disbursed_on) AS month_number, 
       COUNT(d.disbursement_id) AS disbursement_count,
       SUM(d.amount) AS monthly_total,
       AVG(d.amount) AS average_amount
FROM disbursements d
JOIN schemes s ON d.scheme_id = s.scheme_id
GROUP BY MONTH(d.disbursed_on)
ORDER BY month_number"""
        
        # Pattern 7: Citizens without bank accounts
        if re.search(r'citizens.*without.*bank.*account', query_lower):
            return """SELECT c.citizen_id, c.name, c.mobile_no, c.email, 
       SUM(d.amount) AS total_disbursed
FROM citizens c
JOIN disbursements d ON c.citizen_id = d.citizen_id
LEFT JOIN bank_accounts ba ON c.citizen_id = ba.citizen_id
WHERE ba.account_id IS NULL
GROUP BY c.citizen_id, c.name, c.mobile_no, c.email
ORDER BY total_disbursed DESC"""
        
        return None

    def convert_to_sql(self, query: str) -> Dict[str, Any]:
        """Main method to convert natural language query to SQL"""
        try:
            logger.info(f"Processing query: '{query}'")
            
            # Try Azure OpenAI first
            sql = self._try_azure_openai(query)
            method = "azure_openai"
            
            # Fallback to pattern-based if Azure OpenAI fails
            if not sql:
                logger.info("Azure OpenAI not available, trying pattern-based approach")
                sql = self._try_pattern_based_sql(query)
                method = "pattern_based"
            
            if sql:
                return {
                    "status": "success",
                    "success": True,
                    "sql_query": sql,
                    "original_query": query,
                    "method": method,
                    "confidence": 0.8 if method == "azure_openai" else 0.6,
                    "chart_type": "table"
                }
            
            # Failed to convert
            return {
                "status": "error",
                "success": False,
                "message": "Could not convert query to SQL. Please try rephrasing or be more specific.",
                "error": "Could not convert query to SQL",
                "original_query": query,
                "suggestions": [
                    "Try: 'Total disbursement amount by scheme'",
                    "Try: 'Citizens receiving maximum benefits'",
                    "Try: 'Citizens enrolled in multiple schemes'",
                    "Try: 'Officers with highest verification activity'",
                    "Try: 'Female citizens aged 18-30'",
                    "Try: 'Monthly disbursement trends'"
                ]
            }
            
        except Exception as e:
            logger.error(f"Error in convert_to_sql: {e}")
            return {
                "status": "error",
                "success": False,
                "message": f"Processing error: {str(e)}",
                "error": str(e),
                "original_query": query
            }

    def process_query(self, query: str) -> Dict[str, Any]:
        """Main method to process natural language queries (called by API routes)"""
        return self.convert_to_sql(query)

    def natural_language_to_sql(self, query: str) -> Dict[str, Any]:
        """Convert natural language query to SQL"""
        return self.convert_to_sql(query)

# Global instance
prompt_engine = PromptEngine()

def convert_natural_language_to_sql(query: str) -> Dict[str, Any]:
    """Global function to convert natural language to SQL"""
    return prompt_engine.convert_to_sql(query)