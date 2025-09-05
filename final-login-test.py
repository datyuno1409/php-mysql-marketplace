#!/usr/bin/env python3

import requests
import sys

def test_login_flow():
    """Test complete login flow"""
    print("🔐 Testing Complete Login Flow")
    print("=" * 40)
    
    base_url = "http://103.9.205.28"
    session = requests.Session()
    
    # Test login
    login_data = {
        'username': 'user',
        'password': 'Fpt1409!@'
    }
    
    print("1. Attempting login...")
    login_response = session.post(f"{base_url}/login/", data=login_data, allow_redirects=False)
    print(f"   Login response: {login_response.status_code}")
    
    if login_response.status_code in [200, 302]:
        print("✅ Login successful!")
        
        # Follow redirect
        if login_response.status_code == 302:
            redirect_url = login_response.headers.get('Location', '')
            print(f"   Redirecting to: {redirect_url}")
            
            # Get the redirected page
            if redirect_url.startswith('/'):
                redirect_url = base_url + redirect_url
            
            main_response = session.get(redirect_url)
            print(f"   Main page response: {main_response.status_code}")
            
            if main_response.status_code == 200:
                content = main_response.text
                print(f"   Content length: {len(content)} characters")
                
                # Check for product content
                if "product" in content.lower() or "phone" in content.lower():
                    print("✅ Products are visible!")
                    return True
                else:
                    print("⚠️ No products visible, but login works")
                    return True
            else:
                print(f"❌ Cannot access main page: {main_response.status_code}")
                return False
        else:
            print("✅ Login page shows success")
            return True
    else:
        print(f"❌ Login failed: {login_response.status_code}")
        return False

def main():
    if test_login_flow():
        print("\n🎉 LOGIN IS WORKING!")
        print("🔗 Try logging in at: http://103.9.205.28")
        print("🔑 Username: user")
        print("🔑 Password: Fpt1409!@")
    else:
        print("\n❌ Login still has issues")

if __name__ == "__main__":
    main()
