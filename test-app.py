#!/usr/bin/env python3

import requests
import sys

def test_application():
    """Test if application is accessible"""
    print("🧪 Testing PHP MySQL Marketplace Application")
    print("=" * 50)
    
    server_host = "103.9.205.28"
    
    try:
        # Test main application
        print("🌐 Testing main application...")
        response = requests.get(f"http://{server_host}", timeout=10)
        if response.status_code == 200:
            print("✅ Main application is accessible")
            print(f"   Status Code: {response.status_code}")
            print(f"   Content Length: {len(response.content)} bytes")
        else:
            print(f"❌ Main application returned status code: {response.status_code}")
            return False
        
        # Test phpMyAdmin
        print("\n🔧 Testing phpMyAdmin...")
        response = requests.get(f"http://{server_host}:8081", timeout=10)
        if response.status_code == 200:
            print("✅ phpMyAdmin is accessible")
            print(f"   Status Code: {response.status_code}")
        else:
            print(f"❌ phpMyAdmin returned status code: {response.status_code}")
            return False
        
        print("\n🎉 All tests passed!")
        print("🔗 Application URLs:")
        print(f"   Main App: http://{server_host}")
        print(f"   phpMyAdmin: http://{server_host}:8081")
        print(f"   MySQL: {server_host}:3307")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot access application: {e}")
        return False

def main():
    if test_application():
        print("\n✅ Deployment test completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Deployment test failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
