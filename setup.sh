#!/bin/sh
echo "setup and run FRAUD PROJECT docker-compose ..."
docker volume create --name docker_fraud
docker network create --subnet 172.55.0.0/16 --gateway 172.55.0.1 mon_reseau
cd ~/Fraud-api/
docker image build . -t fraud_api:1.0.0 -f API/Dockerfile
cd Docker/Performance/
docker image build . -t performance_image:latest
cd ../Prediction/
docker image build . -t prediction_image:latest
cd ../TransactionPrediction/
docker image build . -t transactionprediction_image:latest
cd ..
sudo cp Performance/performance.py /var/lib/docker/volumes/docker_fraud/_data/prediction.py
sudo cp Prediction/prediction.py /var/lib/docker/volumes/docker_fraud/_data/prediction.py
sudo cp TransactionPrediction/transactionPrediction.py /var/lib/docker/volumes/docker_fraud/_data/transactionPrediction.py
docker-compose up
