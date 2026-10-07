from fastapi import FastAPI
from app.database import Base,engine
import app.models
from app.routes.auth import router as auth_router
from app.routes.projects import router as project_router
from app.routes.tasks import router as task_router
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from app.limiter import limiter
from slowapi import _rate_limit_exceeded_handler


app=FastAPI()


app.state.limiter = limiter

app.add_middleware(SlowAPIMiddleware)
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

Base.metadata.create_all(engine)
app.include_router(auth_router)
app.include_router(project_router)
app.include_router(task_router)