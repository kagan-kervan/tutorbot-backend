import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    grade = Column(Integer, nullable=False)  # 9, 10, 11, 12 gibi
    questions = relationship("Question", back_populates="user")


class Question(Base):
        __tablename__ = "questions"
        id = Column(Integer, primary_key=True, index=True)
        user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
        question = Column(Text, nullable=False)
        answer = Column(Text, nullable=True)
        created_at = Column(DateTime, default=datetime.datetime.utcnow)
        user = relationship("User", back_populates="questions")
