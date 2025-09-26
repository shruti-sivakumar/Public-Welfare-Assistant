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
    6. enrollments: enrollment_id, citizen_id, scheme_id, enrollment_date, status, officer_id
    7. disbursements: disbursement_id, enrollment_id, amount, disbursement_date, status, transaction_id  
    8. officers: officer_id, name, designation, access_level, email, district_id

    IMPORTANT RELATIONSHIPS:
    - citizens.village_id -> villages.village_id
    - villages.district_id -> districts.district_id  
    - districts.state_id -> states.state_id
    - enrollments.citizen_id -> citizens.citizen_id
    - enrollments.scheme_id -> schemes.scheme_id
    - disbursements.enrollment_id -> enrollments.enrollment_id
    - officers.district_id -> districts.district_id

    CRITICAL NOTES:
    - Citizens do NOT have direct 'district' or 'income' columns
    - To get district name for citizens: JOIN citizens -> villages -> districts
    - To get state name for citizens: JOIN citizens -> villages -> districts -> states
    - Use proper table aliases (c for citizens, v for villages, d for districts, s for states)

    EXAMPLE CORRECT QUERIES:
    - "Citizens from Mumbai district": 
      SELECT c.name, c.age FROM citizens c 
      JOIN villages v ON c.village_id = v.village_id 
      JOIN districts d ON v.district_id = d.district_id 
      WHERE d.name = 'Mumbai'
    
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