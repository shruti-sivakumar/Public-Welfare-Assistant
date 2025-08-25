
import openai
from openai import AzureOpenAI
"""
FastAPI Backend for Data Interpreter Assistant with Voice
Main application entry point with comprehensive configuration
"""
from fastapi import FastAPI, Request, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import traceback
import uvicorn
import logging
import time
import os
from datetime import datetime
import azure.cognitiveservices.speech as speechsdk
from backend.db import execute_sql
from dotenv import load_dotenv
load_dotenv()

# Instantiate AzureOpenAI client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)


# Import routes
from backend.routes.query import router as query_router
from backend.routes.verify import router as verify_router
from backend.routes.summary import router as summary_router

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
@app.api_route("/test-openai", methods=["GET", "POST"])
async def test_openai():
    try:
        prompt = "Say hello from Azure OpenAI."
        response = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            messages=[{"role": "user", "content": prompt}]
        )
        message = response.choices[0].message.content
        return {"result": message}
    except Exception as e:
        import traceback; traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})
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


# Test OpenAI endpoint
@app.post("/test-openai")
async def test_openai():
    try:
        prompt = "Say hello from Azure OpenAI."
        response = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            messages=[{"role": "user", "content": prompt}]
        )
        message = response.choices[0].message.content
        return {"result": message}
    except Exception as e:
        import traceback; traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})

# Speech-to-text endpoint using Azure Speech SDK
@app.post("/speech-to-text")
async def speech_to_text(file: UploadFile = File(...)):
    temp_path = None
    try:
        # Save uploaded file to disk
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(await file.read())

        # Configure Azure Speech
        speech_key = os.getenv("AZURE_SPEECH_KEY")
        speech_region = os.getenv("AZURE_SPEECH_REGION")
        if not speech_key or not speech_region:
            return JSONResponse(status_code=500, content={"error": "Azure Speech credentials not set in .env"})

        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
        audio_config = speechsdk.audio.AudioConfig(filename=temp_path)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
        result = speech_recognizer.recognize_once()

        # Explicitly delete recognizer and audio_config to release file handle
        del speech_recognizer
        del audio_config

        # Remove temp file safely
        import time
        for _ in range(5):
            try:
                os.remove(temp_path)
                break
            except PermissionError:
                time.sleep(0.2)

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            return {"text": result.text}
        else:
            return JSONResponse(status_code=400, content={"error": "Speech not recognized", "details": str(result.reason)})
    except Exception as e:
        import traceback
        traceback.print_exc()
        # Try to remove temp file if possible
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass
        return JSONResponse(status_code=500, content={"error": str(e)})

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
@app.post("/nl2sql")
async def nl2sql(request: Request):
    try:
        load_dotenv()
        openai.api_type = "azure"
        openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
        openai.api_key = os.getenv("AZURE_OPENAI_KEY")
        openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")

        data = await request.json()
        nl_query = data.get("query")
        prompt = f"Convert this to an SQL query: {nl_query}"

        response = openai.ChatCompletion.create(
            engine=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            messages=[{"role": "user", "content": prompt}]
        )
        sql_query = response.choices[0].message["content"]

        result = execute_sql(sql_query)

        import pandas as pd
        if isinstance(result, pd.DataFrame):
            result = result.to_dict(orient="records")
        elif isinstance(result, pd.Series):
            result = result.to_dict()

        return {"sql_query": sql_query, "result": result}
    except Exception as e:
        logging.error(f"NL2SQL error: {e}")
        import traceback; traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})
    # Hardcoded SQL queries for demo with plain text summaries
    data = await request.json()
    nl_query = data.get("query", "").lower()
    summary = "Query executed successfully"
    chart_type = "table"
    sql_query = None
    result = None
    data_out = None
    # Helper to extract data from execute_sql result
    def extract_data(res):
        if isinstance(res, dict) and "data" in res:
            return res["data"]
        return res
    if "citizen count" in nl_query:
        sql_query = "SELECT COUNT(*) as count FROM citizens"
        result = execute_sql(sql_query)
        data_out = extract_data(result)
        count = None
        # Try to extract count robustly from result dict
        if isinstance(result, dict) and "data" in result and result["data"] and "count" in result["data"][0]:
            count = result["data"][0]["count"]
        elif isinstance(data_out, list) and data_out and "count" in data_out[0]:
            count = data_out[0]["count"]
        elif isinstance(data_out, dict) and "count" in data_out:
            count = data_out["count"]
        if count is not None:
            summary = f"There are {count} citizens in the database."
        else:
            summary = f"Could not determine citizen count. Debug: {data_out}"
    elif "list all schemes" in nl_query:
        sql_query = "SELECT scheme_id, scheme_name, description FROM schemes"
        result = execute_sql(sql_query)
        data_out = extract_data(result)
        num_schemes = 0
        # Try to extract number of schemes robustly
        if isinstance(result, dict) and "data" in result:
            num_schemes = len(result["data"])
        elif isinstance(data_out, list):
            num_schemes = len(data_out)
        elif isinstance(data_out, dict):
            num_schemes = 1
        if num_schemes > 0:
            summary = f"There are {num_schemes} schemes available."
        else:
            summary = f"No schemes found. Debug: {data_out}"
    elif "show disbursements" in nl_query:
        sql_query = "SELECT * FROM disbursements"
        result = execute_sql(sql_query)
        data_out = extract_data(result)
        num_disbursements = 0
        # Try to extract number of disbursements robustly
        if isinstance(result, dict) and "data" in result:
            num_disbursements = len(result["data"])
        elif isinstance(data_out, list):
            num_disbursements = len(data_out)
        elif isinstance(data_out, dict):
            num_disbursements = 1
        if num_disbursements > 0:
            summary = f"There are {num_disbursements} disbursements recorded."
        else:
            summary = f"No disbursements found. Debug: {data_out}"
    else:
        sql_query = "SELECT 'Demo: No matching hardcoded query' as info"
        result = execute_sql(sql_query)
        data_out = extract_data(result)
        summary = "No matching hardcoded query. Please try a different question."
    return {
        "success": True,
        "sql_query": sql_query,
        "data": data_out,
        "summary": summary,
        "chart_type": chart_type
    }



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
        port=8080, 
        reload=True,
        log_level="info"
    )
