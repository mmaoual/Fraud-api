FROM debian:latest
RUN apt-get update && apt-get install python3-pip -y && pip install requests
ENV LOG 1
ADD transactionPrediction.py /Fraud-api/transactionPrediction.py
WORKDIR /Fraud-api/
EXPOSE 8003
CMD python3 transactionPrediction.py
