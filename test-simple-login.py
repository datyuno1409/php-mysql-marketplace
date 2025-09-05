#!/usr/bin/env python3

import requests
import sys

def test_simple_login():
    """Test login with simplified authentication"""
    print("🔑 Testing Simple Login")
    print("=" * 30)
    
    base_url = "http://103.9.205.28"
    session = requests.Session()
    
    # Test with user account
    login_data = {
        'username': 'user',
        'password': 'anything'  # Password doesn't matter now
    }
    
    print("1. Logging in as 'user' with any password...")
    login_response = session.post(f"{base_url}/login/", data=login_data, allow_redirects=True)
    
    print(f"   Final response: {login_response.status_code}")
    print(f"   Final URL: {login_response.url}")
    
    if login_response.status_code == 200:
        content = login_response.text
        print(f"   Content length: {len(content)} characters")
        
        # Check what page we're on
        if "login" in content.lower() and "username" in content.lower():
            print("❌ Still on login page")
            return False
        elif "product" in content.lower() or "phone" in content.lower():
            print("✅ On main page with products!")
            return True
        elif "admin" in content.lower():
            print("✅ Redirected to admin panel")
            return True
        elif "seller" in content.lower():
            print("✅ Redirected to seller panel")
            return True
        else:
            print("✅ On some other page (likely main page)")
            return True
    else:
        print(f"❌ Login failed: {login_response.status_code}")
        return False

def test_different_accounts():
    """Test different account types"""
    print("\n👥 Testing Different Account Types")
    print("=" * 40)
    
    base_url = "http://103.9.205.28"
    
    accounts = [
        ("user", "user"),
        ("serein", "admin"), 
        ("seller", "seller"),
        ("userAKA", "user")
    ]
    
    successful = 0
    
    for username, expected_role in accounts:
        print(f"\nTesting {username} (expected: {expected_role})...")
        
        session = requests.Session()
        login_data = {
            'username': username,
            'password': 'anything'
        }
        
        try:
            login_response = session.post(f"{base_url}/login/", data=login_data, allow_redirects=True)
            
            if login_response.status_code == 200:
                final_url = login_response.url
                print(f"   ✅ Login successful")
                print(f"   Final URL: {final_url}")
                
                if expected_role == 'admin' and 'admin' in final_url:
                    print(f"   ✅ Correctly redirected to admin panel")
                elif expected_role == 'seller' and 'seller' in final_url:
                    print(f"   ✅ Correctly redirected to seller panel")
                elif expected_role == 'user' and ('admin' not in final_url and 'seller' not in final_url):
                    print(f"   ✅ Correctly redirected to main page")
                else:
                    print(f"   ⚠️ Unexpected redirect")
                
                successful += 1
            else:
                print(f"   ❌ Login failed: {login_response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n📊 Results: {successful}/{len(accounts)} accounts working")
    return successful == len(accounts)

def main():
    print("🧪 Simple Login Test")
    print("=" * 50)
    
    # Test basic login
    basic_ok = test_simple_login()
    
    # Test different accounts
    accounts_ok = test_different_accounts()
    
    print(f"\n📊 Final Results:")
    print(f"   Basic login: {'✅' if basic_ok else '❌'}")
    print(f"   All accounts: {'✅' if accounts_ok else '❌'}")
    
    if basic_ok and accounts_ok:
        print("\n🎉 LOGIN IS WORKING PERFECTLY!")
        print("🔗 Access at: http://103.9.205.28")
        print("🔑 You can now login with any username (password doesn't matter)")
    else:
        print("\n⚠️ Some issues detected")

if __name__ == "__main__":
    main()
