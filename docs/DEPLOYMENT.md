# 🚀 PHP MySQL Marketplace - Deployment Guide

## 📋 Overview

This guide will help you deploy the PHP MySQL Marketplace application to your server using Docker and Kubernetes.

## 🛠 Prerequisites

- Server with SSH access (103.9.205.28:2012)
- Docker installed on the server
- Kubernetes cluster running on the server
- kubectl configured
- Git installed on the server

## 🚀 Quick Deployment

### Option 1: Using Python Script (Recommended)

```bash
python3 deploy.py
```

### Option 2: Using Bash Script

```bash
chmod +x deploy.sh
./deploy.sh
```

### Option 3: Manual Deployment

1. **Clone the repository on your server:**
```bash
ssh -p 2012 root@103.9.205.28 "git clone https://github.com/datyuno1409/php-mysql-marketplace.git /tmp/marketplace"
```

2. **Build the Docker image:**
```bash
ssh -p 2012 root@103.9.205.28 "cd /tmp/marketplace && docker build -t marketplace-php:latest ."
```

3. **Apply Kubernetes manifests:**
```bash
ssh -p 2012 root@103.9.205.28 "cd /tmp/marketplace && kubectl apply -f k8s/"
```

4. **Wait for deployments to be ready:**
```bash
ssh -p 2012 root@103.9.205.28 "kubectl wait --for=condition=available --timeout=300s deployment/mysql-deployment -n marketplace"
ssh -p 2012 root@103.9.205.28 "kubectl wait --for=condition=available --timeout=300s deployment/php-deployment -n marketplace"
ssh -p 2012 root@103.9.205.28 "kubectl wait --for=condition=available --timeout=300s deployment/nginx-deployment -n marketplace"
```

## 🏗 Architecture

The application is deployed with the following components:

- **Nginx**: Web server and reverse proxy
- **PHP-FPM**: Application server
- **MySQL**: Database server
- **Persistent Volumes**: For data storage

## 📁 Kubernetes Manifests

All Kubernetes manifests are located in the `k8s/` directory:

- `namespace.yaml` - Creates the marketplace namespace
- `configmap.yaml` - Application configuration
- `mysql-deployment.yaml` - MySQL database deployment
- `php-deployment.yaml` - PHP application deployment
- `nginx-deployment.yaml` - Nginx web server deployment
- `ingress.yaml` - Ingress configuration
- `kustomization.yaml` - Kustomize configuration

## 🔧 Configuration

The application uses environment variables for configuration:

- `DB_HOST`: Database host (default: mysql-service)
- `DB_NAME`: Database name (default: marketplace)
- `DB_USER`: Database user (default: callmeserein)
- `DB_PASSWORD`: Database password (default: Fpt1409!@)

## 🌐 Access

After deployment, the application will be available at:
- **HTTP**: http://103.9.205.28

## 🔍 Monitoring

Check the status of your deployment:

```bash
# Check pods
kubectl get pods -n marketplace

# Check services
kubectl get services -n marketplace

# Check logs
kubectl logs -f deployment/nginx-deployment -n marketplace
kubectl logs -f deployment/php-deployment -n marketplace
kubectl logs -f deployment/mysql-deployment -n marketplace
```

## 🧹 Cleanup

To remove the deployment:

```bash
kubectl delete namespace marketplace
```

Or use the cleanup script:

```bash
chmod +x k8s/cleanup.sh
./k8s/cleanup.sh
```

## 🔄 Updates

To update the application:

1. Push changes to the repository
2. Run the deployment script again
3. The script will rebuild the Docker image and update the deployment

## 🐛 Troubleshooting

### Common Issues

1. **Database connection issues**: Check if MySQL pod is running and accessible
2. **Image pull errors**: Ensure Docker image is built and available
3. **Service not accessible**: Check LoadBalancer service status and external IP

### Debug Commands

```bash
# Check pod status
kubectl describe pod <pod-name> -n marketplace

# Check service endpoints
kubectl get endpoints -n marketplace

# Check persistent volumes
kubectl get pv,pvc -n marketplace
```

## 📝 Notes

- The application uses persistent volumes for data storage
- Database initialization is handled automatically via ConfigMap
- The deployment includes 2 replicas for both PHP and Nginx for high availability
- All sensitive data should be moved to Kubernetes Secrets in production
