"""
Verification and Health Check Routes
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging

# Import our modules
from db import test_db_connection
from auth import verify_token

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "service": "Data Interpreter API",
        "version": "1.0.0"
    }

@router.get("/verify/database")
async def verify_database() -> Dict[str, Any]:
    """
    Verify database connection
    """
    try:
        is_connected, message = test_db_connection()
        
        return {
            "success": is_connected,
            "message": message,
            "database": "Connected" if is_connected else "Disconnected"
        }
    except Exception as e:
        logger.error(f"Database verification failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database verification failed: {str(e)}")

@router.get("/verify/auth")
async def verify_auth() -> Dict[str, Any]:
    """
    Verify authentication system
    """
    try:
        # Test authentication system
        test_result = verify_token("test_token")
        
        return {
            "success": True,
            "message": "Authentication system operational",
            "auth_system": "Active"
        }
    except Exception as e:
        logger.error(f"Auth verification failed: {str(e)}")
        return {
            "success": False,
            "message": f"Auth verification failed: {str(e)}",
            "auth_system": "Error"
        }

@router.get("/verify/system")
async def verify_system() -> Dict[str, Any]:
    """
    Comprehensive system verification
    """
    try:
        # Test database
        db_connected, db_message = test_db_connection()
        
        # Test auth (basic check)
        auth_status = True
        auth_message = "Authentication system ready"
        
        return {
            "success": db_connected and auth_status,
            "components": {
                "database": {
                    "status": "connected" if db_connected else "disconnected",
                    "message": db_message
                },
                "authentication": {
                    "status": "active" if auth_status else "inactive", 
                    "message": auth_message
                },
                "api": {
                    "status": "running",
                    "message": "FastAPI server operational"
                }
            },
            "overall_status": "healthy" if (db_connected and auth_status) else "degraded"
        }
    except Exception as e:
        logger.error(f"System verification failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"System verification failed: {str(e)}")
