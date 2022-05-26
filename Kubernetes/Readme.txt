kubectl create -f my-deployment-fraud.yml
kubectl get deployment

# si necessaire
kubect delete deployments my-fraud-deployment

kubectl create -f my-service-fraud.yml
kubectl get deployment

# si necessaire
kubect delete service my-fraud-service

kubectl create -f my-ingress-fraud.yml
kubectl get ingress

# console 1 :
minikube start
minikube dashboard --url=true
# on peut fermer la console 1 après


# console 2 :
kubectl proxy --address='0.0.0.0' --disable-filter=true

# http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/http:kubernetes-dashboard:/proxy/#/pod?namespace=default
# http://localhost:8001/api/v1/namespaces/default/services/my-fraud-service/proxy/
# http://localhost:8001/api/v1/namespaces/default/services/my-fraud-service/proxy/performance?model=log