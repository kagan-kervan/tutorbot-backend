from models import User, Conversation, Message
from database import SessionLocal


def save_message_pair(user_id, session_id, question, answer, intent):
    db = SessionLocal()
    try:
        conv = db.query(Conversation).filter_by(session_id=session_id).first()
        if not conv:
            conv = Conversation(user_id=user_id, session_id=session_id)
            db.add(conv)
            db.commit()
            db.refresh(conv)

        db.add_all([
            Message(conversation_id=conv.id, role="user", content=question),
            Message(conversation_id=conv.id, role="assistant", content=answer)
        ])
        db.commit()
    finally:
        db.close()
