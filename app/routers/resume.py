import os
import shutil
from uuid import uuid4
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import ResumeRecord, User
from app.core.security import get_current_user
from app.core.config import settings
from app.services.parser import parse_resume

router = APIRouter(prefix="/resume", tags=["Resume Parsing"])

ALLOWED_EXTENSIONS = {".pdf", ".docx"}

@router.post("/parse", status_code=status.HTTP_201_CREATED)
async def upload_and_parse_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Validate extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file format. Only PDF and DOCX files are allowed."
        )

    # Save physical file to uploads directory
    unique_filename = f"{uuid4().hex}_{file.filename}"
    saved_file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)

    with open(saved_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Run parsing logic
        parsed_result = parse_resume(saved_file_path, file.filename)
        raw_text = parsed_result.pop("_raw_text", "")

        # Persist resume record and extracted data to DB
        record = ResumeRecord(
            user_id=current_user.id,
            filename=file.filename,
            file_path=saved_file_path,
            raw_text=raw_text,
            parsed_data=parsed_result
        )
        db.add(record)
        db.commit()
        db.refresh(record)

        return {
            "id": record.id,
            "filename": record.filename,
            "extracted_data": record.parsed_data,
            "uploaded_at": record.uploaded_at
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while parsing the resume: {str(e)}"
        )