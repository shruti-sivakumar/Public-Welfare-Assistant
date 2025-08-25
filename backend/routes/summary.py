"""
Summary endpoint for data insights and analytics
"""
from fastapi import APIRouter, HTTPException, Header, Query
from fastapi.responses import JSONResponse
from typing import Optional, Dict, Any
import logging

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db import execute_sql, get_db_connection
from backend.auth import verify_token, check_permission

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/summary")
async def get_data_summary(
    token: Optional[str] = Header(None, alias="Authorization"),
    table: Optional[str] = Query(None, description="Specific table to summarize")
):
    """
    Get summary statistics and insights from the database
    """
    try:
        # Basic authentication check
        if token:
            auth_result = verify_token(token.replace("Bearer ", "") if token.startswith("Bearer ") else token)
            if auth_result["status"] != "success":
                raise HTTPException(status_code=401, detail="Invalid authentication token")
            
            # Check read permission
            if not check_permission(token.replace("Bearer ", "") if token.startswith("Bearer ") else token, "read"):
                raise HTTPException(status_code=403, detail="Insufficient permissions")
        
        summary_data = {}
        
        if table:
            # Get summary for specific table
            summary_data = await _get_table_summary(table)
        else:
            # Get overall database summary
            summary_data = await _get_overall_summary()
        
        return JSONResponse(content={
            "status": "success",
            "summary": summary_data,
            "message": f"Summary generated successfully{' for table: ' + table if table else ''}"
        })
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating summary: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": f"Failed to generate summary: {str(e)}"
            }
        )

async def _get_overall_summary() -> Dict[str, Any]:
    """Get overall database summary"""
    try:
        summary = {
            "tables": {},
            "total_records": 0,
            "database_info": {}
        }
        
        # Get table counts
        table_queries = [
            ("citizens", "SELECT COUNT(*) as count FROM citizens"),
            ("officers", "SELECT COUNT(*) as count FROM officers"), 
            ("schemes", "SELECT COUNT(*) as count FROM schemes")
        ]
        
        for table_name, query in table_queries:
            try:
                result = execute_sql(query)
                if result["status"] == "success" and result["data"]:
                    count = result["data"][0]["count"]
                    summary["tables"][table_name] = {
                        "record_count": count,
                        "status": "accessible"
                    }
                    summary["total_records"] += count
                else:
                    summary["tables"][table_name] = {
                        "record_count": 0,
                        "status": "error",
                        "message": result.get("message", "Unknown error")
                    }
            except Exception as e:
                summary["tables"][table_name] = {
                    "record_count": 0,
                    "status": "error", 
                    "message": str(e)
                }
        
        # Get database metadata
        try:
            db_manager = get_db_connection()
            tables_result = db_manager.list_tables()
            if tables_result["status"] == "success":
                summary["database_info"]["total_tables"] = len(tables_result["data"])
                summary["database_info"]["table_names"] = [t["TABLE_NAME"] for t in tables_result["data"]]
        except Exception as e:
            logger.error(f"Error getting database metadata: {e}")
        
        return summary
        
    except Exception as e:
        logger.error(f"Error in _get_overall_summary: {e}")
        return {"error": str(e)}

async def _get_table_summary(table_name: str) -> Dict[str, Any]:
    """Get summary for specific table"""
    try:
        summary = {
            "table_name": table_name,
            "record_count": 0,
            "schema": {},
            "sample_data": []
        }
        
        # Get record count
        count_query = f"SELECT COUNT(*) as count FROM {table_name}"
        count_result = execute_sql(count_query)
        
        if count_result["status"] == "success" and count_result["data"]:
            summary["record_count"] = count_result["data"][0]["count"]
        
        # Get table schema
        try:
            db_manager = get_db_connection()
            schema_result = db_manager.get_table_schema(table_name)
            if schema_result["status"] == "success":
                summary["schema"] = schema_result["data"]
        except Exception as e:
            logger.error(f"Error getting schema for {table_name}: {e}")
        
        # Get sample data (first 5 records)
        sample_query = f"SELECT TOP 5 * FROM {table_name}"
        sample_result = execute_sql(sample_query)
        
        if sample_result["status"] == "success":
            summary["sample_data"] = sample_result["data"]
        
        return summary
        
    except Exception as e:
        logger.error(f"Error in _get_table_summary for {table_name}: {e}")
        return {"error": str(e), "table_name": table_name}

@router.get("/summary/analytics")
async def get_analytics_summary(
    token: Optional[str] = Header(None, alias="Authorization")
):
    """
    Get advanced analytics and insights
    """
    try:
        # Authentication check
        if token:
            auth_result = verify_token(token.replace("Bearer ", "") if token.startswith("Bearer ") else token)
            if auth_result["status"] != "success":
                raise HTTPException(status_code=401, detail="Invalid authentication token")
            
            # Check read permission
            if not check_permission(token.replace("Bearer ", "") if token.startswith("Bearer ") else token, "read"):
                raise HTTPException(status_code=403, detail="Insufficient permissions")
        
        analytics = await _get_analytics_data()
        
        return JSONResponse(content={
            "status": "success",
            "analytics": analytics,
            "message": "Analytics summary generated successfully"
        })
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating analytics: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": f"Failed to generate analytics: {str(e)}"
            }
        )

async def _get_analytics_data() -> Dict[str, Any]:
    """Generate analytics insights"""
    try:
        analytics = {
            "demographic_insights": {},
            "distribution_analysis": {},
            "trends": {}
        }
        
        # Citizens age distribution
        try:
            age_query = """
                SELECT 
                    CASE 
                        WHEN age < 18 THEN 'Under 18'
                        WHEN age BETWEEN 18 AND 30 THEN '18-30'
                        WHEN age BETWEEN 31 AND 50 THEN '31-50'
                        WHEN age BETWEEN 51 AND 65 THEN '51-65'
                        ELSE 'Over 65'
                    END as age_group,
                    COUNT(*) as count
                FROM citizens 
                GROUP BY 
                    CASE 
                        WHEN age < 18 THEN 'Under 18'
                        WHEN age BETWEEN 18 AND 30 THEN '18-30'
                        WHEN age BETWEEN 31 AND 50 THEN '31-50'
                        WHEN age BETWEEN 51 AND 65 THEN '51-65'
                        ELSE 'Over 65'
                    END
                ORDER BY count DESC
            """
            
            age_result = execute_sql(age_query)
            if age_result["status"] == "success":
                analytics["demographic_insights"]["age_distribution"] = age_result["data"]
        except Exception as e:
            logger.error(f"Error getting age distribution: {e}")
        
        # Gender distribution
        try:
            gender_query = "SELECT gender, COUNT(*) as count FROM citizens GROUP BY gender"
            gender_result = execute_sql(gender_query)
            if gender_result["status"] == "success":
                analytics["demographic_insights"]["gender_distribution"] = gender_result["data"]
        except Exception as e:
            logger.error(f"Error getting gender distribution: {e}")
        
        return analytics
        
    except Exception as e:
        logger.error(f"Error in _get_analytics_data: {e}")
        return {"error": str(e)}
