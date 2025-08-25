"""
Query endpoint for natural language to SQL conversion and execution
"""
from fastapi import APIRouter, Query, HTTPException, Header
from fastapi.responses import JSONResponse
from typing import Optional, Dict, Any
from pydantic import BaseModel
import logging

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db import execute_sql, test_db_connection
from backend.prompt_engine import convert_to_sql, get_sample_queries
from backend.auth import verify_token, check_permission

router = APIRouter()
logger = logging.getLogger(__name__)

class QueryRequest(BaseModel):
    """Request model for natural language queries"""
    query: str
    execute: bool = True
    return_chart_suggestion: bool = True

class SqlRequest(BaseModel):
    """Request model for direct SQL execution"""
    sql_query: str

@router.post("/query")
async def process_query(
    request: QueryRequest,
    token: Optional[str] = Header(None, alias="Authorization")
):
    """
    Process natural language query and optionally execute SQL
    Enhanced version with better error handling and response format
    """
    try:
        # Basic authentication check (if token provided)
        if token:
            clean_token = token.replace("Bearer ", "") if token.startswith("Bearer ") else token
            auth_result = verify_token(clean_token)
            if auth_result["status"] != "success":
                raise HTTPException(status_code=401, detail="Invalid authentication token")
            
            # Check read permission
            if not check_permission(clean_token, "read"):
                raise HTTPException(status_code=403, detail="Insufficient permissions")
        
        # Convert natural language to SQL
        sql_result = convert_to_sql(request.query)
        
        if sql_result["status"] != "success":
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "status": "error",
                    "message": sql_result.get("message", "Failed to convert query to SQL"),
                    "original_query": request.query,
                    "suggestions": sql_result.get("suggestions", []),
                    "error_type": "query_conversion_failed"
                }
            )
        
        response_data = {
            "success": True,
            "status": "success",
            "original_query": request.query,
            "sql_query": sql_result["sql_query"],
            "method": sql_result["method"],
            "confidence": sql_result.get("confidence", 0.8),
            "chart_type": sql_result.get("chart_type", "table") if request.return_chart_suggestion else None
        }
        
        # Execute SQL if requested
        if request.execute:
            # Test database connection first
            db_test = test_db_connection()
            if db_test["status"] != "success":
                return JSONResponse(
                    status_code=500,
                    content={
                        "success": False,
                        "status": "error",
                        "message": "Database connection failed",
                        "sql_query": sql_result["sql_query"],
                        "original_query": request.query,
                        "error_type": "database_connection_failed"
                    }
                )
            
            # Execute the SQL query
            execution_result = execute_sql(sql_result["sql_query"])
            
            response_data.update({
                "execution_status": execution_result["status"],
                "data": execution_result.get("data", []),
                "row_count": execution_result.get("row_count", 0),
                "execution_time": execution_result.get("execution_time"),
                "summary": f"Query executed successfully. Retrieved {execution_result.get('row_count', 0)} records."
            })
            
            if execution_result["status"] != "success":
                response_data.update({
                    "success": False,
                    "execution_error": execution_result.get("message", "SQL execution failed"),
                    "error_type": "sql_execution_failed"
                })
        
        return JSONResponse(content=response_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in process_query: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "status": "error",
                "message": f"Internal server error: {str(e)}",
                "original_query": request.query,
                "error_type": "internal_server_error"
            }
        )

@router.get("/query")
async def process_query_get(
    question: str = Query(..., description="Natural language question to convert to SQL"),
    token: Optional[str] = Header(None, alias="Authorization"),
    execute: bool = Query(True, description="Whether to execute the generated SQL")
):
    """
    Process natural language query via GET (backwards compatibility)
    """
    request = QueryRequest(query=question, execute=execute)
    return await process_query(request, token)

@router.get("/query/samples")
async def get_query_samples():
    """
    Get sample queries organized by category
    """
    try:
        samples = get_sample_queries()
        return JSONResponse(content={
            "success": True,
            "status": "success",
            "samples": samples,
            "message": "Sample queries retrieved successfully"
        })
    except Exception as e:
        logger.error(f"Error getting sample queries: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "status": "error",
                "message": f"Failed to get sample queries: {str(e)}"
            }
        )

@router.post("/query/execute")
async def execute_custom_sql(
    request: SqlRequest,
    token: Optional[str] = Header(None, alias="Authorization")
):
    """
    Execute custom SQL query directly (for advanced users)
    Enhanced with better security and validation
    """
    try:
        # Authentication check (required for custom SQL)
        if not token:
            raise HTTPException(status_code=401, detail="Authentication required for custom SQL execution")
        
        clean_token = token.replace("Bearer ", "") if token.startswith("Bearer ") else token
        auth_result = verify_token(clean_token)
        if auth_result["status"] != "success":
            raise HTTPException(status_code=401, detail="Invalid authentication token")
        
        # Check write permission for custom SQL execution
        if not check_permission(clean_token, "write"):
            raise HTTPException(status_code=403, detail="Insufficient permissions for custom SQL execution")
        
        sql_query = request.sql_query.strip()
        if not sql_query:
            raise HTTPException(status_code=400, detail="SQL query is required")
        
        # Enhanced SQL injection protection
        dangerous_patterns = [
            r'\bDROP\s+TABLE\b',
            r'\bDELETE\s+FROM\b',
            r'\bTRUNCATE\s+TABLE\b',
            r'\bALTER\s+TABLE\b',
            r'\bCREATE\s+TABLE\b',
            r'\bINSERT\s+INTO\b',
            r'\bUPDATE\s+\w+\s+SET\b',
            r'\bEXEC\b',
            r'\bEXECUTE\b',
            r';.*?(\bDROP\b|\bDELETE\b|\bTRUNCATE\b)'
        ]
        
        import re
        sql_upper = sql_query.upper()
        
        for pattern in dangerous_patterns:
            if re.search(pattern, sql_upper, re.IGNORECASE):
                raise HTTPException(
                    status_code=400, 
                    detail=f"SQL query contains potentially dangerous operations"
                )
        
        # Limit to SELECT statements for safety
        if not sql_upper.strip().startswith('SELECT'):
            raise HTTPException(
                status_code=400,
                detail="Only SELECT statements are allowed for custom SQL execution"
            )
        
        # Execute the SQL query
        result = execute_sql(sql_query)
        
        return JSONResponse(content={
            "success": result["status"] == "success",
            "status": result["status"],
            "sql_query": sql_query,
            "data": result.get("data", []),
            "row_count": result.get("row_count", 0),
            "message": result.get("message", ""),
            "execution_type": "custom_sql",
            "execution_time": result.get("execution_time")
        })
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error executing custom SQL: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "status": "error",
                "message": f"Failed to execute custom SQL: {str(e)}"
            }
        )
