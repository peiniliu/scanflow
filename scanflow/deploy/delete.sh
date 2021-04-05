sudo /usr/local/bin/kubectl delete -f gathering-deployment.yaml
sudo /usr/local/bin/kubectl delete -f preprocessing-deployment.yaml
sudo /usr/local/bin/kubectl delete -f modeling-deployment.yaml
sudo /usr/local/bin/kubectl delete -f tracker-workflow1-deployment.yaml

sudo /usr/local/bin/kubectl delete -f getnewdata-deployment.yaml
sudo /usr/local/bin/kubectl delete -f preprocessingnewdata-deployment.yaml
sudo /usr/local/bin/kubectl delete -f predictor-deployment.yaml
sudo /usr/local/bin/kubectl delete -f tracker-workflow2-deployment.yaml
