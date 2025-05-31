import datetime
from typing import Optional

from pydantic import BaseModel


class QuestionRequest(BaseModel):
    user_id: int
    question: str


class AnswerResponse(BaseModel):
    question: str
    intent: str
    answer: str
    context: str


class UserCreate(BaseModel):
    name: str
    grade: int


class UserRead(BaseModel):
    id: int
    name: str
    grade: int

    class Config:
        orm_mode = True


class QuestionCreate(BaseModel):
    user_id: int
    question: str
    answer: Optional[str] = None


class QuestionRead(BaseModel):
    id: int
    user_id: int
    question: str
    answer: Optional[str]
    created_at: datetime.datetime

    class Config:
        orm_mode = True
