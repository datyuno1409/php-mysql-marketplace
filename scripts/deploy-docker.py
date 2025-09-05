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
    result = ssh_command("103.9.205.28", "2012", "root", "echo Connection test")
    if result.returncode != 0:
        print("❌ Cannot connect to server")
        return False
    
    # Check if Docker is installed
    result = ssh_command("103.9.205.28", "2012", "root", "docker --version")
    if result.returncode != 0:
        print("❌ Docker is not installed on server")
        return False
    
    # Check if Docker Compose is installed
    result = ssh_command("103.9.205.28", "2012", "root", "docker-compose --version")
    if result.returncode != 0:
        print("❌ Docker Compose is not installed on server")
        return False
    
    print("✅ All prerequisites met")
    return True

def deploy_application():
    """Deploy the application using Docker Compose"""
    print("🚀 Starting deployment with Docker Compose...")
    
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
        
        # Step 2: Stop existing containers
        print("🛑 Stopping existing containers...")
        ssh_command(server_host, server_port, server_user, 
                   f"cd /tmp/{app_name} && docker-compose -f docker-compose.prod.yml down")
        
        # Step 3: Build and start containers
        print("🐳 Building and starting containers...")
        ssh_command(server_host, server_port, server_user, 
                   f"cd /tmp/{app_name} && docker-compose -f docker-compose.prod.yml up -d --build")
        
        # Step 4: Wait for services to be ready
        print("⏳ Waiting for services to be ready...")
        time.sleep(30)
        
        # Step 5: Check container status
        print("🔍 Checking container status...")
        result = ssh_command(server_host, server_port, server_user, 
                           f"cd /tmp/{app_name} && docker-compose -f docker-compose.prod.yml ps")
        print(result.stdout)
        
        print("✅ Deployment completed successfully!")
        print(f"🔗 Access your application at: http://{server_host}")
        print(f"🔗 Access phpMyAdmin at: http://{server_host}:8080")
        
        return True
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        return False

def test_deployment():
    """Test the deployment"""
    print("🧪 Testing deployment...")
    
    # Check container status
    result = ssh_command("103.9.205.28", "2012", "root", 
                        "cd /tmp/marketplace && docker-compose -f docker-compose.prod.yml ps")
    print("📋 Container status:")
    print(result.stdout)
    
    # Check logs
    result = ssh_command("103.9.205.28", "2012", "root", 
                        "cd /tmp/marketplace && docker-compose -f docker-compose.prod.yml logs --tail=10")
    print("📝 Recent logs:")
    print(result.stdout)
    
    print("✅ Deployment test completed!")

def main():
    print("🚀 PHP MySQL Marketplace - Docker Compose Deployment")
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
    print("🔗 phpMyAdmin is available at: http://103.9.205.28:8080")
    print("📊 Monitor your deployment with: docker-compose -f docker-compose.prod.yml ps")

if __name__ == "__main__":
    main()
