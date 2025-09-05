#!/usr/bin/env python3

import requests
import sys

def test_login_redirect():
    """Test login redirect with detailed debugging"""
    print("🔄 Testing Login Redirect")
    print("=" * 30)
    
    base_url = "http://103.9.205.28"
    session = requests.Session()
    
    # Test with user account
    login_data = {
        'username': 'user',
        'password': 'anything'
    }
    
    print("1. Logging in as 'user'...")
    login_response = session.post(f"{base_url}/login/", data=login_data, allow_redirects=False)
    
    print(f"   Response status: {login_response.status_code}")
    print(f"   Response headers:")
    for key, value in login_response.headers.items():
        if 'location' in key.lower() or 'set-cookie' in key.lower():
            print(f"     {key}: {value}")
    
    if login_response.status_code == 302:
        redirect_url = login_response.headers.get('Location', '')
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
        print(f"   ❌ No redirect (status: {login_response.status_code})")
        return False

def test_direct_main_page():
    """Test direct access to main page"""
    print("\n🌐 Testing Direct Main Page Access")
    print("=" * 40)
    
    base_url = "http://103.9.205.28"
    
    try:
        response = requests.get(base_url, allow_redirects=True)
        print(f"Main page response: {response.status_code}")
        print(f"Final URL: {response.url}")
        
        if response.status_code == 200:
            content = response.text
            print(f"Content length: {len(content)} characters")
            
            if "login" in content.lower():
                print("ℹ️ Redirected to login (normal behavior)")
                return True
            else:
                print("✅ Direct access to main page")
                return True
        else:
            print(f"❌ Cannot access main page: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🧪 Login Redirect Test")
    print("=" * 50)
    
    # Test direct access
    direct_ok = test_direct_main_page()
    
    # Test login redirect
    redirect_ok = test_login_redirect()
    
    print(f"\n📊 Results:")
    print(f"   Direct access: {'✅' if direct_ok else '❌'}")
    print(f"   Login redirect: {'✅' if redirect_ok else '❌'}")
    
    if direct_ok and redirect_ok:
        print("\n🎉 LOGIN AND REDIRECT ARE WORKING!")
        print("🔗 Access at: http://103.9.205.28")
    else:
        print("\n⚠️ Some issues detected")

if __name__ == "__main__":
    main()
