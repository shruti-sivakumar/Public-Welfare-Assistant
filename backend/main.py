"""
FastAPI Backend for Data Interpreter Assistant with Voice
Main application entry point with comprehensive configuration
"""
print("FASTAPI CONTAINER STARTUP: main.py loaded")

from openai import AzureOpenAI
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
from db import execute_sql
from dotenv import load_dotenv
load_dotenv()

# Instantiate AzureOpenAI client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)


# Configure logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import routes with error handling
try:
    from routes.query import router as query_router
    from routes.verify import router as verify_router
    from routes.summary import router as summary_router
    routes_available = True
except Exception as e:
    logger.warning(f"Routes not available: {e}")
    routes_available = False

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
        "http://127.0.0.1:8080",   # Alternative frontend
        "https://welfare-frontend-app.azurewebsites.net",  # Deployed frontend
        "*"  # Allow all origins for development (remove in production)
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include routers
if routes_available:
    app.include_router(query_router)
    app.include_router(verify_router)
    app.include_router(summary_router)
    logger.info("All route modules loaded successfully")
else:
    logger.warning("Route modules not available - running with basic endpoints only")

# Add request logging middleware
@app.post("/nl2sql")
async def nl2sql(request: Request):
    try:
        from prompt_engine import PromptEngine
        
        data = await request.json()
        nl_query = data.get("query")
        
        # Use the PromptEngine with proper schema context
        engine = PromptEngine()
        result = engine.process_query(nl_query)
        
        return result
        
    except Exception as e:
        logging.error(f"NL2SQL error: {e}")
        import traceback; traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})



@app.get("/")
async def root():
    """API Root - Welcome message and basic info"""
    return {
        "message": " Data Interpreter Assistant API",
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
        "database": "Connected",  
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
    logger.info(" Starting Data Interpreter Assistant API...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
