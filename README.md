# Python_infra
# Python Service Monitoring URLs with Prometheus Metrics

This project is a Python-based service that monitors the HTTP status and response time of a set of URLs. It exposes the monitoring data as Prometheus-compatible metrics, which can be scraped by a Prometheus server.

## Prerequisites

- Docker
- Kubernetes (K8s) cluster
- Helm 3.x installed
- Prometheus instance running in your Kubernetes cluster (for scraping metrics)
- kubectl configured to access your cluster

## Steps to Run the Python Service on Kubernetes

Follow the steps below to deploy this service in a Kubernetes cluster.

### Step 1: Clone this repository

Clone the repository to your local machine:
```bash
git clone <your-repository-url>
cd <repository-directory>

### Step 2: Create Docker Image
1. Create a Dockerfile:
Dockerfile to containerize the Python application can be found within the project

2. Build the Docker image:
docker build -t python-prometheus .

3. (Optional) Push the image to a container registry:


### Step 3: Deploy to Kubernetes using Helm

1. Install Helm (if not installed already):
curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash

2. Create a Helm chart for the deployment:
helm create python-prometheus
cd python-prometheus

3. Modify the Helm chart files: 
** in values.yaml , update the image.repository and image.tag to point to your Docker image: **

4. Expose port 8000: 
**In templates/deployment.yaml, ensure the container exposes port 8000: **

5. Create a Service:
** In templates/service.yaml, define a service to expose port 8000 for Prometheus scraping: **

6. helm install python-prometheus ./python-prometheus
helm install python-url-monitor ./python-url-monitor

7. Verify the deployment: Check if the pods and services are running:
kubectl get pods
kubectl get svc


### Step 4: Accessing Metrics
http://<service-ip>:8000/metrics

### Step 5: Troubleshooting
If the service is not running correctly, check the logs of the pods:
kubectl logs <pod-name>

To debug the service, you can access the pod's shell:
kubectl exec -it <pod-name> -- /bin/bash

### Step 6: Docker and Helm Chart Details
* The Dockerfile provided is used to containerize the Python application.
* You can create the Helm chart by running: helm create python-prometheus

This generates the following structure:
python-prometheus/
├── Chart.yaml
├── values.yaml
├── charts/
├── templates/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ...

We should use deployment.yaml, values.yaml and service yaml from templates folder to adjust the ones created within the chart structure.

Once your Helm chart is modified, you can deploy it to your Kubernetes cluster by running:
helm install python-url-monitor ./python-url-monitor

Then, check if everything is running correctly:
kubectl get pods
kubectl get svc

------------------------
This README file now contains all the necessary information to build and deploy your Python app on a Kubernetes cluster, including Docker and Helm instructions.