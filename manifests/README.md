For running all the services into a kubernetes container using minikube:
1. Download minikube package through terminal
2. Run `minikube start`
3. Run `kubectl apply -f manifests/pvc.yaml`
4. Run `kubectl apply -f manifests/persistent-volume.yaml`
5. Run `kubectl apply -f manifests/clusterrole.yaml`
6. Run `kubectl apply -f manifests/clusterrolebinding.yaml`
7. Run `kubectl apply -f manifests/kube.yaml` to create or apply (if already ran this command previously) changes of the kube.yaml file
8. Run `minikube service python-api-service` to run the services and get their running ports
9. If wished to test with postman, you should change the ports and ips of the backend and auth services in the tests