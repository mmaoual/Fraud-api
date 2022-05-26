#!/bin/sh
echo "uninstall docker fraud ..."
cd ~/Fraud-api/
docker-compose down
sudo rm -f /var/lib/docker/volumes/docker_fraud/_data/performance.py
sudo rm -f /var/lib/docker/volumes/docker_fraud/_data/prediction.py
sudo rm -f /var/lib/docker/volumes/docker_fraud/_data/transactionPrediction.py
sudo rm -f /var/lib/docker/volumes/docker_fraud/_data/app_test.log
docker volume rm docker_fraud
docker network rm mon_reseau
docker image rm -f performance_image:latest
docker image rm -f prediction_image:latest
docker image rm -f transactionprediction_image:latest
docker image rm -f fraud_api:1.0.0
echo "uninstall done."
