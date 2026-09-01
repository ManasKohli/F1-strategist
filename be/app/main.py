from fastapi import FastAPI
from app.routes import simulation, health
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


#react fe connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
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
