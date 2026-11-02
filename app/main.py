from fastapi import FastAPI
from app.db.database import Base, engine
from app.routers import auth, profile, resume

# Create all database tables automatically on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Internship API Portal",
    description="REST APIs for User Management, JWT Authentication, and Resume Parsing",
    version="1.0.0"
)

# Register routers
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(resume.router)

@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "FastAPI Internship Project is running smoothly!"}
