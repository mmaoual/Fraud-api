FROM debian:latest
RUN apt-get update && apt-get install python3-pip -y && pip install requests
ENV LOG 1
ADD performance.py /Fraud-api/performance.py
WORKDIR /Fraud-api/
EXPOSE 8001
CMD python3 performance.py
