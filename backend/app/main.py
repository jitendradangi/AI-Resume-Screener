from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "AI Resume Screener Backend Running"}