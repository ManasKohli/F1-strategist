import os

from fastapi import FastAPI
from app.routes import simulation, health
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


frontend_origins = [
    "http://localhost:5173",
    "http://localhost:5174",
]
frontend_origins.extend(
    origin.strip()
    for origin in os.getenv("FRONTEND_URLS", "").split(",")
    if origin.strip()
)


#react fe connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=frontend_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#api routes
app.include_router(simulation.router, prefix="/api")
app.include_router(health.router, prefix="/api")


#startup
@app.on_event("startup")
def startup():
    print("Starting up the application...")
