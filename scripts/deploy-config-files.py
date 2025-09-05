#!/usr/bin/env python3
import os
import shutil
import subprocess
import sys

def deploy_files():
    """Deploy configuration files to server"""
    print("🚀 Deploying configuration files...")
    
    # Files to deploy
    files_to_deploy = [
        {
            'local': 'config.php',
            'remote': '/home/callmeserein/marketplace/config.php',
            'container_path': '/var/www/html/config.php',
            'container': 'marketplace-php-prod'
        },
        {
            'local': 'nginx.prod.conf',
            'remote': '/home/callmeserein/marketplace/nginx.prod.conf',
            'container_path': '/etc/nginx/conf.d/default.conf',
            'container': 'marketplace-nginx-prod'
        }
    ]
    
    server_ip = "103.9.205.28"
    username = "callmeserein"
    password = "Next-Step@2310"
    
    success_count = 0
    
    for file_info in files_to_deploy:
        print(f"\n📁 Deploying {file_info['local']}...")
        
        # Check if local file exists
        if not os.path.exists(file_info['local']):
            print(f"❌ Local file {file_info['local']} not found")
            continue
            
        try:
            # Try using pscp to upload file
            pscp_cmd = [
                'pscp', '-pw', password,
                file_info['local'],
                f"{username}@{server_ip}:{file_info['remote']}"
            ]
            
            print(f"Uploading {file_info['local']} to server...")
            result = subprocess.run(pscp_cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print(f"✅ Successfully uploaded {file_info['local']}")
                
                # Now copy to container
                docker_cmd = [
                    'plink', '-ssh', f"{username}@{server_ip}", '-pw', password,
                    f"docker cp {file_info['remote']} {file_info['container']}:{file_info['container_path']}"
                ]
                
                print(f"Copying to container {file_info['container']}...")
                docker_result = subprocess.run(docker_cmd, capture_output=True, text=True, timeout=30)
                
                if docker_result.returncode == 0:
                    print(f"✅ Successfully deployed to container")
                    success_count += 1
                    
                    # Restart container if it's nginx
                    if 'nginx' in file_info['container']:
                        restart_cmd = [
                            'plink', '-ssh', f"{username}@{server_ip}", '-pw', password,
                            f"docker exec {file_info['container']} nginx -s reload"
                        ]
                        
                        print(f"Reloading nginx configuration...")
                        restart_result = subprocess.run(restart_cmd, capture_output=True, text=True, timeout=30)
                        
                        if restart_result.returncode == 0:
                            print(f"✅ Nginx configuration reloaded")
                        else:
                            print(f"⚠️ Failed to reload nginx: {restart_result.stderr}")
                            
                else:
                    print(f"❌ Failed to copy to container: {docker_result.stderr}")
                    
            else:
                print(f"❌ Failed to upload file: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print(f"❌ Timeout while deploying {file_info['local']}")
        except Exception as e:
            print(f"❌ Error deploying {file_info['local']}: {e}")
    
    print(f"\n📊 Deployment Summary:")
    print(f"Successfully deployed: {success_count}/{len(files_to_deploy)} files")
    
    if success_count > 0:
        print(f"\n🔄 Testing website after deployment...")
        test_website()
    
    return success_count == len(files_to_deploy)

def test_website():
    """Test website functionality after deployment"""
    import requests
    import urllib3
    
    # Disable SSL warnings
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    test_urls = [
        "http://103.9.205.28",
        "http://vn-nextstep.cftenant.com",
        "https://vn-nextstep.cftenant.com"
    ]
    
    for url in test_urls:
        try:
            print(f"\n🔍 Testing {url}...")
            response = requests.get(url, verify=False, timeout=10)
            
            if response.status_code == 200:
                if 'marketplace' in response.text.lower() or 'login' in response.text.lower():
                    print(f"✅ {url} is working - marketplace content detected")
                else:
                    print(f"⚠️ {url} responds but may not be marketplace app")
            else:
                print(f"❌ {url} returned status {response.status_code}")
                
        except Exception as e:
            print(f"❌ Failed to test {url}: {e}")

def main():
    print("🔧 Configuration Deployment Tool")
    print("=" * 40)
    
    # Check if required files exist
    required_files = ['config.php', 'nginx.prod.conf']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return False
    
    # Deploy files
    success = deploy_files()
    
    if success:
        print("\n🎉 All files deployed successfully!")
        print("\n📝 Next steps:")
        print("1. Test login functionality on new domain")
        print("2. Verify session management works correctly")
        print("3. Check that HTTPS redirects properly")
    else:
        print("\n⚠️ Some files failed to deploy. Please check the errors above.")
    
    return success

if __name__ == "__main__":
    main()