from pydantic import BaseModel


class CustomerQueryRequest(BaseModel):
    customer_query: str


class CustomerReplyResponse(BaseModel):
    reply: str
