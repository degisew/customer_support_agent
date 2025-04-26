import os
from dotenv import load_dotenv
from fastapi import HTTPException
import google.generativeai as genai
from src.core.exceptions import InternalInvariantError
from src.auto_support_ai.schemas import CustomerQueryRequest, CustomerReplyResponse


load_dotenv()

# Configure Gemini API Key
GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")

print("DAG", GEMINI_API_KEY)

if not GEMINI_API_KEY:
    raise InternalInvariantError("Missing GEMINI_API_KEY in .env file.")


genai.configure(api_key=GEMINI_API_KEY)


class CustomerSupportService:
    """Service class for handling customer support AI agent interactions."""

    @staticmethod
    def generate_reply(customer_query: str) -> str:
        """
        Generate an intelligent and empathetic reply for a customer query using Gemini AI.

        Args:
            customer_query (str): The customer's input message.

        Returns:
            str: AI-generated customer support reply.
        """
        system_prompt = (
            "You are an intelligent, professional customer support AI agent.\n"
            "Analyze the emotional tone of the customer message (e.g., angry, happy, confused).\n"
            "Respond empathetically, politely, and helpfully.\n"
            "Keep the response clear, professional, and under 100 words.\n\n"
            f"Customer message: {customer_query}\n\n"
            "Your reply:"
        )

        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(system_prompt)
        return response.text.strip()

    @staticmethod
    async def get_customer_reply(
        request: CustomerQueryRequest,
    ) -> CustomerReplyResponse:
        """
        Process the incoming customer query and return the AI-generated reply.

        Args:
            request (CustomerQueryRequest): Pydantic model containing the customer query.

        Returns:
            CustomerReplyResponse: Pydantic model containing the AI agent's reply.

        Raises:
            HTTPException: If an error occurs during AI generation.
        """
        try:
            ai_reply: str = CustomerSupportService.generate_reply(
                request.customer_query
            )
            return CustomerReplyResponse(reply=ai_reply)
        except Exception as e:
            error_message = str(e)

            if "API key not valid" in error_message:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid API Key. Please check your credentials.",
                )
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Please try again later.",
        )
