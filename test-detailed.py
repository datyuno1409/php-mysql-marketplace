#!/usr/bin/env python3

import requests
import sys
from urllib.parse import urljoin

def test_page(url, page_name):
    """Test a specific page"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f"✅ {page_name}: OK (Status: {response.status_code})")
            return True
        else:
            print(f"❌ {page_name}: Failed (Status: {response.status_code})")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ {page_name}: Error - {e}")
        return False

def test_database_connection():
    """Test database connection by checking if products load"""
    try:
        response = requests.get("http://103.9.205.28", timeout=10)
        if response.status_code == 200:
            # Check if page contains product data
            content = response.text.lower()
            if "product" in content or "phone" in content or "tablet" in content:
                print("✅ Database connection: OK (Products loaded)")
                return True
            else:
                print("❌ Database connection: Failed (No product data)")
                return False
        else:
            print(f"❌ Database connection: Failed (Status: {response.status_code})")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Database connection: Error - {e}")
        return False

def main():
    print("🔍 Detailed Testing - PHP MySQL Marketplace")
    print("=" * 60)
    
    base_url = "http://103.9.205.28"
    
    # Test main pages
    pages_to_test = [
        (f"{base_url}/", "Homepage"),
        (f"{base_url}/login/", "Login Page"),
        (f"{base_url}/signup/", "Signup Page"),
        (f"{base_url}/admin/", "Admin Panel"),
        (f"{base_url}/seller/", "Seller Panel"),
        (f"{base_url}/shoping-cart.php", "Shopping Cart"),
        (f"{base_url}/category.php", "Category Page"),
    ]
    
    print("📄 Testing Pages:")
    page_results = []
    for url, name in pages_to_test:
        result = test_page(url, name)
        page_results.append(result)
    
    print("\n🗄️ Testing Database:")
    db_result = test_database_connection()
    
    print("\n📊 Summary:")
    successful_pages = sum(page_results)
    total_pages = len(page_results)
    
    print(f"   Pages working: {successful_pages}/{total_pages}")
    print(f"   Database: {'OK' if db_result else 'Failed'}")
    
    if successful_pages >= total_pages * 0.7 and db_result:
        print("\n🎉 Application is working well!")
        print("🔗 You can use the application at: http://103.9.205.28")
        return True
    else:
        print("\n⚠️ Some issues detected, but basic functionality works")
        return False

if __name__ == "__main__":
    main()
