from fastapi import FastAPI

from sql import models
from sql.database import engine

#models.Base.metadata.create_all(bind=engine)

app = FastAPI()



@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
