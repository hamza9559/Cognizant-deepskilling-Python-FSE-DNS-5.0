from fastapi import FastAPI

app = FastAPI(title="Course Service (Port 8002)")

COURSES = [
    {"id": 1, "name": "Asynchronous Programming", "code": "CS401"},
    {"id": 2, "name": "Microservice Architecture", "code": "CS402"}
]

@app.get("/api/v1/courses/")
async def get_courses():
    return COURSES

@app.post("/api/v1/courses/")
async def create_course(course: dict):
    COURSES.append(course)
    return course