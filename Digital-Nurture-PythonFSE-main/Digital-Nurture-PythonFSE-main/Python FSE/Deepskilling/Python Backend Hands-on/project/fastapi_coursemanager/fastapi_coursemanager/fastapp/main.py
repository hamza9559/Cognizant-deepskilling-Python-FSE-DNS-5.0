from fastapi import FastAPI, HTTPException, status, Depends, BackgroundTasks, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
import time

from fastapp.database import engine, Base, get_db
from fastapp.models import Course, Student, Enrollment
from fastapp.schemas import (
    CourseCreate, CourseResponse,
    StudentCreate, StudentResponse,
    EnrollmentCreate, EnrollmentResponse
)

# 1. Custom OpenAPI Metadata Configuration Branding (Step 75)
app = FastAPI(
    title="Course Management System",
    description="High-performance backend engine powered by FastAPI & Async SQLAlchemy",
    version="2.5.0",
    contact={
        "name": "Academic Support Operations",
        "email": "backend-ops@saveetha.edu.in",
    }
)

# Async DB Auto-generation Hook
@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# --- BACKGROUND TASK WORKER ENGINE (Step 73) ---
def send_confirmation_email(student_email: str):
    # Simulating long-running I/O operation
    time.sleep(2) 
    print(f"\n[BACKGROUND WORKER] Sending confirmation to {student_email} -- SUCCESS\n")


# =====================================================================
# 🟩 1. COURSES ROUTING COMPONENT ENGINE
# =====================================================================

@app.get("/api/courses/", response_model=List[CourseResponse], status_code=status.HTTP_200_OK, tags=["Courses"])
async def get_all_courses(limit: int = 10, department_id: Optional[int] = None, db: AsyncSession = Depends(get_db)):
    query = select(Course)
    if department_id is not None:
        query = query.where(Course.department_id == department_id)
    result = await db.execute(query.limit(limit))
    return result.scalars().all()


@app.post("/api/courses/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED, 
          tags=["Courses"], summary="Create a new course catalog record", response_description="The newly mapped course data record")
async def create_course(course: CourseCreate, db: AsyncSession = Depends(get_db)):
    code_check = await db.execute(select(Course).where(Course.code == course.code))
    if code_check.scalars().first():
        raise HTTPException(status_code=400, detail=f"Course code {course.code} already exists.")
    
    db_course = Course(**course.model_dump())
    db.add(db_course)
    await db.commit()
    await db.refresh(db_course)
    return db_course


@app.get("/api/courses/{course_id}", response_model=CourseResponse, tags=["Courses"])
async def get_course_by_id(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalars().first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@app.put("/api/courses/{course_id}", response_model=CourseResponse, tags=["Courses"])
async def update_course(course_id: int, updated_data: CourseCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalars().first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    for key, val in updated_data.model_dump().items():
        setattr(course, key, val)
        
    await db.commit()
    await db.refresh(course)
    return course


@app.delete("/api/courses/{course_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Courses"])
async def delete_course(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalars().first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    await db.delete(course)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# RELATIONAL RELATIONAL JOIN QUERY ROUTE (Step 71)
@app.get("/api/courses/{course_id}/students/", response_model=List[StudentResponse], tags=["Courses"])
async def get_enrolled_students(course_id: int, db: AsyncSession = Depends(get_db)):
    course_check = await db.execute(select(Course).where(Course.id == course_id))
    if not course_check.scalars().first():
        raise HTTPException(status_code=404, detail="Course not found")

    query = select(Student).join(Enrollment, Student.id == Enrollment.student_id).where(Enrollment.course_id == course_id)
    result = await db.execute(query)
    return result.scalars().all()


# =====================================================================
# 🟩 2. STUDENTS ROUTING COMPONENT ENGINE
# =====================================================================

@app.get("/api/students/", response_model=List[StudentResponse], tags=["Students"])
async def get_all_students(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student))
    return result.scalars().all()


@app.post("/api/students/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED, tags=["Students"])
async def create_student(student: StudentCreate, db: AsyncSession = Depends(get_db)):
    email_check = await db.execute(select(Student).where(Student.email == student.email))
    if email_check.scalars().first():
        raise HTTPException(status_code=400, detail="Email matching this identification profile already exists.")
        
    db_student = Student(**student.model_dump())
    db.add(db_student)
    await db.commit()
    await db.refresh(db_student)
    return db_student


# =====================================================================
# 🟩 3. ENROLLMENTS ROUTING COMPONENT ENGINE
# =====================================================================

@app.post("/api/enrollments/", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED, tags=["Enrollments"])
async def create_enrollment(
    enrollment: EnrollmentCreate, 
    background_tasks: BackgroundTasks, 
    db: AsyncSession = Depends(get_db)
):
    # Verify both models exist prior to relationship assembly
    student = (await db.execute(select(Student).where(Student.id == enrollment.student_id))).scalars().first()
    course = (await db.execute(select(Course).where(Course.id == enrollment.course_id))).scalars().first()
    if not student or not course:
        raise HTTPException(status_code=404, detail="Target student or course reference identifier not found.")

    db_enrollment = Enrollment(**enrollment.model_dump())
    db.add(db_enrollment)
    await db.commit()
    await db.refresh(db_enrollment)

    # Dispatch non-blocking transaction to thread workers instantly (Step 73)
    background_tasks.add_task(send_confirmation_email, student.email)

    return db_enrollment