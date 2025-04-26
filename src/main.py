from fastapi import FastAPI
from src.core.exceptions import register_global_exceptions
from src.auto_support_ai.routes import router as support_router

app = FastAPI(
    title="AutoSupportAI - Customer Support Agent",
    description="AI-powered API to generate customer support replies using Gemini",
    version="1.0",
)


app.include_router(support_router)


register_global_exceptions(app)
