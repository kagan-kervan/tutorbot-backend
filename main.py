from fastapi import FastAPI
from schemas import QuestionRequest, AnswerResponse
from nlu import detect_intent
from knoledge_base import get_context
from rag import retrieve_context, generate_with_gemini

app = FastAPI()

@app.get("/")
def home():
    return {"message": "TutorBot backend is running!"}


@app.post("/ask", response_model=AnswerResponse)
def ask_question(req: QuestionRequest):
    question = req.question
    intent = detect_intent(question)

    context = retrieve_context(question)
    answer = generate_with_gemini(context, question)

    return AnswerResponse(
        question=question,
        intent=intent,
        answer=answer,
        context=context
    )