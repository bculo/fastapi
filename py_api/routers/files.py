import base64

from fastapi import UploadFile
from fastapi import APIRouter
from starlette import status
from starlette.responses import JSONResponse

router = APIRouter(
    prefix="/file",
    tags=["file"],
)


@router.post("/upload-file/")
async def create_upload_file(file: UploadFile):
    file_contents = await file.read()
    base64_encoded = base64.b64encode(file_contents).decode("utf-8")
    response_instance = {"filename": file.filename, "base64": base64_encoded}
    return JSONResponse(content=response_instance, status_code=status.HTTP_200_OK)
