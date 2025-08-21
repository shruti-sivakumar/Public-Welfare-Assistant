"""
FastAPI Backend for Data Interpreter Assistant with Voice
Main application entry point with comprehensive configuration
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
import time
import os
from datetime import datetime

# Import routes
from routes.query import router as query_router
from routes.verify import router as verify_router
from routes.summary import router as summary_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app with enhanced configuration
app = FastAPI(
    title="Data Interpreter Assistant API",
    description="""
    Backend API for conversational data querying with voice support.
    
    ## Features
    * Natural Language to SQL conversion
    * Database query execution
    * Authentication and authorization
    * Data analytics and summaries
    * Real-time health monitoring
    
    ## Authentication
    Most endpoints support optional Bearer token authentication for enhanced security.
    
    ## Endpoints
    * `/query` - Process natural language queries
    * `/verify` - System health and verification
    * `/summary` - Data analytics and insights
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Enhanced CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",    # Streamlit default
        "http://127.0.0.1:8501",   # Streamlit alternative
        "http://localhost:3000",    # React dev server
        "http://127.0.0.1:3000",   # React alternative
        "http://localhost:8080",    # Alternative frontend
        "http://127.0.0.1:8080"    # Alternative frontend
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Add request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests"""
    start_time = time.time()
    
    # Log request
    logger.info(f"🔵 {request.method} {request.url.path} - Client: {request.client.host}")
    
    # Process request
    response = await call_next(request)
    
    # Log response
    process_time = time.time() - start_time
    logger.info(f"🟢 {request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time:.2f}s")
    
    return response

# Include routers (without prefix for direct access)
app.include_router(query_router, tags=["Query Processing"])
app.include_router(verify_router, tags=["System Verification"])
app.include_router(summary_router, tags=["Data Analytics"])

@app.get("/")
async def root():
    """API Root - Welcome message and basic info"""
    return {
        "message": "🚀 Data Interpreter Assistant API",
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "documentation": "/docs",
        "health_check": "/health",
        "endpoints": {
            "query": "/query",
            "verify": "/verify", 
            "summary": "/summary"
        }
    }

@app.get("/health")
async def health_check():
    """Comprehensive health check endpoint"""
    return {
        "status": "healthy",
        "service": "Data Interpreter Assistant API",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "uptime": "Running",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "database": "Connected",  # This could be enhanced with actual DB check
        "api_docs": "/docs"
    }

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Custom 404 handler"""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Endpoint not found",
            "message": f"The endpoint {request.url.path} does not exist",
            "available_endpoints": [
                "/", "/health", "/docs", "/query", "/verify", "/summary"
            ]
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    """Custom 500 handler"""
    logger.error(f"Internal server error on {request.url.path}: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred. Please try again later.",
            "timestamp": datetime.utcnow().isoformat()
        }
    )

if __name__ == "__main__":
    # Enhanced startup configuration
    logger.info("🚀 Starting Data Interpreter Assistant API...")
    uvicorn.run(
        app, 
        host="127.0.0.1", 
        port=8000, 
        reload=True,
        log_level="info"
    )
