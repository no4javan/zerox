
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pyzerox import zerox
import asyncio
import os
import uuid
from pathlib import Path
from config import settings

app = FastAPI(
    title="Document to Markdown Conversion API",
    description="API for converting various document formats to Markdown using Vision AI"
)

async def process_file(file_path: str, task_id: str, output_dir: str):
    try:
        result = await zerox(
            file_path=file_path,
            model="gpt-4o-mini",
            output_dir=output_dir,
            cleanup=settings.CLEANUP_TEMP,
            concurrency=settings.MAX_CONCURRENCY,
            temp_dir=settings.TEMP_DIR
        )
        
        # Save result to output directory
        result_path = Path(output_dir) / f"{task_id}_result.txt"
        with open(result_path, "w", encoding="utf-8") as f:
            for page in result.pages:
                f.write(page.content + "\n\n")
                
        return result
        
    except Exception as e:
        # Log error and cleanup
        print(f"Error processing file: {str(e)}")
        if os.path.exists(file_path):
            os.remove(file_path)
        raise e

@app.post("/convert/")
async def convert_document(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks
):
    # Generate unique task ID
    task_id = str(uuid.uuid4())
    
    # Create output directory
    output_dir = Path("output") / task_id
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save uploaded file
    file_path = output_dir / file.filename
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    # Start conversion in background
    background_tasks.add_task(
        process_file,
        str(file_path),
        task_id,
        str(output_dir)
    )
    
    return JSONResponse({
        "task_id": task_id,
        "message": "Conversion started",
        "status_endpoint": f"/status/{task_id}"
    })

@app.get("/status/{task_id}")
async def check_status(task_id: str):
    output_dir = Path("output") / task_id
    result_file = output_dir / f"{task_id}_result.txt"
    
    if not output_dir.exists():
        raise HTTPException(404, "Task not found")
    
    if result_file.exists():
        with open(result_file, "r", encoding="utf-8") as f:
            content = f.read()
        return {
            "status": "completed",
            "result": content
        }
    
    return {
        "status": "processing"
    }

@app.get("/")
async def read_root():
    return {
        "message": "Document to Markdown Conversion API",
        "endpoints": {
            "/convert/": "POST - Convert document to markdown",
            "/status/{task_id}": "GET - Check conversion status"
        }
    }

# Create required directories
os.makedirs(settings.TEMP_DIR, exist_ok=True)
os.makedirs("output", exist_ok=True)
