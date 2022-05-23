#!/bin/sh
echo "setup and run FRAUD PROJECT docker-compose ..."
docker volume create --name docker_fraud
docker network create --subnet 172.55.0.0/16 --gateway 172.55.0.1 mon_reseau
cd ~/Fraud-api/
cd performance_image/
docker image build . -t performance_image:latest
cd ../prediction_image/
docker image build . -t prediction_image:latest
cd ../transactionPrediction_image/
docker image build . -t transactionPrediction_image:latest
cd ..
sudo cp performance_image/performance.py /var/lib/docker/volumes/docker_fraud/_data/prediction.py
sudo cp prediction_image/prediction.py /var/lib/docker/volumes/docker_fraud/_data/prediction.py
sudo cp transactionPrediction_image/transactionPrediction.py /var/lib/docker/volumes/docker_fraud/_data/transactionPrediction.py
docker-compose up
