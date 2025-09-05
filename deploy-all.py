#!/usr/bin/env python3

import subprocess
import sys
import time
import os

def run_command(command, check=True):
    """Run a command and return the result"""
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running command: {command}")
        print(f"Error: {e.stderr}")
        if check:
            sys.exit(1)
        return e

def ssh_command(host, port, user, command):
    """Execute command via SSH"""
    ssh_cmd = f"ssh -p {port} {user}@{host} '{command}'"
    return run_command(ssh_cmd)

def check_prerequisites():
    """Check if all prerequisites are met"""
    print("🔍 Checking prerequisites...")
    
    # Check if we can connect to server
    result = ssh_command("103.9.205.28", "2012", "root", "echo 'Connection test'")
    if result.returncode != 0:
        print("❌ Cannot connect to server")
        return False
    
    # Check if Docker is installed
    result = ssh_command("103.9.205.28", "2012", "root", "docker --version")
    if result.returncode != 0:
        print("❌ Docker is not installed on server")
        return False
    
    # Check if kubectl is available
    result = ssh_command("103.9.205.28", "2012", "root", "kubectl version --client")
    if result.returncode != 0:
        print("❌ kubectl is not available on server")
        return False
    
    print("✅ All prerequisites met")
    return True

def deploy_application():
    """Deploy the application"""
    print("🚀 Starting deployment...")
    
    server_host = "103.9.205.28"
    server_port = "2012"
    server_user = "root"
    repo_url = "https://github.com/datyuno1409/php-mysql-marketplace.git"
    app_name = "marketplace"
    
    try:
        # Step 1: Clone repository
        print("📦 Cloning repository on server...")
        ssh_command(server_host, server_port, server_user, 
                   f"rm -rf /tmp/{app_name} && git clone {repo_url} /tmp/{app_name}")
        
        # Step 2: Build Docker image
        print("🐳 Building Docker image...")
        ssh_command(server_host, server_port, server_user, 
                   f"cd /tmp/{app_name} && docker build -t {app_name}-php:latest .")
        
        # Step 3: Apply Kubernetes manifests
        print("📋 Applying Kubernetes manifests...")
        ssh_command(server_host, server_port, server_user, 
                   f"cd /tmp/{app_name} && kubectl apply -f k8s/")
        
        # Step 4: Wait for deployments
        print("⏳ Waiting for deployments to be ready...")
        deployments = ["mysql-deployment", "php-deployment", "nginx-deployment"]
        
        for deployment in deployments:
            print(f"   Waiting for {deployment}...")
            ssh_command(server_host, server_port, server_user, 
                       f"kubectl wait --for=condition=available --timeout=300s deployment/{deployment} -n marketplace")
        
        # Step 5: Get service information
        print("🌐 Getting service information...")
        result = ssh_command(server_host, server_port, server_user, 
                           "kubectl get services -n marketplace")
        print(result.stdout)
        
        print("✅ Deployment completed successfully!")
        print(f"🔗 Access your application at: http://{server_host}")
        
        return True
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        return False

def test_deployment():
    """Test the deployment"""
    print("🧪 Testing deployment...")
    
    # Check pods status
    result = ssh_command("103.9.205.28", "2012", "root", 
                        "kubectl get pods -n marketplace")
    print("📋 Pod status:")
    print(result.stdout)
    
    # Check services
    result = ssh_command("103.9.205.28", "2012", "root", 
                        "kubectl get services -n marketplace")
    print("🌐 Service status:")
    print(result.stdout)
    
    print("✅ Deployment test completed!")

def main():
    print("🚀 PHP MySQL Marketplace - Complete Deployment")
    print("=" * 60)
    
    # Check prerequisites
    if not check_prerequisites():
        print("❌ Prerequisites check failed")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    
    # Deploy application
    if not deploy_application():
        print("❌ Deployment failed")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    
    # Test deployment
    test_deployment()
    
    print("\n🎉 Deployment completed successfully!")
    print("🔗 Your application is now available at: http://103.9.205.28")
    print("📊 Monitor your deployment with: kubectl get pods -n marketplace")

if __name__ == "__main__":
    main()
