from fastapi import FastAPI

app = FastAPI()


#startup
@app.on_event("startup")
def startup():
    print("Starting up the application...")


#health
@app.get("/health")
def health_check():
    return {"status": "healthy"}
