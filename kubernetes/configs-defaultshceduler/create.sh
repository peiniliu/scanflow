sudo /usr/local/bin/kubectl apply -f gathering-deployment.yaml
sudo /usr/local/bin/kubectl apply -f preprocessing-deployment.yaml
sudo /usr/local/bin/kubectl apply -f modeling-deployment.yaml
sudo /usr/local/bin/kubectl apply -f tracker-workflow1-deployment.yaml

#sudo /usr/local/bin/kubectl apply -f getnewdata-deployment.yaml
#sudo /usr/local/bin/kubectl apply -f preprocessingnewdata-deployment.yaml
#sudo /usr/local/bin/kubectl apply -f predictor-deployment.yaml
#sudo /usr/local/bin/kubectl apply -f tracker-workflow2-deployment.yaml

sudo /usr/local/bin/kubectl apply -f tracker-workflow1-service.yaml
#sudo /usr/local/bin/kubectl apply -f tracker-workflow2-service.yaml
#sudo /usr/local/bin/kubectl apply -f predictor-service.yaml
