from pydantic import BaseModel, EmailStr, Field


class FeedbackRequest(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    message: str = Field(min_length=1, max_length=4000)


class FeedbackResponse(BaseModel):
    ok: bool
    status: str
    request_id: str
