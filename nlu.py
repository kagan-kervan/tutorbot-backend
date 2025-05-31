import joblib
model = joblib.load("intent_classifier.pkl")

def detect_intent(question: str) -> str:
    return model.predict([question])[0]
