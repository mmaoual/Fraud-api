echo "uninstall docker fraud ..."
cd Docker
docker-compose down
del /f "\\wsl$\docker-desktop-data\version-pack-data\community\docker\volumes\docker_fraud\_data\performance.py"
del /f "\\wsl$\docker-desktop-data\version-pack-data\community\docker\volumes\docker_fraud\_data\prediction.py"
del /f "\\wsl$\docker-desktop-data\version-pack-data\community\docker\volumes\docker_fraud\_data\transactionPrediction.py"
docker volume rm docker_fraud
docker network rm mon_reseau
docker image rm -f performance_image:latest
docker image rm -f prediction_image:latest
docker image rm -f transactionprediction_image:latest
docker image rm -f mmaoual/fraud_api:1.0.0
cd ..
echo "uninstall done."