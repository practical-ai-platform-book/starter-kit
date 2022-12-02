from fastapi import FastAPI

app = FastAPI()

@app.get("/greet/{name}")
def greet(name: str) -> dict[str, str]:
    return {"message": f"Hello, {name}!"}
