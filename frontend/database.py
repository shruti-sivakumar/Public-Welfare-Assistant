import pyodbc
import pandas as pd
import streamlit as st
from typing import Optional, Dict, Any, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WelfareDatabase:
    def __init__(self):
        self.connection_string = None
        self.connection = None
    
    def configure_connection(self, server: str, database: str, username: str = None, password: str = None, trusted_connection: bool = True):
        """Configure database connection parameters"""
        if trusted_connection:
            self.connection_string = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;"
        else:
            self.connection_string = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};"
    
    def connect(self) -> bool:
        """Establish database connection"""
        try:
            if not self.connection_string:
                st.error("Database connection not configured. Please set connection parameters.")
                return False
            
            self.connection = pyodbc.connect(self.connection_string)
            logger.info("Database connection established successfully")
            return True
        except Exception as e:
            logger.error(f"Database connection failed: {str(e)}")
            st.error(f"Database connection failed: {str(e)}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
            logger.info("Database connection closed")
    
    def execute_query(self, query: str, params: tuple = None) -> Optional[pd.DataFrame]:
        """Execute SQL query and return results as DataFrame"""
        try:
            if not self.connection:
                if not self.connect():
                    return None
            
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # Get column names
            columns = [column[0] for column in cursor.description] if cursor.description else []
            
            # Fetch all results
            rows = cursor.fetchall()
            
            # Convert to DataFrame
            if rows:
                df = pd.DataFrame.from_records(rows, columns=columns)
                logger.info(f"Query executed successfully, returned {len(df)} rows")
                return df
            else:
                logger.info("Query executed successfully, no rows returned")
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"Query execution failed: {str(e)}")
            st.error(f"Query execution failed: {str(e)}")
            return None
    
    def get_schemes(self) -> pd.DataFrame:
        """Get all welfare schemes"""
        query = """
        SELECT 
            s.scheme_id,
            s.name,
            s.sector,
            s.description,
            COUNT(e.enrollment_id) as total_enrollments,
            COALESCE(SUM(d.amount), 0) as total_disbursements
        FROM schemes s
        LEFT JOIN enrollments e ON s.scheme_id = e.scheme_id
        LEFT JOIN disbursements d ON s.scheme_id = d.scheme_id
        GROUP BY s.scheme_id, s.name, s.sector, s.description
        ORDER BY s.scheme_id
        """
        return self.execute_query(query)
    
    def get_citizens_count(self, district: str = None) -> int:
        """Get total count of citizens"""
        if district:
            query = """
            SELECT COUNT(*) as count 
            FROM citizens c
            JOIN villages v ON c.village_id = v.village_id
            JOIN districts d ON v.district_id = d.district_id
            WHERE d.name = ?
            """
            result = self.execute_query(query, (district,))
        else:
            query = "SELECT COUNT(*) as count FROM citizens"
            result = self.execute_query(query)
        
        return result['count'].iloc[0] if result is not None and not result.empty else 0
    
    def get_disbursements_summary(self, scheme_name: str = None) -> pd.DataFrame:
        """Get disbursements summary by scheme"""
        if scheme_name:
            query = """
            SELECT 
                s.name as scheme_name,
                COUNT(d.disbursement_id) as total_disbursements,
                SUM(d.amount) as total_amount,
                AVG(d.amount) as avg_amount
            FROM schemes s
            JOIN disbursements d ON s.scheme_id = d.scheme_id
            WHERE s.name = ?
            GROUP BY s.scheme_id, s.name
            """
            return self.execute_query(query, (scheme_name,))
        else:
            query = """
            SELECT 
                s.name as scheme_name,
                COUNT(d.disbursement_id) as total_disbursements,
                SUM(d.amount) as total_amount,
                AVG(d.amount) as avg_amount
            FROM schemes s
            LEFT JOIN disbursements d ON s.scheme_id = d.scheme_id
            GROUP BY s.scheme_id, s.name
            ORDER BY total_amount DESC
            """
            return self.execute_query(query)
    
    def get_enrollments_by_scheme(self) -> pd.DataFrame:
        """Get enrollment counts by scheme"""
        query = """
        SELECT 
            s.name as scheme_name,
            COUNT(e.enrollment_id) as enrollments,
            COUNT(CASE WHEN e.status = 'Active' THEN 1 END) as active_enrollments
        FROM schemes s
        LEFT JOIN enrollments e ON s.scheme_id = e.scheme_id
        GROUP BY s.scheme_id, s.name
        ORDER BY enrollments DESC
        """
        return self.execute_query(query)
    
    def search_citizens(self, search_term: str, district: str = None) -> pd.DataFrame:
        """Search citizens by name or Aadhaar"""
        base_query = """
        SELECT 
            c.citizen_id,
            c.name,
            c.aadhaar_no,
            c.gender,
            c.age,
            c.mobile_no,
            c.email,
            v.name as village_name,
            d.name as district_name,
            st.name as state_name
        FROM citizens c
        JOIN villages v ON c.village_id = v.village_id
        JOIN districts d ON v.district_id = d.district_id
        JOIN states st ON d.state_id = st.state_id
        WHERE (c.name LIKE ? OR c.aadhaar_no LIKE ?)
        """
        
        if district:
            base_query += " AND d.name = ?"
            params = (f"%{search_term}%", f"%{search_term}%", district)
        else:
            params = (f"%{search_term}%", f"%{search_term}%")
        
        base_query += " ORDER BY c.name LIMIT 100"
        return self.execute_query(base_query, params)
    
    def get_districts(self) -> List[str]:
        """Get all districts"""
        query = "SELECT DISTINCT name FROM districts ORDER BY name"
        result = self.execute_query(query)
        return result['name'].tolist() if result is not None and not result.empty else []
    
    def get_states(self) -> List[str]:
        """Get all states"""
        query = "SELECT DISTINCT name FROM states ORDER BY name"
        result = self.execute_query(query)
        return result['name'].tolist() if result is not None and not result.empty else []
    

# Global database instance
@st.cache_resource
def get_database():
    return WelfareDatabase()
