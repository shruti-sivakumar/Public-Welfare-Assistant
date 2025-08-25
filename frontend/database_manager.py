import pyodbc
import logging
import os

class DatabaseManager:
    def __init__(self, db_path=None):
        # Use environment variables for Azure SQL connection (best practice)
        self.server = os.getenv("AZURE_SQL_SERVER")    # e.g., yourserver.database.windows.net
        self.database = os.getenv("AZURE_SQL_DATABASE")
        self.username = os.getenv("AZURE_SQL_USER")
        self.password = os.getenv("AZURE_SQL_PASSWORD")
        self.driver = os.getenv("AZURE_SQL_DRIVER", "{ODBC Driver 17 for SQL Server}")
        self.connection_string = (
            f"DRIVER={self.driver};"
            f"SERVER={self.server};"
            f"DATABASE={self.database};"
            f"UID={self.username};"
            f"PWD={self.password}"
        )

    def execute_query(self, query, params=None):
        conn = None
        try:
            conn = pyodbc.connect(self.connection_string)
            cursor = conn.cursor()
            logging.info(f"Executing SQL: {query} | params: {params}")
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # SELECT queries
            if query.strip().lower().startswith("select"):
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                result = [dict(zip(columns, row)) for row in rows]
                return result
            else:
                conn.commit()
                return {"rows_affected": cursor.rowcount}
        except Exception as e:
            logging.error(f"DB error: {e}")
            raise
        finally:
            if conn:
                conn.close()
