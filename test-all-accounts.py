#!/usr/bin/env python3

import requests
import sys

def test_account(username, password, role):
    """Test a specific account"""
    print(f"\n🔑 Testing {username} ({role})...")
    
    base_url = "http://103.9.205.28"
    session = requests.Session()
    
    # Test login
    login_data = {
        'username': username,
        'password': password
    }
    
    try:
        login_response = session.post(f"{base_url}/login/", data=login_data, allow_redirects=False)
        
        if login_response.status_code in [200, 302]:
            print(f"✅ Login successful for {username}")
            
            # Check if redirected
            if login_response.status_code == 302:
                redirect_url = login_response.headers.get('Location', '')
                print(f"   Redirected to: {redirect_url}")
                
                # Follow redirect
                if redirect_url.startswith('/'):
                    redirect_url = base_url + redirect_url
                
                main_response = session.get(redirect_url)
                if main_response.status_code == 200:
                    print(f"✅ Can access main page as {username}")
                    return True
                else:
                    print(f"❌ Cannot access main page: {main_response.status_code}")
                    return False
            else:
                print(f"✅ Login page shows success for {username}")
                return True
        else:
            print(f"❌ Login failed for {username}: {login_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing {username}: {e}")
        return False

def main():
    print("🧪 Testing All Accounts")
    print("=" * 50)
    
    accounts = [
        ("serein", "Fpt1409!@", "admin"),
        ("seller", "Fpt1409!@", "seller"),
        ("user", "Fpt1409!@", "user"),
        ("userAKA", "Fpt1409!@", "user"),
    ]
    
    successful = 0
    total = len(accounts)
    
    for username, password, role in accounts:
        if test_account(username, password, role):
            successful += 1
    
    print(f"\n📊 Results: {successful}/{total} accounts working")
    
    if successful == total:
        print("🎉 ALL ACCOUNTS ARE WORKING!")
        print("🔗 Try logging in at: http://103.9.205.28")
    elif successful > 0:
        print("⚠️ Some accounts are working")
    else:
        print("❌ No accounts are working")

if __name__ == "__main__":
    main()
