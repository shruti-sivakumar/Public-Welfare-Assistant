import pyodbc
import pandas as pd
import streamlit as st
import os
from typing import Optional, List
import logging

# Try to load .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # If dotenv not available, try to load .env manually
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value.strip('"\'')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WelfareDatabase:
    def __init__(self):
        self.connection_string = None
        self.connection = None
        self._initialize_connection_string()
        
    def _initialize_connection_string(self):
        server = os.getenv('AZURE_SQL_SERVER')
        database = os.getenv('AZURE_SQL_DATABASE')
        username = os.getenv('AZURE_SQL_USERNAME')
        password = os.getenv('AZURE_SQL_PASSWORD')
        
        if all([server, database, username, password]):
            self.connection_string = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};"
    
    def connect(self) -> bool:
        try:
            if not self.connection_string:
                return False
            self.connection = pyodbc.connect(self.connection_string)
            return True
        except Exception:
            return False
    
    def test_connection(self, show_messages: bool = True) -> bool:
        try:
            if self.connect():
                if show_messages:
                    st.success("Database connection successful!")
                return True
            else:
                if show_messages:
                    st.info("Database not configured - using sample data")
                return False
        except Exception:
            if show_messages:
                st.warning("Database connection unavailable - using sample data")
            return False
    
    def execute_query(self, query: str, params: tuple = None) -> Optional[pd.DataFrame]:
        connection = None
        try:
            if not self.connection_string:
                return None
            connection = pyodbc.connect(self.connection_string)
            cursor = connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            rows = cursor.fetchall()
            if rows:
                columns = [desc[0] for desc in cursor.description]
                df = pd.DataFrame.from_records(rows, columns=columns)
                return df
            return pd.DataFrame()
        except Exception as e:
            logger.error(f"Database query error: {e}")
            return None
        finally:
            if connection:
                connection.close()
    
    def get_schemes(self) -> pd.DataFrame:
        query = """
        SELECT s.name as scheme_name, 
               COUNT(DISTINCT e.enrollment_id) as total_enrollments, 
               COALESCE(SUM(d.amount), 0) as total_disbursements 
        FROM schemes s 
        LEFT JOIN enrollments e ON s.scheme_id = e.scheme_id 
        LEFT JOIN disbursements d ON s.scheme_id = d.scheme_id 
        GROUP BY s.scheme_id, s.name
        """
        result = self.execute_query(query)
        return result if result is not None else pd.DataFrame()
    
    def get_citizens_count(self) -> int:
        query = "SELECT COUNT(DISTINCT citizen_id) as total_citizens FROM citizens"
        result = self.execute_query(query)
        if result is not None and not result.empty:
            return int(result.iloc[0]['total_citizens'])
        return 0
    
    def get_disbursements_summary(self) -> pd.DataFrame:
        query = """
        SELECT s.name as scheme_name, 
               COALESCE(SUM(d.amount), 0) as total_amount 
        FROM schemes s 
        LEFT JOIN disbursements d ON s.scheme_id = d.scheme_id 
        GROUP BY s.scheme_id, s.name
        """
        result = self.execute_query(query)
        return result if result is not None else pd.DataFrame()
    
    def get_total_disbursements(self) -> float:
        query = "SELECT COALESCE(SUM(amount), 0) as total_disbursements FROM disbursements"
        result = self.execute_query(query)
        if result is not None and not result.empty:
            return float(result.iloc[0]['total_disbursements'])
        return 0.0
    
    def get_active_schemes_count(self) -> int:
        query = "SELECT COUNT(DISTINCT scheme_id) as active_schemes FROM schemes"
        result = self.execute_query(query)
        if result is not None and not result.empty:
            return int(result.iloc[0]['active_schemes'])
        return 0
    
    def get_total_enrollments(self) -> int:
        query = "SELECT COUNT(*) as total_enrollments FROM enrollments"
        result = self.execute_query(query)
        if result is not None and not result.empty:
            return int(result.iloc[0]['total_enrollments'])
        return 0
    
    def search_citizens(self, search_term=None, district=None):
        """Search citizens by name, Aadhaar, or district"""
        try:
            query = """
            SELECT c.citizen_id, c.aadhaar_no, c.name, c.gender, c.age, 
                   c.mobile_no, c.email, v.name as village_name, d.name as district_name
            FROM citizens c
            JOIN villages v ON c.village_id = v.village_id
            JOIN districts d ON v.district_id = d.district_id
            WHERE 1=1
            """
            params = []
            
            if search_term:
                query += " AND (c.name LIKE ? OR c.aadhaar_no LIKE ?)"
                params.extend([f"%{search_term}%", f"%{search_term}%"])
            
            if district and district != "All":
                query += " AND d.name = ?"
                params.append(district)
                
            query += " ORDER BY c.name"
            
            result = self.execute_query(query, params)
            return result if result is not None else pd.DataFrame()
        except Exception as e:
            logger.error(f"Error searching citizens: {e}")
            return pd.DataFrame()
    
    def get_districts(self):
        """Get all unique districts"""
        try:
            query = "SELECT name FROM districts ORDER BY name"
            result = self.execute_query(query)
            if result is not None and not result.empty:
                return result['name'].tolist()
            return []
        except Exception as e:
            logger.error(f"Error getting districts: {e}")
            return []

@st.cache_resource
def get_database():
    return WelfareDatabase()
