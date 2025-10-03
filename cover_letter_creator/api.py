import os
import tempfile
import uuid

from creator import Creator, Replacements
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from seek_api import SeekApi

from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import os
import uuid
from typing import List

from models import Template
from database import get_db, init_db

from cover_letter_creator.utils import get_template_from_id

TEMPLATE_API_ENDPOINT = None

app = FastAPI(title="Cover Letter Generator")


class CoverLetterRequest(BaseModel):
    url: str
    name: str
    template_id: str


def create_cover_letter(url: str, name: str, template_filepath: str) -> str:
    for result in SeekApi().from_url(url):
        replacements = Replacements.from_result(result)
        creator = Creator(template_filepath)
        return creator.run(
            replacements=replacements,
            description=result.description,
            output_dir=tempfile.gettempdir(),
            applicant_name=name,
        )


@app.post("/generate-cover-letter/")
async def generate_cover_letter(request: CoverLetterRequest):
    try:
        template_filepath = get_template_from_id(request.template_id)
        file_path = create_cover_letter(request.url, request.name, template_filepath)
        filename = os.path.basename(file_path)
        return FileResponse(
            path=file_path, filename=filename, media_type="application/octet-stream"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating cover letter: {str(e)}"
        )


@app.get("/")
async def root():
    return {"message": "Cover Letter Generator API"}

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/")
async def root():
    return {"message": "DOCX Template Manager API"}

@app.post("/templates/upload", response_model=dict)
async def upload_template(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload a DOCX template file
    """
    if not file.filename.lower().endswith('.docx'):
        raise HTTPException(
            status_code=400, 
            detail="Only DOCX files are allowed"
        )
    
    template_id = str(uuid.uuid4())

    safe_filename = f"{template_id}_{file.filename}"
    file_path = os.path.join("cover_letter_creator/templates", safe_filename)
    
    try:
        contents = await file.read()
        file_size = len(contents)
        
        with open(file_path, "wb") as f:
            f.write(contents)
        
        db_template = Template(
            template_id=template_id,
            filename=file.filename,
            file_path=file_path,
            file_size=file_size
        )
        
        db.add(db_template)
        db.commit()
        db.refresh(db_template)
        
        return {
            "template_id": template_id,
            "filename": file.filename,
            "file_size": file_size,
            "message": "Template uploaded successfully"
        }
        
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=500, 
            detail=f"Error uploading template: {str(e)}"
        )

@app.get("/templates", response_model=List[dict])
async def list_templates(db: Session = Depends(get_db)):
    """
    Get list of all uploaded templates
    """
    templates = db.query(Template).all()
    
    return [
        {
            "template_id": template.template_id,
            "filename": template.filename,
            "upload_date": template.upload_date.isoformat(),
            "file_size": template.file_size
        }
        for template in templates
    ]

@app.get("/templates/{template_id}")
async def get_template_info(template_id: str, db: Session = Depends(get_db)):
    """
    Get information about a specific template
    """
    template = db.query(Template).filter(Template.template_id == template_id).first()
    
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    return {
        "template_id": template.template_id,
        "filename": template.filename,
        "upload_date": template.upload_date.isoformat(),
        "file_size": template.file_size,
        "file_path": template.file_path
    }

@app.delete("/templates/{template_id}")
async def delete_template(template_id: str, db: Session = Depends(get_db)):
    """
    Delete a template by template_id
    """
    template = db.query(Template).filter(Template.template_id == template_id).first()
    
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    try:
        # Delete file from filesystem
        if os.path.exists(template.file_path):
            os.remove(template.file_path)
        
        # Delete record from database
        db.delete(template)
        db.commit()
        
        return {
            "message": "Template deleted successfully",
            "template_id": template_id,
            "filename": template.filename
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error deleting template: {str(e)}"
        )

@app.get("/templates/{template_id}/download")
async def download_template(template_id: str, db: Session = Depends(get_db)):
    """
    Download a template file
    """
    from fastapi.responses import FileResponse
    
    template = db.query(Template).filter(Template.template_id == template_id).first()
    
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    if not os.path.exists(template.file_path):
        raise HTTPException(status_code=404, detail="Template file not found")
    
    return FileResponse(
        path=template.file_path,
        filename=template.filename,
        media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )

# Error handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
