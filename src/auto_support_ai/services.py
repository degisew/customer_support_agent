import os
import random
from dotenv import load_dotenv
import google.generativeai as genai
from fastapi import HTTPException
from src.core.exceptions import InternalInvariantError
from src.auto_support_ai.schemas import CustomerQueryRequest, CustomerReplyResponse


load_dotenv()

# Configure Gemini API Key
GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")


if not GEMINI_API_KEY:
    raise InternalInvariantError("Missing GEMINI_API_KEY in .env file.")


genai.configure(api_key=GEMINI_API_KEY)


class CustomerSupportService:
    """Service class for handling customer support AI agent interactions."""

    # TODO: This can be enhanced in the future by adding real
    # TODO: registration and authentication.
    FAKE_USERS: list[str] = ["user_1"]

    # TODO: This is an in-memory simulation to handle prompt history for now
    # TODO: We will handle this in a real DB in the future.
    USER_MEMORY: dict[str, list[str]] = {}

    @staticmethod
    def get_random_user_id() -> str:
        return random.choice(CustomerSupportService.FAKE_USERS)

    @staticmethod
    def update_user_memory(user_id: str, customer_query: str) -> None:
        if user_id not in CustomerSupportService.USER_MEMORY:
            CustomerSupportService.USER_MEMORY[user_id] = []

        CustomerSupportService.USER_MEMORY[user_id].append(customer_query)

        # Keep only the last 10 messages
        if len(CustomerSupportService.USER_MEMORY[user_id]) > 10:
            CustomerSupportService.USER_MEMORY[user_id] = (
                CustomerSupportService.USER_MEMORY[user_id][-10:]
            )

    @staticmethod
    def get_user_memory(user_id: str) -> list[str]:
        return CustomerSupportService.USER_MEMORY.get(user_id, [])

    @staticmethod
    def build_prompt(user_memory: list[str], new_message: str) -> str:
        memory_text = "\n".join([f"Customer said: {msg}" for msg in user_memory])

        system_prompt = (
            "You are an intelligent, professional customer support AI agent.\n"
            "You ONLY respond to valid customer service queries related to products, services, or issues.\n"
            "If a question is unrelated (like asking for poems, weather, etc.), politely say:\n"
            '"I\'m here to assist you with customer support only. Please let me know your issue."\n'
            "Analyze the emotional tone (e.g., angry, happy, confused). and respond accordingly\n"
            "But Don't say 'I understand' / It's frustrating everywhere without it's context. \n"
            "You have this history with the customer:\n"
            f"{memory_text}\n\n"
            "Now, respond to their new message:\n"
            f"{new_message}\n\n"
            "Respond empathetically, politely, helpfully, and under 100 words."
        )
        return system_prompt

    @staticmethod
    def generate_reply(customer_query: str) -> str:
        """
        Generate an intelligent and empathetic reply for a customer query using Gemini AI.

        Args:
            customer_query (str): The customer's input message.

        Returns:
            str: AI-generated customer support reply.
        """
        user_id: str = CustomerSupportService.get_random_user_id()
        user_memory: list[str] = CustomerSupportService.get_user_memory(user_id)
        prompt: str = CustomerSupportService.build_prompt(user_memory, customer_query)

        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)
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
            # TODO: This will be a logger
            print(f"##### {error_message}")

            if "API key not valid" in error_message:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid API Key. Please check your credentials.",
                )
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Please try again later.",
        )
