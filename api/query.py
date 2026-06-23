from fastapi import (
    APIRouter
)

from schemas.query_schema import (
    QueryRequest
)

from services.query_service import (
    ask_question
)

router = APIRouter()


@router.post(
    "/ask"
)
def ask(
    request:
    QueryRequest
):

    return ask_question(
        request.question
    )