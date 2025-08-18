from fastapi import FastAPI
from app.routes import admin_logs

app = FastAPI(title="BOTZZZ Admin API", version="1.0")

# include routes
app.include_router(admin_logs.router)

@app.get("/")
def root():
    return {"message": "BOTZZZ Admin API running"}
