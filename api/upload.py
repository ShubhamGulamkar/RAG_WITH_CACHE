# from fastapi import (
#     APIRouter,
#     UploadFile
# )

# from services.document_service import (
#     process_document
# )

# router = APIRouter()


# @router.post(
#     "/upload"
# )
# async def upload_file(
#     file: UploadFile
# ):

#     content = (
#         await file.read()
#     )

#     success, message = (
#         process_document(
#             file.filename,
#             content
#         )
#     )

#     return {
#         "success": success,
#         "message": message
#     }

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
    status
)

from services.document_service import (
    process_document
)

router = APIRouter(
    tags=["Document Upload"]
)

SUPPORTED_EXTENSIONS = {
    "txt",
    "pdf",
    "docx"
}


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...)
):
    try:

        print("=" * 50)
        print("Upload Request Received")

        if not file.filename:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Filename is missing."
            )

        extension = (
            file.filename
            .split(".")[-1]
            .lower()
        )

        print(
            f"File Name : {file.filename}"
        )

        print(
            f"Extension : {extension}"
        )

        if extension not in SUPPORTED_EXTENSIONS:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Supported file types: "
                    "TXT, PDF, DOCX"
                )
            )

        content = await file.read()

        if not content:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is empty."
            )

        print(
            f"File Size : "
            f"{len(content)} bytes"
        )

        success, message = (
            process_document(
                filename=file.filename,
                file_bytes=content
            )
        )

        print(
            f"Processing Result : {message}"
        )

        return {
            "success": success,
            "filename": file.filename,
            "message": message
        }

    except HTTPException:
        raise

    except Exception as ex:

        print(
            f"Upload Error : {str(ex)}"
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(ex)
        )