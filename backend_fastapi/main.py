from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"msg": "JeanTrail AI backend is running!"}
