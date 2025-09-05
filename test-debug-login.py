#!/usr/bin/env python3

import requests
import sys

def test_debug_login():
    """Test debug login with POST request"""
    print("🔍 Testing Debug Login")
    print("=" * 25)
    
    base_url = "http://103.9.205.28"
    session = requests.Session()
    
    # Test POST request
    login_data = {
        'username': 'user',
        'password': 'anything'
    }
    
    print("1. Sending POST request to debug-login.php...")
    response = session.post(f"{base_url}/debug-login.php", data=login_data, allow_redirects=False)
    
    print(f"   Response status: {response.status_code}")
    print(f"   Response headers:")
    for key, value in response.headers.items():
        if 'location' in key.lower() or 'set-cookie' in key.lower():
            print(f"     {key}: {value}")
    
    if response.status_code == 302:
        redirect_url = response.headers.get('Location', '')
        print(f"   Redirect URL: {redirect_url}")
        
        # Follow redirect
        if redirect_url.startswith('/'):
            redirect_url = base_url + redirect_url
        
        print(f"   Following redirect to: {redirect_url}")
        main_response = session.get(redirect_url)
        print(f"   Final response: {main_response.status_code}")
        print(f"   Final URL: {main_response.url}")
        
        if main_response.status_code == 200:
            content = main_response.text
            print(f"   Content length: {len(content)} characters")
            
            if "login" in content.lower() and "username" in content.lower():
                print("   ❌ Still on login page after redirect")
                return False
            elif "product" in content.lower() or "phone" in content.lower():
                print("   ✅ On main page with products!")
                return True
            else:
                print("   ✅ On some other page (likely main page)")
                return True
        else:
            print(f"   ❌ Cannot access redirected page: {main_response.status_code}")
            return False
    else:
        print(f"   ❌ No redirect (status: {response.status_code})")
        print(f"   Response content: {response.text[:200]}...")
        return False

def main():
    print("🧪 Debug Login Test")
    print("=" * 50)
    
    success = test_debug_login()
    
    if success:
        print("\n🎉 DEBUG LOGIN IS WORKING!")
        print("🔗 The issue might be in the original login code")
    else:
        print("\n❌ DEBUG LOGIN NOT WORKING")
        print("🔍 Need to investigate further")

if __name__ == "__main__":
    main()
