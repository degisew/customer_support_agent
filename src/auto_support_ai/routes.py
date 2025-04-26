from fastapi.routing import APIRouter

from src.auto_support_ai.services import CustomerSupportService
from src.auto_support_ai.schemas import CustomerQueryRequest, CustomerReplyResponse


router = APIRouter()


@router.post(
    "/reply",
    response_model=CustomerReplyResponse,
    summary="Generate a customer support reply",
    description="Takes a customer query as input and returns an empathetic, AI-generated customer support reply.",
)
async def get_customer_reply(
    request: CustomerQueryRequest,
) -> CustomerReplyResponse:
    """
    Endpoint to generate a customer support reply based on the input query.

    Args:
        request (CustomerQueryRequest): Request body containing the customer's query.

    Returns:
        CustomerReplyResponse: Response containing the AI-generated reply.
    """
    return await CustomerSupportService.get_customer_reply(request)
