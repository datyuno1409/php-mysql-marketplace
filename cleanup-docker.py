#!/usr/bin/env python3

import subprocess
import sys

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

def cleanup_deployment():
    """Clean up the Docker deployment"""
    print("🧹 Cleaning up Docker deployment...")
    
    server_host = "103.9.205.28"
    server_port = "2012"
    server_user = "root"
    
    try:
        # Stop and remove containers
        print("🛑 Stopping and removing containers...")
        ssh_command(server_host, server_port, server_user, 
                   "cd /tmp/marketplace && docker-compose -f docker-compose.prod.yml down")
        
        # Remove images
        print("🗑️ Removing images...")
        ssh_command(server_host, server_port, server_user, 
                   "docker rmi marketplace-php:latest || true")
        
        # Remove volumes
        print("🗑️ Removing volumes...")
        ssh_command(server_host, server_port, server_user, 
                   "docker volume rm marketplace_mysql_data_prod || true")
        
        # Clean up repository
        print("🗑️ Cleaning up repository...")
        ssh_command(server_host, server_port, server_user, 
                   "rm -rf /tmp/marketplace")
        
        print("✅ Cleanup completed successfully!")
        
    except Exception as e:
        print(f"❌ Cleanup failed: {e}")
        return False
    
    return True

def main():
    print("🧹 PHP MySQL Marketplace - Docker Cleanup")
    print("=" * 50)
    
    if cleanup_deployment():
        print("🎉 Cleanup completed successfully!")
    else:
        print("❌ Cleanup failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
