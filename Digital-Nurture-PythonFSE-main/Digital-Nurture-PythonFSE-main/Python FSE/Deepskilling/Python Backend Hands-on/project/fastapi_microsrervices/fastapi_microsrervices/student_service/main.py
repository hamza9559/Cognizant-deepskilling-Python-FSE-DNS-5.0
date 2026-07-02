from fastapi import FastAPI, HTTPException, status
import httpx

app = FastAPI(title="Student Service (Port 8001)")

@app.post("/api/v1/enrollments/")
async def enroll_student(enrollment: dict):
    # Inter-service communication ping
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("http://127.0.0.1:8002/api/v1/courses/")
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="Internal communication failure")
        except httpx.RequestError:
            # CRITICAL FIX: Explicitly pass status_code=503 inside the FastAPI HTTPException
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
                detail="Course Service is down"
            )
            
    return {"status": "Enrolled successfully", "data": enrollment}