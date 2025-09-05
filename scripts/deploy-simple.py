#!/usr/bin/env python3

import subprocess
import sys
import time

def run_ssh_command(command):
    """Execute command via SSH"""
    ssh_cmd = f'ssh -p 2012 root@103.9.205.28 "{command}"'
    print(f"🔧 Running: {command}")
    
    try:
        result = subprocess.run(ssh_cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ Success: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e.stderr}")
        return False

def main():
    print("🚀 PHP MySQL Marketplace - Simple Docker Deployment")
    print("=" * 60)
    
    commands = [
        "echo 'Starting deployment...'",
        "rm -rf /tmp/marketplace",
        "git clone https://github.com/datyuno1409/php-mysql-marketplace.git /tmp/marketplace",
        "cd /tmp/marketplace && docker-compose -f docker-compose.prod.yml down",
        "cd /tmp/marketplace && docker-compose -f docker-compose.prod.yml up -d --build",
        "sleep 30",
        "cd /tmp/marketplace && docker-compose -f docker-compose.prod.yml ps"
    ]
    
    for i, command in enumerate(commands, 1):
        print(f"\n📋 Step {i}/{len(commands)}")
        if not run_ssh_command(command):
            print(f"❌ Step {i} failed!")
            sys.exit(1)
    
    print("\n🎉 Deployment completed successfully!")
    print("🔗 Your application is now available at: http://103.9.205.28")
    print("🔗 phpMyAdmin is available at: http://103.9.205.28:8080")

if __name__ == "__main__":
    main()
