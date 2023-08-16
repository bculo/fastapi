import base64

from fastapi import UploadFile
from fastapi import APIRouter

router = APIRouter(
    prefix="/file",
    tags=["file"],
)


@router.post("/file/upload-file/")
async def create_upload_file(file: UploadFile):
    file_contents = await file.read()
    base64_encoded = base64.b64encode(file_contents).decode("utf-8")
    return {"filename": file.filename, "base64": base64_encoded}
