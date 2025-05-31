from pydantic import BaseModel

class QuestionRequest(BaseModel):
    user_id: int
    question: str

class AnswerResponse(BaseModel):
    question: str
    intent: str
    answer: str
    context: str
