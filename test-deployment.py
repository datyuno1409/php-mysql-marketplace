#!/usr/bin/env python3

import subprocess
import sys
import time
import requests

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

def test_kubernetes_deployment():
    """Test Kubernetes deployment status"""
    print("🔍 Testing Kubernetes deployment...")
    
    server_host = "103.9.205.28"
    server_port = "2012"
    server_user = "root"
    
    # Check namespace
    result = ssh_command(server_host, server_port, server_user, 
                        "kubectl get namespace marketplace")
    if "marketplace" in result.stdout:
        print("✅ Namespace 'marketplace' exists")
    else:
        print("❌ Namespace 'marketplace' not found")
        return False
    
    # Check pods
    result = ssh_command(server_host, server_port, server_user, 
                        "kubectl get pods -n marketplace")
    print("📋 Pod status:")
    print(result.stdout)
    
    # Check services
    result = ssh_command(server_host, server_port, server_user, 
                        "kubectl get services -n marketplace")
    print("🌐 Service status:")
    print(result.stdout)
    
    return True

def test_application_access():
    """Test if application is accessible"""
    print("🌐 Testing application access...")
    
    server_host = "103.9.205.28"
    
    try:
        response = requests.get(f"http://{server_host}", timeout=10)
        if response.status_code == 200:
            print("✅ Application is accessible")
            return True
        else:
            print(f"❌ Application returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot access application: {e}")
        return False

def main():
    print("🧪 Testing PHP MySQL Marketplace Deployment")
    print("=" * 50)
    
    # Test Kubernetes deployment
    if not test_kubernetes_deployment():
        print("❌ Kubernetes deployment test failed")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    
    # Test application access
    if not test_application_access():
        print("❌ Application access test failed")
        sys.exit(1)
    
    print("\n✅ All tests passed! Deployment is successful.")
    print("🔗 Access your application at: http://103.9.205.28")

if __name__ == "__main__":
    main()
