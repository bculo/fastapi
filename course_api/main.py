from fastapi import FastAPI

from routers import students

app = FastAPI()

app.include_router(students.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
