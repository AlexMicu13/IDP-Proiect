For starting the services in Azure, you should follow the steps below:
1. Download the Azure CLI
2. For Windows:
`az login
terraform init -upgrade
terraform plan -out main.tfplan
terraform apply main.tfplan
$resource_group_name = terraform output -raw resource_group_name
az aks list --resource-group $resource_group_name --query "[].name" --output table
$(terraform output kube_config) | Out-File -FilePath ./azurek8s -Force
// Delete the EOT from the azurek8s file
az aks get-credentials --resource-group $resource_group_name --name <cluster_name>
$env:KUBECONFIG="./azurek8s"`

For Unix:
`az login
terraform init -upgrade
terraform plan -out main.tfplan
terraform apply main.tfplan
resource_group_name=$(terraform output -raw resource_group_name)
az aks list --resource-group $resource_group_name --query "[].name" --output table
$(terraform output kube_config) > ./azurek8s
// Delete the EOT from the azurek8s file
az aks get-credentials --resource-group $resource_group_name --name <cluster_name>
export KUBECONFIG=./azurek8s`

3. Run the commands from below:
`kubectl apply -f ../manifests/namespaces.yaml
kubectl apply -f ../manifests/persistent-volume.yaml
kubectl apply -f ../manifests/pvc.yaml
kubectl apply -f ../manifests/clusterrole.yaml
kubectl apply -f ../manifests/clusterrolebinding.yaml
kubectl apply -f ../manifests/deploy.yaml
kubectl apply -f ../manifests/initdb.yaml
kubectl apply -f ../manifests/datasource.yaml
kubectl apply -f ../manifests/dashboardconfig.yaml
kubectl apply -f ../manifests/dashboards.yaml
kubectl apply -f ../manifests/kube.yaml
kubectl apply -f ../manifests/services.yaml
kubectl apply -f ../manifests/ingress.yaml // for this command you need to wait for the external ip to be available
kubectl apply -f ../manifests/network-policies.yaml`

4. Run `kubectl get service -n ingress-nginx ingress-nginx-controller -o wide` to get the ip and hosts.

5. If wished to test with postman, you should add the hosts on your hosts configuration file then you are good to go. 
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

To close the services in Azure, you should follow the steps below:
6. `terraform plan -destroy -out main.destroy.tfplan
terraform apply main.destroy.tfplan`

