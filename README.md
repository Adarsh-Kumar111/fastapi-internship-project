# FastAPI Internship Project - AI Career & Resume Assistant

A robust backend service built with **FastAPI**, designed to handle user authentication, profile management, and automated PDF resume parsing.

---

## 🚀 Features

- **User Authentication:** Secure JWT-based access token authentication (Login & Signup).
- **Profile Management:** Endpoints to retrieve and update user profile information.
- **Resume Parsing:** Upload PDF resumes and extract structured text, candidate skills, contact info, and education details using `pdfplumber`.
- **Interactive Documentation:** Auto-generated API documentation with Swagger UI and ReDoc.

---

## 🛠️ Tech Stack

- **Framework:** FastAPI
- **Server:** Uvicorn
- **Validation:** Pydantic, email-validator
- **PDF Processing:** pdfplumber
- **Security:** PyJWT / Passlib (Bcrypt)

---

## 📂 Project Structure

```text
fastapi-internship-project/
├── app/
│   ├── main.py
│   ├── models/
│   ├── routes/
│   │   ├── auth.py
│   │   ├── profile.py
│   │   └── resume.py
│   └── utils/
├── requirements.txt
├── .gitignore
└── README.md
