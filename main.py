from fastapi import FastAPI, status
from starlette.requests import Request
from starlette.responses import JSONResponse
from domain.exceptions import CoreException, NotFoundException
from routers import users, items

app = FastAPI()

app.include_router(users.router)
app.include_router(items.router)


@app.exception_handler(CoreException)
async def unicorn_exception_handler(request: Request, exc: CoreException):
    description = "Unknown exception" if exc.description is None else exc.description

    if type(exc) is NotFoundException:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=description)

    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=description)


@app.get("/")
async def throw_exception():
    return "ITS WORKS"




