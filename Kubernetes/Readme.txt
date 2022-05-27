# TEST & EXECUTION

# console 1 :
minikube start
minikube dashboard --url=true
# on peut fermer la console 1 après

# console 2 :
kubectl proxy --address='0.0.0.0' --disable-filter=true

# console 3 :
kubectl create -f my-deployment-fraud.yml
kubectl get deployment

# si necessaire
kubectl delete deployment my-deployment-fraud

kubectl create -f my-service-fraud.yml
kubectl get service

# si necessaire
kubect delete service my-fraud-service

kubectl create -f my-ingress-fraud.yml
kubectl get ingress

console windows cmd : 
# pont avec la machine locale
ssh -i "data_enginering_machine.pem" ubuntu@<ip machine> -fNL 8000:192.168.49.2:80

# acces api via navigateur
http://localhost:8000/docs