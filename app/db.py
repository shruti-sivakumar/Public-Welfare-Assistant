"""
Database connection and query execution module for Azure SQL Database
Enhanced version with local SQLite fallback and better error handling
"""
import os
import pyodbc
import pandas as pd
from typing import Dict, List, Any, Optional
from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# SQLAlchemy Base for models
Base = declarative_base()

class DatabaseManager:
    """Enhanced Database Manager with Azure SQL and SQLite support"""
    
    def __init__(self):
        self.use_local_db = os.getenv('USE_LOCAL_DB', 'true').lower() == 'true'
        self.connection_string = self._build_connection_string()
        self.engine = None
        self.metadata = MetaData()
        self._initialize_engine()
        self._create_tables_if_not_exist()
    
    def _build_connection_string(self) -> str:
        """Build connection string based on configuration"""
        if self.use_local_db:
            # Use SQLite for local development
            sqlite_path = os.getenv('LOCAL_DB_CONNECTION_STRING', 'sqlite:///./data_interpreter.db')
            logger.info(f"Using local SQLite database: {sqlite_path}")
            return sqlite_path
        else:
            # Use Azure SQL for production
            server = os.getenv('AZURE_SQL_SERVER')
            database = os.getenv('AZURE_SQL_DATABASE')
            username = os.getenv('AZURE_SQL_USERNAME')
            password = os.getenv('AZURE_SQL_PASSWORD')
            driver = os.getenv('AZURE_SQL_DRIVER', 'ODBC Driver 17 for SQL Server')
            
            if not all([server, database, username, password]):
                logger.warning("Azure SQL credentials not complete, falling back to SQLite")
                self.use_local_db = True
                return os.getenv('LOCAL_DB_CONNECTION_STRING', 'sqlite:///./data_interpreter.db')
            
            # For SQLAlchemy with Azure SQL
            connection_string = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver.replace(' ', '+')}"
            logger.info(f"Using Azure SQL database: {server}/{database}")
            return connection_string
    
    def _initialize_engine(self):
        """Initialize SQLAlchemy engine with proper configuration"""
        try:
            if self.use_local_db:
                # SQLite configuration
                self.engine = create_engine(
                    self.connection_string,
                    echo=os.getenv('DB_ECHO', 'false').lower() == 'true',
                    connect_args={"check_same_thread": False}  # For SQLite threading
                )
            else:
                # Azure SQL configuration
                self.engine = create_engine(
                    self.connection_string,
                    echo=os.getenv('DB_ECHO', 'false').lower() == 'true',
                    pool_size=int(os.getenv('DB_POOL_SIZE', '10')),
                    max_overflow=int(os.getenv('DB_MAX_OVERFLOW', '20'))
                )
            
            logger.info("Database engine initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database engine: {e}")
            self.engine = None
    
    def _create_tables_if_not_exist(self):
        """Create sample tables for testing if they don't exist"""
        if not self.engine:
            return
        
        try:
            with self.engine.connect() as conn:
                # Create Citizens table
                citizens_table = """
                CREATE TABLE IF NOT EXISTS citizens (
                    citizen_id INTEGER PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    age INTEGER,
                    gender VARCHAR(10),
                    address TEXT,
                    phone VARCHAR(20),
                    email VARCHAR(100),
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
                """
                
                # Create Officers table
                officers_table = """
                CREATE TABLE IF NOT EXISTS officers (
                    officer_id INTEGER PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    department VARCHAR(100),
                    rank VARCHAR(50),
                    phone VARCHAR(20),
                    email VARCHAR(100),
                    is_active BOOLEAN DEFAULT 1,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
                """
                
                # Create Schemes table
                schemes_table = """
                CREATE TABLE IF NOT EXISTS schemes (
                    scheme_id INTEGER PRIMARY KEY,
                    scheme_name VARCHAR(200) NOT NULL,
                    description TEXT,
                    eligibility TEXT,
                    benefits TEXT,
                    is_active BOOLEAN DEFAULT 1,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
                """
                
                # Execute table creation
                conn.execute(text(citizens_table))
                conn.execute(text(officers_table))
                conn.execute(text(schemes_table))
                conn.commit()
                
                # Insert sample data if tables are empty
                self._insert_sample_data_if_needed(conn)
                
                logger.info("Database tables created/verified successfully")
        except Exception as e:
            logger.error(f"Error creating tables: {e}")
    
    def _insert_sample_data_if_needed(self, conn):
        """Insert sample data if tables are empty"""
        try:
            # Check if citizens table has data
            result = conn.execute(text("SELECT COUNT(*) as count FROM citizens"))
            count = result.fetchone()[0]
            
            if count == 0:
                # Insert sample citizens
                sample_citizens = [
                    (1, 'Alice Johnson', 28, 'Female', '123 Main St', '555-0001', 'alice@email.com'),
                    (2, 'Bob Smith', 34, 'Male', '456 Oak Ave', '555-0002', 'bob@email.com'),
                    (3, 'Carol Davis', 45, 'Female', '789 Pine Rd', '555-0003', 'carol@email.com'),
                    (4, 'David Wilson', 29, 'Male', '321 Elm St', '555-0004', 'david@email.com'),
                    (5, 'Eva Brown', 52, 'Female', '654 Maple Dr', '555-0005', 'eva@email.com')
                ]
                
                for citizen in sample_citizens:
                    conn.execute(text(
                        "INSERT INTO citizens (citizen_id, name, age, gender, address, phone, email) "
                        "VALUES (:id, :name, :age, :gender, :address, :phone, :email)"
                    ), {
                        'id': citizen[0], 'name': citizen[1], 'age': citizen[2],
                        'gender': citizen[3], 'address': citizen[4], 'phone': citizen[5], 'email': citizen[6]
                    })
                
                # Insert sample officers
                sample_officers = [
                    (1, 'Officer Martinez', 'Police', 'Sergeant', '555-1001', 'martinez@police.gov'),
                    (2, 'Officer Thompson', 'Fire Department', 'Lieutenant', '555-1002', 'thompson@fire.gov'),
                    (3, 'Officer Anderson', 'Police', 'Detective', '555-1003', 'anderson@police.gov')
                ]
                
                for officer in sample_officers:
                    conn.execute(text(
                        "INSERT INTO officers (officer_id, name, department, rank, phone, email) "
                        "VALUES (:id, :name, :dept, :rank, :phone, :email)"
                    ), {
                        'id': officer[0], 'name': officer[1], 'dept': officer[2],
                        'rank': officer[3], 'phone': officer[4], 'email': officer[5]
                    })
                
                # Insert sample schemes
                sample_schemes = [
                    (1, 'Senior Citizen Benefits', 'Benefits for senior citizens', 'Age >= 60', 'Healthcare, Pension'),
                    (2, 'Student Scholarship', 'Education support for students', 'Student with good grades', 'Tuition fees, Books'),
                    (3, 'Housing Assistance', 'Housing support for low income families', 'Income < $30,000', 'Rent subsidy, Housing loans')
                ]
                
                for scheme in sample_schemes:
                    conn.execute(text(
                        "INSERT INTO schemes (scheme_id, scheme_name, description, eligibility, benefits) "
                        "VALUES (:id, :name, :desc, :eligibility, :benefits)"
                    ), {
                        'id': scheme[0], 'name': scheme[1], 'desc': scheme[2],
                        'eligibility': scheme[3], 'benefits': scheme[4]
                    })
                
                conn.commit()
                logger.info("Sample data inserted successfully")
        except Exception as e:
            logger.error(f"Error inserting sample data: {e}")
    
    def test_connection(self) -> Dict[str, Any]:
        """Test database connection and return status"""
        try:
            if not self.engine:
                return {"status": "error", "message": "Database engine not initialized"}
            
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT 1 as test"))
                row = result.fetchone()
                
            # Get database info
            db_type = "SQLite" if self.use_local_db else "Azure SQL"
            
            return {
                "status": "success",
                "message": f"Database connection successful ({db_type})",
                "database_type": db_type,
                "test_query_result": row[0] if row else None,
                "engine_info": str(self.engine.url).split('@')[0] + '@***'  # Hide credentials
            }
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return {
                "status": "error",
                "message": f"Database connection failed: {str(e)}",
                "database_type": "SQLite" if self.use_local_db else "Azure SQL"
            }
    
    def execute_query(self, query: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Execute SQL query and return results with enhanced error handling"""
        try:
            if not self.engine:
                return {
                    "status": "error",
                    "message": "Database engine not initialized",
                    "data": []
                }
            
            with self.engine.connect() as conn:
                # Prepare parameters
                query_params = params or {}
                
                # Execute query
                result = conn.execute(text(query), query_params)
                
                # Handle different query types
                query_upper = query.strip().upper()
                if query_upper.startswith('SELECT'):
                    # SELECT queries
                    columns = result.keys()
                    rows = result.fetchall()
                    data = [dict(zip(columns, row)) for row in rows]
                    
                    return {
                        "status": "success",
                        "message": f"Query executed successfully. {len(data)} rows returned.",
                        "data": data,
                        "row_count": len(data),
                        "columns": list(columns)
                    }
                else:
                    # INSERT, UPDATE, DELETE queries
                    conn.commit()
                    affected_rows = result.rowcount if hasattr(result, 'rowcount') else 0
                    
                    return {
                        "status": "success",
                        "message": f"Query executed successfully. {affected_rows} rows affected.",
                        "data": [],
                        "rows_affected": affected_rows
                    }
                    
        except SQLAlchemyError as e:
            logger.error(f"SQL query execution failed: {e}")
            return {
                "status": "error",
                "message": f"SQL execution error: {str(e)}",
                "data": [],
                "error_type": "SQLAlchemyError"
            }
        except Exception as e:
            logger.error(f"Unexpected error during query execution: {e}")
            return {
                "status": "error",
                "message": f"Unexpected error: {str(e)}",
                "data": [],
                "error_type": "UnexpectedError"
            }
    
    def execute_query_pandas(self, query: str, params: Optional[Dict] = None) -> pd.DataFrame:
        """Execute query and return results as pandas DataFrame"""
        try:
            if not self.engine:
                logger.error("Database engine not initialized")
                return pd.DataFrame()
            
            df = pd.read_sql_query(text(query), self.engine, params=params or {})
            logger.info(f"Query executed successfully. DataFrame shape: {df.shape}")
            return df
            
        except Exception as e:
            logger.error(f"Failed to execute query with pandas: {e}")
            return pd.DataFrame()
    
    def get_table_schema(self, table_name: str) -> Dict[str, Any]:
        """Get schema information for a specific table"""
        try:
            if self.use_local_db:
                # SQLite schema query
                schema_query = f"PRAGMA table_info({table_name})"
                result = self.execute_query(schema_query)
                
                if result["status"] == "success":
                    # Convert SQLite schema to standard format
                    schema_data = []
                    for col in result["data"]:
                        schema_data.append({
                            "COLUMN_NAME": col["name"],
                            "DATA_TYPE": col["type"],
                            "IS_NULLABLE": "YES" if col["notnull"] == 0 else "NO",
                            "COLUMN_DEFAULT": col["dflt_value"]
                        })
                    
                    return {
                        "status": "success",
                        "data": schema_data,
                        "table_name": table_name
                    }
            else:
                # Azure SQL schema query
                schema_query = """
                SELECT 
                    COLUMN_NAME,
                    DATA_TYPE,
                    IS_NULLABLE,
                    COLUMN_DEFAULT,
                    CHARACTER_MAXIMUM_LENGTH
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = :table_name
                ORDER BY ORDINAL_POSITION
                """
                
                return self.execute_query(schema_query, {"table_name": table_name})
        except Exception as e:
            logger.error(f"Error getting table schema: {e}")
            return {
                "status": "error",
                "message": f"Failed to get schema for table {table_name}: {str(e)}"
            }
    
    def list_tables(self) -> Dict[str, Any]:
        """List all tables in the database"""
        try:
            if self.use_local_db:
                # SQLite tables query
                tables_query = "SELECT name as TABLE_NAME, 'BASE TABLE' as TABLE_TYPE FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
            else:
                # Azure SQL tables query
                tables_query = """
                SELECT TABLE_NAME, TABLE_TYPE 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_TYPE = 'BASE TABLE'
                ORDER BY TABLE_NAME
                """
            
            return self.execute_query(tables_query)
        except Exception as e:
            logger.error(f"Error listing tables: {e}")
            return {
                "status": "error",
                "message": f"Failed to list tables: {str(e)}"
            }
    
    def get_database_info(self) -> Dict[str, Any]:
        """Get comprehensive database information"""
        try:
            info = {
                "database_type": "SQLite" if self.use_local_db else "Azure SQL",
                "connection_status": "connected" if self.engine else "disconnected",
                "tables": [],
                "total_tables": 0
            }
            
            # Get tables
            tables_result = self.list_tables()
            if tables_result["status"] == "success":
                info["tables"] = tables_result["data"]
                info["total_tables"] = len(tables_result["data"])
            
            # Get record counts for main tables
            main_tables = ["citizens", "officers", "schemes"]
            record_counts = {}
            
            for table in main_tables:
                try:
                    count_result = self.execute_query(f"SELECT COUNT(*) as count FROM {table}")
                    if count_result["status"] == "success" and count_result["data"]:
                        record_counts[table] = count_result["data"][0]["count"]
                except:
                    record_counts[table] = "Error"
            
            info["record_counts"] = record_counts
            
            return {
                "status": "success",
                "data": info
            }
        except Exception as e:
            logger.error(f"Error getting database info: {e}")
            return {
                "status": "error",
                "message": f"Failed to get database info: {str(e)}"
            }

# Global database manager instance
db_manager = DatabaseManager()

# Convenience functions for backward compatibility
def get_db_connection():
    """Get database manager instance"""
    return db_manager

def execute_sql(query: str, params: Optional[Dict] = None):
    """Execute SQL query using global database manager"""
    return db_manager.execute_query(query, params)

def test_db_connection():
    """Test database connection using global database manager"""
    return db_manager.test_connection()

def get_database_info():
    """Get comprehensive database information"""
    return db_manager.get_database_info()
