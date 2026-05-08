from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

class BaselineModel:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=10000, stop_words='english')
        self.clf = LogisticRegression(class_weight='balanced')

    def train(self, texts: list[str], labels: list[int]):
        X = self.vectorizer.fit_transform(texts)
        self.clf.fit(X, labels)
        joblib.dump((self.vectorizer, self.clf), 'baseline.pkl')

    def predict(self, text: str) -> float:
        vec, clf = joblib.load('baseline.pkl')
        X = vec.transform([text])
        return clf.predict_proba(X)[0][1] # Probability of being "True"