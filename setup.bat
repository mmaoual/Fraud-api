echo "setup and run FRAUD PROJECT docker-compose ..."
docker volume create --name docker_fraud
docker network create --subnet 172.55.0.0/16 --gateway 172.55.0.1 mon_reseau
docker image build . -t mmaoual/fraud_api:1.0.0 -f API/Dockerfile
cd Docker/Performance/
docker image build . -t performance_image:latest
cd ../Prediction/
docker image build . -t prediction_image:latest
cd ../TransactionPrediction/
docker image build . -t transactionprediction_image:latest
cd ..
xcopy /y "Performance\performance.py" "\\wsl$\docker-desktop-data\version-pack-data\community\docker\volumes\docker_fraud\_data"
xcopy /y "Prediction\prediction.py" "\\wsl$\docker-desktop-data\version-pack-data\community\docker\volumes\docker_fraud\_data"
xcopy /y "TransactionPrediction\transactionPrediction.py" "\\wsl$\docker-desktop-data\version-pack-data\community\docker\volumes\docker_fraud\_data"

docker-compose up
cd ..