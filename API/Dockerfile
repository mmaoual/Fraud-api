FROM ubuntu:20.04
WORKDIR /Fraud-api/API
ADD Model/DecisionTreeClassifier_model.joblib Model/LogisticRegression_model.joblib Model/RandomForestClassifier_model.joblib ./
ADD API/requirements.txt API/fraud.py ./
RUN apt-get update && apt-get install python3-pip -y && pip install -r ./requirements.txt
EXPOSE 8000
CMD uvicorn strokes:server --host 0.0.0.0