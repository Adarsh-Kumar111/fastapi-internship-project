import re
from typing import Dict, Any, List
import pdfplumber
import docx

# Technical and Soft skills keyword catalog
TECH_KEYWORDS = {
    "python", "fastapi", "django", "flask", "javascript", "typescript", "react", "node.js",
    "sql", "postgresql", "mysql", "mongodb", "docker", "kubernetes", "aws", "git",
    "html", "css", "c++", "java", "pandas", "numpy", "machine learning", "nlp"
}

SOFT_KEYWORDS = {
    "leadership", "communication", "teamwork", "problem solving", "critical thinking",
    "adaptability", "time management", "collaboration", "work ethic", "creativity"
}

def extract_text_from_pdf(file_path: str) -> str:
    extracted_text = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                extracted_text.append(text)
    return "\n".join(extracted_text)

def extract_text_from_docx(file_path: str) -> str:
    doc = docx.Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs if p.text])

def extract_email(text: str) -> str | None:
    match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    return match.group(0) if match else None

def extract_phone(text: str) -> str | None:
    match = re.search(r"(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}", text)
    return match.group(0).strip() if match else None

def extract_linkedin(text: str) -> str | None:
    match = re.search(r"(https?://(www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+)", text)
    return match.group(0) if match else None

def extract_github(text: str) -> str | None:
    match = re.search(r"(https?://(www\.)?github\.com/[a-zA-Z0-9_-]+)", text)
    return match.group(0) if match else None

def extract_sections(text: str) -> Dict[str, List[str]]:
    """Heuristic extraction for bullet points under specific section headers."""
    sections = {
        "education": [],
        "work_experience": [],
        "projects": [],
        "certifications": [],
        "internships": [],
        "languages": [],
        "achievements": []
    }
    
    current_section = None
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    headers_map = {
        "education": "education",
        "academic": "education",
        "experience": "work_experience",
        "employment": "work_experience",
        "work history": "work_experience",
        "projects": "projects",
        "certifications": "certifications",
        "certificates": "certifications",
        "internships": "internships",
        "languages": "languages",
        "achievements": "achievements",
        "honors": "achievements",
    }

    for line in lines:
        lower_line = line.lower()
        matched_header = None
        for keyword, sec_name in headers_map.items():
            if keyword in lower_line and len(line.split()) <= 4:
                matched_header = sec_name
                break
        
        if matched_header:
            current_section = matched_header
        elif current_section:
            sections[current_section].append(line)

    return sections

def parse_resume(file_path: str, filename: str) -> Dict[str, Any]:
    # 1. Extract text according to format
    if filename.lower().endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif filename.lower().endswith(".docx"):
        text = extract_text_from_docx(file_path)
    else:
        text = ""

    text_lower = text.lower()
    sections = extract_sections(text)

    # 2. Extract technical & soft skills
    tech_skills = [s.title() for s in TECH_KEYWORDS if s in text_lower]
    soft_skills = [s.title() for s in SOFT_KEYWORDS if s in text_lower]

    # 3. Guess Name (typically the first non-empty line of the resume)
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    guessed_name = lines[0] if lines and len(lines[0].split()) <= 4 else None

    # 4. Guess Summary
    summary = None
    for idx, l in enumerate(lines[:10]):
        if "summary" in l.lower() or "objective" in l.lower():
            if idx + 1 < len(lines):
                summary = lines[idx + 1]
                break

    return {
        "full_name": guessed_name,
        "email": extract_email(text),
        "phone_number": extract_phone(text),
        "address": None,
        "linkedin_url": extract_linkedin(text),
        "github_url": extract_github(text),
        "professional_summary": summary,
        "technical_skills": tech_skills,
        "soft_skills": soft_skills,
        "education": sections["education"][:5],
        "work_experience": sections["work_experience"][:10],
        "projects": sections["projects"][:10],
        "certifications": sections["certifications"][:5],
        "internships": sections["internships"][:5],
        "languages": sections["languages"][:5],
        "achievements": sections["achievements"][:5],
        "_raw_text": text
    }