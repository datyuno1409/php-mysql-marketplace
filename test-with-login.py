#!/usr/bin/env python3

import requests
import sys

def test_login_and_access():
    """Test login and access to protected pages"""
    print("🔐 Testing Login and Access")
    print("=" * 40)
    
    base_url = "http://103.9.205.28"
    session = requests.Session()
    
    # Test credentials from database.sql
    test_credentials = [
        {"username": "serein", "password": "Fpt1409!@", "role": "admin"},
        {"username": "seller", "password": "Fpt1409!@", "role": "seller"},
        {"username": "user", "password": "Fpt1409!@", "role": "user"},
    ]
    
    for cred in test_credentials:
        print(f"\n🔑 Testing login as {cred['username']} ({cred['role']})...")
        
        # Get login page
        login_url = f"{base_url}/login/"
        response = session.get(login_url)
        
        if response.status_code != 200:
            print(f"❌ Cannot access login page: {response.status_code}")
            continue
        
        # Attempt login
        login_data = {
            'username': cred['username'],
            'password': cred['password']
        }
        
        login_response = session.post(login_url, data=login_data, allow_redirects=False)
        
        if login_response.status_code in [200, 302]:
            print(f"✅ Login successful for {cred['username']}")
            
            # Test access to main page
            main_response = session.get(base_url)
            if main_response.status_code == 200:
                print(f"✅ Can access main page as {cred['username']}")
                
                # Check if products are loaded
                content = main_response.text.lower()
                if "product" in content or "phone" in content or "tablet" in content:
                    print(f"✅ Products loaded for {cred['username']}")
                    return True
                else:
                    print(f"⚠️ No product data visible for {cred['username']}")
            else:
                print(f"❌ Cannot access main page: {main_response.status_code}")
        else:
            print(f"❌ Login failed for {cred['username']}: {login_response.status_code}")
    
    return False

def test_public_pages():
    """Test pages that should be accessible without login"""
    print("\n🌐 Testing Public Pages")
    print("=" * 40)
    
    base_url = "http://103.9.205.28"
    
    # These pages should be accessible without login
    public_pages = [
        ("/login/", "Login Page"),
        ("/signup/", "Signup Page"),
    ]
    
    for path, name in public_pages:
        url = base_url + path
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"✅ {name}: Accessible")
            else:
                print(f"❌ {name}: Status {response.status_code}")
        except Exception as e:
            print(f"❌ {name}: Error - {e}")

def main():
    print("🧪 Comprehensive Application Test")
    print("=" * 50)
    
    # Test public pages
    test_public_pages()
    
    # Test login and protected access
    if test_login_and_access():
        print("\n🎉 Application is working correctly!")
        print("🔗 You can access the application at: http://103.9.205.28")
        print("🔑 Login credentials:")
        print("   Admin: serein / Fpt1409!@")
        print("   Seller: seller / Fpt1409!@") 
        print("   User: user / Fpt1409!@")
        return True
    else:
        print("\n⚠️ Some issues detected")
        return False

if __name__ == "__main__":
    main()
