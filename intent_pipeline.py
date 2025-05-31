import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

# Veri setini oku
df = pd.read_csv("intent_dataset_50.csv")

# Train/test ayır
X_train, X_test, y_train, y_test = train_test_split(df["sentence"], df["intent"], test_size=0.2, random_state=42)

# Pipeline: TF-IDF + LogisticRegression
clf = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
    ("lr", LogisticRegression(max_iter=200))
])

# Eğit
clf.fit(X_train, y_train)

# Değerlendir
acc = clf.score(X_test, y_test)
print(f"Test accuracy: {acc:.2f}")

# Kaydet
joblib.dump(clf, "intent_classifier.pkl")