from fastapi import FastAPI, HTTPException, status, Depends, BackgroundTasks, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from datetime import datetime, timedelta
import time
import jwt
from passlib.context import CryptContext

from fastapp.database import engine, Base, get_db
from fastapp.models import Course, Student, Enrollment, User
from fastapp.schemas import (
    CourseCreate, CourseResponse, CourseDetailResponse,
    StudentCreate, StudentResponse,
    EnrollmentCreate, EnrollmentResponse,
    UserCreate, UserResponse, Token
)

# --- SECURITY UTILITIES (Hands-On 10) ---
SECRET_KEY = "SUPER_SECRET_COMPLIANCE_KEY_2026"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")

app = FastAPI(
    title="Course Management System",
    description="Production-Grade Backend Architecture with Auth and Seeding Engine",
    version="3.0.0"
)

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # --- AUTOMATED DATA SEEDING (Hands-On 8) ---
    async with AsyncSession(engine) as session:
        course_check = await session.execute(select(Course))
        if not course_check.scalars().first():
            # Seed Base Courses
            c1 = Course(name="Asynchronous Programming", code="CS401", credits=4, department_id=1)
            c2 = Course(name="Microservice Architecture", code="CS402", credits=3, department_id=1)
            session.add_all([c1, c2])
            
            # Seed Administration User profile (password: admin123)
            admin_user = User(username="admin", hashed_password=pwd_context.hash("admin123"))
            session.add(admin_user)
            
            await session.commit()

def send_confirmation_email(student_email: str):
    time.sleep(1)
    print(f"\n[BACKGROUND WORKER] Sending confirmation to {student_email} -- SUCCESS\n")

# --- AUTH HELPER DEPENDENCY ---
async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")
        
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user


# =====================================================================
# 🔐 AUTHENTICATION ENDPOINTS (Hands-On 10)
# =====================================================================

@app.post("/api/auth/register", response_model=UserResponse, status_code=201, tags=["Authentication"])
async def register_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(User).where(User.username == user_in.username))
    if existing.scalars().first():
        raise HTTPException(status_code=400, detail="Username already registered")
    new_user = User(username=user_in.username, hashed_password=pwd_context.hash(user_in.password))
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@app.post("/api/auth/token", response_model=Token, tags=["Authentication"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == form_data.username))
    user = result.scalars().first()
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    token_data = {"sub": user.username, "exp": datetime.utcnow() + timedelta(minutes=30)}
    encoded_jwt = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": encoded_jwt, "token_type": "bearer"}


# =====================================================================
# 📚 COURSES MANAGEMENT & RELATIONSHIPS (Hands-On 8)
# =====================================================================

@app.get("/api/courses/", response_model=List[CourseResponse], tags=["Courses"])
async def get_all_courses(limit: int = 10, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).limit(limit))
    return result.scalars().all()

# SECURED POST ENDPOINT via dependency injection gate (Hands-On 10)
@app.post("/api/courses/", response_model=CourseResponse, status_code=201, tags=["Courses"])
async def create_course(course: CourseCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    code_check = await db.execute(select(Course).where(Course.code == course.code))
    if code_check.scalars().first():
        raise HTTPException(status_code=400, detail="Course code already exists.")
    db_course = Course(**course.model_dump())
    db.add(db_course)
    await db.commit()
    await db.refresh(db_course)
    return db_course

# NESTED SERIALIZATION ROUTE LOOKUP (Hands-On 8)
@app.get("/api/courses/{course_id}/detailed", response_model=CourseDetailResponse, tags=["Courses"])
async def get_course_details_nested(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalars().first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Extract structural items cleanly through join relationship proxy attributes
    students = [e.student for e in course.enrollments]
    
    return {
        "id": course.id,
        "name": course.name,
        "code": course.code,
        "credits": course.credits,
        "department_id": course.department_id,
        "enrolled_students": students
    }


# =====================================================================
# 🎓 STUDENTS & ENROLLMENTS ROUTERS
# =====================================================================

@app.post("/api/students/", response_model=StudentResponse, status_code=201, tags=["Students"])
async def create_student(student: StudentCreate, db: AsyncSession = Depends(get_db)):
    db_student = Student(**student.model_dump())
    db.add(db_student)
    await db.commit()
    await db.refresh(db_student)
    return db_student

@app.post("/api/enrollments/", response_model=EnrollmentResponse, status_code=201, tags=["Enrollments"])
async def create_enrollment(enrollment: EnrollmentCreate, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    student = (await db.execute(select(Student).where(Student.id == enrollment.student_id))).scalars().first()
    course = (await db.execute(select(Course).where(Course.id == enrollment.course_id))).scalars().first()
    if not student or not course:
        raise HTTPException(status_code=404, detail="Student or course profile target not found.")
    
    db_enrollment = Enrollment(**enrollment.model_dump())
    db.add(db_enrollment)
    await db.commit()
    await db.refresh(db_enrollment)
    background_tasks.add_task(send_confirmation_email, student.email)
    return db_enrollment