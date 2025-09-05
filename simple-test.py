#!/usr/bin/env python3

import requests

def test_simple():
    print("🌐 Simple Web Test")
    print("=" * 30)
    
    try:
        # Test homepage
        response = requests.get("http://103.9.205.28", timeout=10)
        print(f"Homepage status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Website is accessible")
            print(f"Content length: {len(response.text)} characters")
            
            # Check if it redirects to login
            if "login" in response.text.lower():
                print("ℹ️ Website redirects to login (this is normal)")
                print("🔑 You need to login to see products")
                print("   Username: user")
                print("   Password: Fpt1409!@")
                return True
            else:
                print("✅ Website shows content without login")
                return True
        else:
            print(f"❌ Website not accessible: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    if test_simple():
        print("\n🎉 WEBSITE IS WORKING!")
        print("🔗 Open: http://103.9.205.28")
        print("🔑 Login with: user / Fpt1409!@")
    else:
        print("\n❌ Website has issues")
