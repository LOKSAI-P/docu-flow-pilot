
"""
API endpoints for tGPT
This module provides a RESTful API for the tGPT backend services.
"""
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
import sys
import os

# Add parent directory to path to import services
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import services
from search_assistant.search_service import SearchService
from data_generator.generator_service import DataGeneratorService
from meeting_summarizer.summarizer_service import MeetingSummarizerService
from nfr_assistant.nfr_service import NFRService

app = FastAPI(title="tGPT API", description="Team Guidance and Productive Tool API")

# Initialize services
search_service = SearchService()
data_generator_service = DataGeneratorService()
meeting_summarizer_service = MeetingSummarizerService()
nfr_service = NFRService()

# Models for request/response
class SearchQuery(BaseModel):
    query: str
    base_url: str
    space_key: str
    auth_token: str
    top_k: int = 5

class QuestionRequest(BaseModel):
    question: str
    context: str

class TemplateRequest(BaseModel):
    template_id: str
    template_content: str
    template_type: str = "json"

class GenerateDataRequest(BaseModel):
    template_id: str
    count: int = 1

class ConfluenceUploadRequest(BaseModel):
    page_id: str
    base_url: str
    auth_token: str

class MeetingData(BaseModel):
    title: str
    date: str
    duration: str
    participants: List[str]
    summary: str
    key_points: List[str]
    action_items: Optional[List[str]] = None
    decisions: Optional[List[str]] = None

class NFRData(BaseModel):
    project_name: str
    project_description: str
    requirements: Dict[str, List[Dict[str, Any]]]
    audit_trail: Optional[List[Dict[str, str]]] = None

# API Routes

# Search Assistant Routes
@app.post("/search/fetch-pages")
async def fetch_confluence_pages(request: SearchQuery):
    result = search_service.fetch_confluence_pages(
        request.base_url, 
        request.space_key, 
        request.auth_token
    )
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result

@app.post("/search/query")
async def search_pages(request: SearchQuery):
    result = search_service.search(request.query, request.top_k)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result

@app.post("/search/answer")
async def answer_question(request: QuestionRequest):
    result = search_service.answer_question(request.question, request.context)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result

# Data Generator Routes
@app.post("/generator/load-template")
async def load_template(request: TemplateRequest):
    result = data_generator_service.load_template(
        request.template_id, 
        request.template_content,
        request.template_type
    )
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result

@app.post("/generator/generate")
async def generate_data(request: GenerateDataRequest):
    result = data_generator_service.generate_data(request.template_id, request.count)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result

@app.post("/generator/upload-to-confluence")
async def upload_generator_output(
    content: str = Form(...),
    content_type: str = Form(...),
    request: ConfluenceUploadRequest = Form(...)
):
    # Parse the content based on type
    if content_type.lower() == "json":
        parsed_content = json.loads(content)
    else:
        parsed_content = content
        
    # Parse the request
    request_dict = json.loads(request)
    confluence_request = ConfluenceUploadRequest(**request_dict)
    
    result = data_generator_service.upload_to_confluence(
        confluence_request.page_id,
        parsed_content,
        content_type,
        confluence_request.base_url,
        confluence_request.auth_token
    )
    
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result

# Meeting Summarizer Routes
@app.post("/meeting/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    result = meeting_summarizer_service.transcribe_audio(file.file)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result

@app.post("/meeting/summarize")
async def summarize_text(text: str = Form(...), max_length: int = Form(150), min_length: int = Form(50)):
    result = meeting_summarizer_service.summarize_text(text, max_length, min_length)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result

@app.post("/meeting/generate-report")
async def generate_meeting_report(meeting_data: MeetingData):
    result = meeting_summarizer_service.generate_markdown_report(meeting_data.dict())
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result

@app.post("/meeting/upload-to-confluence")
async def upload_meeting_summary(
    markdown_content: str = Form(...),
    request: ConfluenceUploadRequest = Form(...)
):
    # Parse the request
    request_dict = json.loads(request)
    confluence_request = ConfluenceUploadRequest(**request_dict)
    
    result = meeting_summarizer_service.upload_to_confluence(
        confluence_request.page_id,
        markdown_content,
        confluence_request.base_url,
        confluence_request.auth_token
    )
    
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result

# NFR Assistant Routes
@app.post("/nfr/suggest-category")
async def suggest_nfr_category(requirement_text: str = Form(...)):
    result = nfr_service.suggest_nfr_category(requirement_text)
    if not result:
        raise HTTPException(status_code=400, detail="Failed to suggest category")
    return {"suggestions": result}

@app.post("/nfr/generate-doc")
async def generate_nfr_doc(nfr_data: NFRData):
    result = nfr_service.generate_markdown_doc(nfr_data.dict())
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result

@app.post("/nfr/export-docx")
async def export_nfr_to_docx(markdown_content: str = Form(...)):
    result = nfr_service.export_to_docx(markdown_content)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    
    # In a real API, you would return the file for download
    # This is simplified for demonstration
    return {"file_path": result["file_path"]}

@app.post("/nfr/export-pdf")
async def export_nfr_to_pdf(markdown_content: str = Form(...)):
    result = nfr_service.export_to_pdf(markdown_content)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    
    # In a real API, you would return the file for download
    # This is simplified for demonstration
    return {"file_path": result["file_path"]}

@app.post("/nfr/upload-to-confluence")
async def upload_nfr_doc(
    markdown_content: str = Form(...),
    request: ConfluenceUploadRequest = Form(...)
):
    # Parse the request
    request_dict = json.loads(request)
    confluence_request = ConfluenceUploadRequest(**request_dict)
    
    result = nfr_service.upload_to_confluence(
        confluence_request.page_id,
        markdown_content,
        confluence_request.base_url,
        confluence_request.auth_token
    )
    
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result

# Healthcheck endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
