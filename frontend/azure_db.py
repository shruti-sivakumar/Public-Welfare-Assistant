"""
Auto-connection module for Azure Database
This will automatically connect to your Azure SQL Database when the Streamlit app starts
"""
import os
import pyodbc
import streamlit as st
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from root directory
load_dotenv(dotenv_path="../.env")
# Also try current directory as fallback
load_dotenv()

def get_azure_connection():
    """Create and return Azure SQL Database connection"""
    try:
        server = os.getenv('AZURE_SQL_SERVER')
        database = os.getenv('AZURE_SQL_DATABASE') 
        username = os.getenv('AZURE_SQL_USERNAME')
        password = os.getenv('AZURE_SQL_PASSWORD')
        driver = os.getenv('AZURE_SQL_DRIVER', 'ODBC Driver 18 for SQL Server')
        
        # If credentials are empty or missing, return None silently (demo mode)
        if not all([server, database, username, password]) or server.strip() == '' or database.strip() == '':
            logger.info("Azure SQL Database credentials not configured - running in demo mode")
            return None
            
        connection_string = (
            f"DRIVER={{{driver}}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={username};"
            f"PWD={password};"
            "Encrypt=yes;"
            "TrustServerCertificate=yes;"
            "Connection Timeout=60;"
            "Login Timeout=60;"
        )
        
        connection = pyodbc.connect(connection_string)
        logger.info(f"Successfully connected to Azure SQL Database: {database}")
        return connection
        
    except Exception as e:
        logger.error(f"Failed to connect to Azure SQL Database: {str(e)}")
        # Don't show error in UI for missing credentials - just log it
        return None

@st.cache_resource
def init_database_connection():
    """Initialize and cache the database connection"""
    return get_azure_connection()

def force_reconnect_database():
    """Force reconnection to database (clears cache)"""
    # Clear the cached connection
    init_database_connection.clear()
    # Create a new connection
    return init_database_connection()

def test_connection(show_messages=True):
    """Test the database connection"""
    conn = init_database_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 as test")
            result = cursor.fetchone()
            cursor.close()
            if result:
                if show_messages:
                    st.success("✅ Successfully connected to Azure SQL Database!")
                return True
        except Exception as e:
            if show_messages:
                st.error(f"Connection test failed: {str(e)}")
            return False
    return False

def execute_query(query, params=None):
    """Execute query using the cached connection"""
    conn = init_database_connection()
    if not conn:
        return None
        
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        # For SELECT queries, fetch results
        if query.strip().upper().startswith('SELECT'):
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            cursor.close()
            
            # Convert to list of dictionaries
            result = []
            for row in rows:
                result.append(dict(zip(columns, row)))
            return result
        else:
            # For INSERT, UPDATE, DELETE
            conn.commit()
            cursor.close()
            return {"status": "success", "rowcount": cursor.rowcount}
            
    except Exception as e:
        logger.error(f"Query execution failed: {str(e)}")
        st.error(f"Query Error: {str(e)}")
        return None
