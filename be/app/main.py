from fastapi import FastAPI
from app.routes import simulation

app = FastAPI()


#api routes
app.include_router(simulation.router, prefix="/api")


#startup
@app.on_event("startup")
def startup():
    print("Starting up the application...")


#health
@app.get("/health")
def health_check():
    return {"status": "healthy"}
