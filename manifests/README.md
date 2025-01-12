For running all the services into a kubernetes container using minikube:
1. Download minikube package through terminal
2. For first use
`minikube start // If you have minikube
kind create cluster –config kind-config.yaml // If you have kind
kubectl apply -f manifests/namespaces.yaml
kubectl apply -f manifests/persistent-volume.yaml
kubectl apply -f manifests/pvc.yaml
kubectl apply -f manifests/clusterrole.yaml
kubectl apply -f manifests/clusterrolebinding.yaml
kubectl apply -f manifests/deploy.yaml
kubectl apply -f manifests/initdb.yaml
kubectl apply -f manifests/datasource.yaml
kubectl apply -f manifests/dashboardconfig.yaml
kubectl apply -f manifests/dashboards.yaml
kubectl apply -f manifests/kube.yaml
kubectl apply -f manifests/services.yaml
kubectl apply -f manifests/ingress.yaml // for this command you need to wait for the external ip to be available
kubectl apply -f manifests/network-policies.yaml`
3. Run `kubectl get service -n ingress-nginx ingress-nginx-controller -o wide` to get the ip and hosts.
4. If wished to test with postman, you should add the hosts on your hosts configuration file then you are good to go. 
For Windows:
`notepad C:\Windows\System32\drivers\etc\hosts` as administrator
For Unix:
`sudo nano /etc/hosts`

Example:
`135.237.11.203 auth-reservation-app.com
135.237.11.203 backend-reservation-app.com
135.237.11.203 grafana-reservation-app.com
135.237.11.203 pgadmin-reservation-app.com
135.237.11.203 portainer-reservation-app.com`