from fastapi import APIRouter
from api.v1.endpoints import auth, jobs, candidates, interviews, dashboard, sourcing, voice

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])
api_router.include_router(candidates.router, prefix="/candidates", tags=["Candidates"])
api_router.include_router(interviews.router, prefix="/interviews", tags=["Interviews"])
api_router.include_router(sourcing.router, prefix="/sourcing", tags=["Candidate Sourcing"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(voice.router, prefix="/voice", tags=["Voice Calling"])
