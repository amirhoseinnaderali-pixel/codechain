import os
from typing import Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from agents import super_code_generator

class RunRequest(BaseModel):
    task: str
    language: Optional[str] = "python"
    verbose: Optional[bool] = False
    api_key: Optional[str] = None
    mode: Optional[str] = "fast"

app = FastAPI(title="DevGenie API", version="1.0.0", description="AI Code Assistant powered by Google Gemini")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def trim(text: str, limit: int = 8000):
    if not isinstance(text, str):
        return text
    return text if len(text) <= limit else text[:limit] + "\n\n...[truncated]"

@app.post("/run")
async def run_task(req: RunRequest):
    """Run coding task with API key"""
    print(f"📥 Received request: task='{req.task[:50]}...', has_api_key={bool(req.api_key)}")
    
    # Get API key from request body first (required)
    api_key = req.api_key
    
    # Fallback to environment variable if not provided in request
    if not api_key:
        api_key = os.getenv("GOOGLE_API_KEY", "")
        print("⚠️ Using API key from environment variable")
    
    if not api_key:
        print("❌ No API key provided")
        raise HTTPException(
            status_code=400, 
            detail="Google AI Studio API key is required. Please provide it in the request body or set GOOGLE_API_KEY environment variable."
        )
    
    try:
        mode = req.mode or "fast"
        print(f"🚀 Starting super_code_generator with api_key length: {len(api_key) if api_key else 0}, mode: {mode}")
        result = super_code_generator(
            task=req.task,
            api_key=api_key,
            mode=mode
        )
        print("✅ super_code_generator completed successfully")
        
        # Support both dict and string results from super_code_generator
        if isinstance(result, dict):
            payload = {
                "requirements": trim(result.get("requirements", ""), 4000),
                "selected_design": trim(result.get("selected_design", ""), 4000),
                "final_code": trim(result.get("final_code", result.get("final_output", "")), 8000),
                "documentation": trim(result.get("documentation", ""), 6000),
                "security_audit": trim(result.get("security_audit", ""), 4000),
                "performance_metrics": result.get("performance_metrics", {}),
                "complexity_score": result.get("complexity_score", 0.0),
                "total_models_used": result.get("total_models_used", result.get("total_models", 0)),
                "messages": result.get("messages", result.get("all_steps", [])),
                "workflow_started": result.get("workflow_started"),
                "workflow_completed": result.get("workflow_completed", result.get("completed_at")),
            }
        else:
            # When a plain string is returned, treat it as the final code/output
            payload = {
                "requirements": "",
                "selected_design": "",
                "final_code": trim(str(result), 8000),
                "documentation": "",
                "security_audit": "",
                "performance_metrics": {},
                "complexity_score": 0.0,
                "total_models_used": 0,
                "messages": [],
                "workflow_started": None,
                "workflow_completed": None,
            }
        return payload
    
    except Exception as e:
        print(f"❌ Error in run_task: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Backend is running"}

@app.options("/run")
async def run_options():
    """Handle CORS preflight"""
    return {"status": "ok"}

# Serve index.html at root
@app.get("/")
async def root_index():
    index_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    if not os.path.exists(index_path):
        raise HTTPException(status_code=404, detail="index.html not found")
    return FileResponse(index_path)

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
else:
    print(f"Warning: Static directory not found: {static_dir}")

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8000))
    print("=" * 60)
    print(f"Starting DevGenie API on 0.0.0.0:{port}")
    print("=" * 60)
    print("📝 API key should be provided in requests")
    print("=" * 60)
    uvicorn api:app --host 0.0.0.0 --port $PORT
    
