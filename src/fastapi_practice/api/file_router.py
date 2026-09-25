from fastapi import APIRouter, File, UploadFile

file_router = APIRouter(prefix="/file", tags=["File"])

@file_router.post("/upload-file")
async def upload_file(
    file : UploadFile = File(...)
):
    return {
        "file_name" : file.filename,
        "file_type" : file.content_type
    }