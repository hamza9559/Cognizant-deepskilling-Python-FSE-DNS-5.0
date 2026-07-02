from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime

# --- COURSE SCHEMAS ---
class CourseBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    code: str = Field(..., min_length=3, max_length=20)
    credits: int = Field(..., ge=1, le=5)

class CourseCreate(CourseBase):
    department_id: int

class CourseResponse(CourseBase):
    id: int
    department_id: int
    class Config:
        from_attributes = True

# --- STUDENT SCHEMAS ---
class StudentBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr

class StudentCreate(StudentBase):
    pass

class StudentResponse(StudentBase):
    id: int
    class Config:
        from_attributes = True

# --- NESTED RELATIONSHIP RESPONSE (Hands-On 8) ---
class CourseDetailResponse(CourseResponse):
    enrolled_students: List[StudentResponse] = []

# --- ENROLLMENT SCHEMAS ---
class EnrollmentBase(BaseModel):
    student_id: int
    course_id: int

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentResponse(EnrollmentBase):
    id: int
    enrollment_date: datetime
    class Config:
        from_attributes = True

# --- USER & AUTH SCHEMAS (Hands-On 10) ---
class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str