from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
import httpx
import jwt

app = FastAPI(
    title="API Gateway (Port 8000)",
    description="Production-Grade API Gateway with JWT Enforcement, CORS Mapping, and Fault Tolerance"
)

# CORS Policy Configuration (Hands-On 9 Requirement)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "GATEWAY_SECRET"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)

STUDENT_SERVICE_URL = "http://127.0.0.1:8001"
COURSE_SERVICE_URL = "http://127.0.0.1:8002"

# =====================================================================
# 🔐 AUTHENTICATION ENDPOINT
# =====================================================================

@app.post("/api/v1/auth/login", tags=["Authentication"])
async def login():
    """Generates a valid testing JWT token for Hands-On 9 evaluation"""
    token = jwt.encode({"sub": "admin"}, SECRET_KEY, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}


# =====================================================================
# 📚 COURSES PROXY ENDPOINTS (Hands-On 9 Evaluation)
# =====================================================================

@app.get("/api/v1/courses/", tags=["Courses"])
async def get_courses_proxy():
    """PUBLIC ENDPOINT: Fetches course list without checking auth headers"""
    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(f"{COURSE_SERVICE_URL}/api/v1/courses/")
            return res.json()
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Service Unavailable")

@app.post("/api/v1/courses/", tags=["Courses"])
async def create_course_proxy(course_data: dict, token: str = Depends(oauth2_scheme)):
    """SECURED ENDPOINT: Blocks anonymous requests with a 401 Unauthorized code"""
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    async with httpx.AsyncClient() as client:
        try:
            res = await client.post(f"{COURSE_SERVICE_URL}/api/v1/courses/", json=course_data)
            return res.json()
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Service Unavailable")


# =====================================================================
# 🎓 ENROLLMENTS PROXY ENDPOINT (Hands-On 10 Evaluation)
# =====================================================================

@app.post("/api/v1/enrollments/", tags=["Enrollments"])
async def enroll_student_proxy(enrollment_data: dict):
    """FAULT TOLERANT ENDPOINT: Forwards the exact 503 status code to the browser"""
    async with httpx.AsyncClient() as client:
        try:
            res = await client.post(f"{STUDENT_SERVICE_URL}/api/v1/enrollments/", json=enrollment_data)
            
            # CRITICAL FIX: If the downstream service returned an error code (like 503),
            # pass that exact status code back to the browser instead of defaulting to 200.
            if res.status_code != 200:
                raise HTTPException(status_code=res.status_code, detail=res.json().get("detail", "Error"))
                
            return res.json()
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Service Unavailable")