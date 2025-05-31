import os
from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User, Base, Question
from nlu import detect_intent
from rag import retrieve_context, generate_with_gemini
from schemas import UserCreate, AnswerResponse, QuestionRequest, QuestionRead, UserRead, QuestionCreate
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL  # Import from the config file

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get("/")
def home():
    return {"message": "TutorBot backend is running!"}



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Kullanıcı listesini getirme
@app.get("/users/", response_model=List[UserRead])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name, grade=user.grade)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



# Soru kaydetme (answer parametresiz de olabilir, cevap sonradan eklenebilir)
@app.post("/questions/", response_model=QuestionRead)
def create_question(question: QuestionCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == question.user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_question = Question(user_id=question.user_id, question=question.question, answer=question.answer)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


@app.post("/ask", response_model=AnswerResponse)
def ask_question(req: QuestionRequest, db: Session = Depends(get_db)):
    question = req.question
    intent = detect_intent(question)
    context = retrieve_context(question)

    # Kullanıcıyı bul
    user = db.query(User).filter(User.id == req.user_id).first()
    grade = user.grade if user else 9  # Default 9. sınıf

    answer = generate_with_gemini(context, question, grade)
    # Soru ve cevabı veritabanına kaydet
    if user:
        create_question_entry(db, user_id=user.id, question=question, answer=answer)

    return AnswerResponse(
        question=question,
        intent=intent,
        answer=answer,
        context=context
    )

# Soru listesini getirme
@app.get("/questions/", response_model=List[QuestionRead])
def get_questions(db: Session = Depends(get_db)):
    return db.query(Question).all()


def create_question_entry(db, user_id: int, question: str, answer: str = None):
    """
    Yeni bir question kaydını veritabanına ekler.
    """
    db_question = Question(user_id=user_id, question=question, answer=answer)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question