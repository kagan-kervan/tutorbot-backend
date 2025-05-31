from typing import Optional

from fastapi import FastAPI, Request, Response, Cookie

from schemas import QuestionRequest, AnswerResponse
from nlu import detect_intent
from knoledge_base import get_context
from rag import retrieve_context, generate_with_gemini
from curd import save_message_pair
from chat_memory import get_session_id, push_history, get_last_messages

app = FastAPI()

@app.get("/")
def home():
    return {"message": "TutorBot backend is running!"}


@app.post("/ask", response_model=AnswerResponse)
async def ask(req: QuestionRequest, response: Response, session_id: Optional[str] = Cookie(default=None)):
    sid = await get_session_id(session_id)
    if session_id is None:
        response.set_cookie("session_id", sid, max_age=60*60*24)

    history = await get_last_messages(sid)
    intent = detect_intent(req.question)
    context = retrieve_context(req.question)
    prompt_msgs = history + [
        {"role": "user", "content": req.question},
        {"role": "system", "content": f"Konu Bilgisi:\n{context}"}
    ]
    answer = generate_with_gemini(context, req.question)

    await push_history(sid, "user", req.question)
    await push_history(sid, "assistant", answer)
    await save_message_pair(user_id=req.user_id, session_id=sid, question=req.question, answer=answer, intent=intent)

    return AnswerResponse(question=req.question, intent=intent, answer=answer)