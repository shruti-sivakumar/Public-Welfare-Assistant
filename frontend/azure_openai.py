"""
Azure OpenAI integration for Natural Language to SQL conversion
Direct integration with Azure OpenAI service for the Streamlit frontend
"""
import os
from openai import AzureOpenAI
from dotenv import load_dotenv
import streamlit as st
import logging
import json

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Azure OpenAI client
@st.cache_resource
def get_azure_openai_client():
    """Initialize and cache the Azure OpenAI client"""
    try:
        client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        )
        logger.info("Azure OpenAI client initialized successfully")
        return client
    except Exception as e:
        logger.error(f"Failed to initialize Azure OpenAI client: {str(e)}")
        st.error(f"OpenAI Connection Error: {str(e)}")
        return None

def get_database_schema_context():
    """Get database schema context for better SQL generation"""
    schema_context = """
    You are a SQL expert working with a welfare database with the following EXACT table structure:

    ACTUAL Tables and Columns:
    1. citizens: citizen_id, aadhaar_no, name, gender, age, mobile_no, email, village_id
    2. villages: village_id, name, district_id  
    3. districts: district_id, name, state_id
    4. states: state_id, name
    5. schemes: scheme_id, name, description, sector, frequency, benefit_type
    6. enrollments: enrollment_id, citizen_id, scheme_id, enrollment_date, status, last_verified_on, verified_by
    7. disbursements: disbursement_id, citizen_id, scheme_id, amount, status, disbursed_on, approved_by, payment_mode
    8. officers: officer_id, name, designation, access_level, email, district_id
    9. health_details: citizen_id, chronic_conditions, disability_status
    10. bank_accounts: account_id, citizen_id, account_no, bank_name, ifsc_code
    11. scheme_eligibility: scheme_id, min_age, max_age, gender, category_required, min_income, disability_required

    IMPORTANT RELATIONSHIPS:
    - citizens.village_id -> villages.village_id
    - villages.district_id -> districts.district_id  
    - districts.state_id -> states.state_id
    - enrollments.citizen_id -> citizens.citizen_id
    - enrollments.scheme_id -> schemes.scheme_id
    - disbursements.citizen_id -> citizens.citizen_id
    - disbursements.scheme_id -> schemes.scheme_id
    - health_details.citizen_id -> citizens.citizen_id
    - bank_accounts.citizen_id -> citizens.citizen_id
    - officers.district_id -> districts.district_id

    CRITICAL NOTES:
    - DISBURSEMENTS TABLE: Does NOT have enrollment_id column! Only has citizen_id and scheme_id
    - To connect disbursements to enrollments: JOIN disbursements d ON d.citizen_id = e.citizen_id AND d.scheme_id = e.scheme_id
    - NEVER use 'disbursements.enrollment_id' - this column does not exist!
    - CITIZENS TABLE: Does NOT have 'state', 'district', 'disability_percentage', 'bank_account' columns
    - To get state/district for citizens: JOIN citizens -> villages -> districts -> states
    - To get disability info: MUST JOIN citizens -> health_details (use disability_status, NOT disability_percentage)
    - To get bank info: MUST JOIN citizens -> bank_accounts
    - DISABILITY: ALWAYS include 'JOIN health_details hd ON c.citizen_id = hd.citizen_id' when using disability_status
    - NEVER reference hd.disability_status without the JOIN - will cause 'could not be bound' error
    - DISABILITY: Use health_details.disability_status (VARCHAR like 'Physical', 'None'), NOT disability_percentage (doesn't exist)
    - DATE COLUMNS: Use disbursed_on for disbursements, enrollment_date for enrollments
    - NEVER use columns like c.state, c.district, c.disability_percentage, c.bank_account
    - CRITICAL: There is NO 'type', 'area_type', or 'rural_urban' column in ANY table!
    - NEVER use WHERE v.type = 'rural' or c.area_type = 'Rural' - these columns don't exist!
    - For rural/urban queries: Use village names that contain 'Rural' in the name
    - Example: WHERE v.name LIKE '%Rural%' for rural areas
    - Use proper table aliases (c for citizens, v for villages, dt for districts, st for states, hd for health_details, ba for bank_accounts)

    SQL SYNTAX RULES:
    - GROUP BY: All non-aggregate columns in SELECT must be in GROUP BY clause
    - DATA TYPES: health_details.chronic_conditions is TEXT, use LIKE or = for text comparison, not > numeric
    - AGGREGATE FUNCTIONS: COUNT(), SUM(), AVG() don't need table prefix in GROUP BY
    - TEXT COMPARISON: Use 'Physical' not 70 for disability_status comparison
    - NUMERIC FIELDS: Only amount, citizen_id, scheme_id, etc. are numeric
    - CORRECT SYNTAX: SELECT c.name, COUNT(*) FROM citizens c GROUP BY c.name
    - WRONG SYNTAX: SELECT c.name, s.name FROM citizens c GROUP BY c.name (missing s.name in GROUP BY)

    CRITICAL COLUMN ERRORS TO AVOID:
    - villages table has NO 'type' column - NEVER use v.type = 'rural'
    - citizens table has NO 'state', 'district', 'area_type' columns
    - For rural/urban: Check village names for patterns like 'Rural' in name
    - For disability queries: MUST JOIN health_details table: JOIN health_details hd ON c.citizen_id = hd.citizen_id
    - disbursements table has NO enrollment_id - use citizen_id and scheme_id

    INTELLIGENT QUERY MATCHING RULES:
    - FLEXIBLE TEXT MATCHING: Always use LIKE with wildcards for text searches
    - SCHEME NAMES: Use LIKE '%PMAY%' or LIKE '%NSAP%' or LIKE '%Ujjwala%' - data may have variations
    - DISABILITY: ALWAYS JOIN health_details: JOIN health_details hd ON c.citizen_id = hd.citizen_id

    FLEXIBLE MATCHING EXAMPLES:
    - 'disability above 70%': WHERE (hd.disability_status LIKE '%80%' OR hd.disability_status LIKE '%90%' OR hd.disability_status LIKE '%100%')
    - 'PMAY scheme': WHERE (s.name LIKE '%PMAY%' OR s.name LIKE '%housing%' OR s.name LIKE '%Awas%')
    - 'Mumbai district': WHERE (d.name LIKE '%Mumbai%' OR v.name LIKE '%Mumbai%')
    - 'disabled citizens': WHERE (hd.disability_status IS NOT NULL AND hd.disability_status != 'None')
    - 'elderly above 60': WHERE DATEDIFF(YEAR, c.date_of_birth, GETDATE()) >= 60

    EXAMPLE CORRECT QUERIES:
    - "Citizens from Mumbai district": 
      SELECT c.name, c.age FROM citizens c 
      JOIN villages v ON c.village_id = v.village_id 
      JOIN districts d ON v.district_id = d.district_id 
      WHERE d.name = 'Mumbai'
    
    - "PMAY enrollments in Odisha": 
      SELECT c.name, e.enrollment_date FROM enrollments e
      JOIN citizens c ON e.citizen_id = c.citizen_id
      JOIN villages v ON c.village_id = v.village_id
      JOIN districts d ON v.district_id = d.district_id
      JOIN states st ON d.state_id = st.state_id
      JOIN schemes s ON e.scheme_id = s.scheme_id
      WHERE s.name = 'PMAY' AND st.name = 'Odisha'
    
    - "Count of citizens": SELECT COUNT(*) as citizen_count FROM citizens
    - "All schemes": SELECT scheme_id, name, description, sector FROM schemes
    """
    return schema_context

def natural_language_to_sql(user_query: str, show_reasoning: bool = False):
    """
    Convert natural language query to SQL using Azure OpenAI
    
    Args:
        user_query: Natural language query from user
        show_reasoning: Whether to show the AI's reasoning process
        
    Returns:
        dict: Contains sql_query, explanation, and any errors
    """
    client = get_azure_openai_client()
    if not client:
        return {"error": "Azure OpenAI client not available"}
    
    try:
        schema_context = get_database_schema_context()
        
        prompt = f"""
        {schema_context}
        
        Convert this natural language query to SQL:
        "{user_query}"
        
        Requirements:
        1. Generate ONLY valid SQL Server T-SQL syntax
        2. Use appropriate JOINs when multiple tables are needed
        3. Include proper WHERE clauses for filtering
        4. Use COUNT, SUM, AVG etc. for aggregations when needed
        5. Return TOP 100 results by default for SELECT queries
        6. Use meaningful column aliases
        
        Response format (JSON):
        {{
            "sql_query": "your SQL query here",
            "explanation": "brief explanation of what the query does",
            "query_type": "SELECT/INSERT/UPDATE/DELETE",
            "tables_used": ["table1", "table2"]
        }}
        
        Important: Respond with ONLY the JSON, no other text.
        """
        
        response = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            messages=[
                {"role": "system", "content": "You are a SQL expert. Convert natural language to SQL queries for a welfare database. Respond only with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,  # Low temperature for more consistent SQL generation
            max_tokens=800
        )
        
        result_text = response.choices[0].message.content.strip()
        
        if show_reasoning:
            st.info(f"AI Response: {result_text}")
        
        # Parse the JSON response
        try:
            result = json.loads(result_text)
            logger.info(f"Generated SQL for query '{user_query}': {result.get('sql_query')}")
            return result
        except json.JSONDecodeError as e:
            # Fallback: try to extract SQL from response
            logger.warning(f"Failed to parse JSON response: {e}")
            
            # Try to find SQL in the response
            sql_start_markers = ["SELECT", "INSERT", "UPDATE", "DELETE", "WITH"]
            for marker in sql_start_markers:
                if marker in result_text.upper():
                    # Extract potential SQL
                    lines = result_text.split('\n')
                    sql_lines = []
                    capturing = False
                    
                    for line in lines:
                        line_upper = line.strip().upper()
                        if any(marker in line_upper for marker in sql_start_markers):
                            capturing = True
                        
                        if capturing:
                            sql_lines.append(line.strip())
                            # Stop at semicolon or empty line after SQL
                            if line.strip().endswith(';') or (len(sql_lines) > 1 and line.strip() == ''):
                                break
                    
                    if sql_lines:
                        return {
                            "sql_query": ' '.join(sql_lines).rstrip(';'),
                            "explanation": f"Generated SQL for: {user_query}",
                            "query_type": "SELECT",
                            "tables_used": ["unknown"]
                        }
            
            return {"error": f"Failed to parse AI response: {result_text[:200]}..."}
            
    except Exception as e:
        logger.error(f"Error in natural_language_to_sql: {str(e)}")
        return {"error": f"OpenAI API error: {str(e)}"}

def test_openai_connection():
    """Test the Azure OpenAI connection"""
    try:
        client = get_azure_openai_client()
        if not client:
            return False
            
        # Simple test query
        response = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            messages=[{"role": "user", "content": "Say 'Hello from Azure OpenAI!'"}],
            max_tokens=50
        )
        
        result = response.choices[0].message.content
        logger.info(f"OpenAI test successful: {result}")
        return True
        
    except Exception as e:
        logger.error(f"OpenAI test failed: {str(e)}")
        return False