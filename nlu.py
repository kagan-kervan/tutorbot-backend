def detect_intent(question: str) -> str:
    q = question.lower()
    if "nedir" in q or "tanımı" in q:
        return "definition"
    elif "çöz" in q or "nasıl yapılır" in q:
        return "solution"
    elif "örnek" in q:
        return "example"
    else:
        return "explanation"
