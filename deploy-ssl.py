#!/usr/bin/env python3
import subprocess
import sys
import time
import os
from datetime import datetime

SERVER_IP = "103.9.205.28"
SSH_PORT = "2012"
SSH_PASSWORD = "Next-Step@2310"
SSH_USER = "root"
PROJECT_PATH = "/tmp/marketplace"

def run_command(command, description):
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] {description}")
    print(f"Command: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=300)
        
        if result.stdout:
            print(f"Output: {result.stdout.strip()}")
        if result.stderr:
            print(f"Error: {result.stderr.strip()}")
            
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
            return True
        else:
            print(f"❌ {description} - FAILED (Exit code: {result.returncode})")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"❌ {description} - TIMEOUT")
        return False
    except Exception as e:
        print(f"❌ {description} - ERROR: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("🚀 TRIỂN KHAI SSL CHO MARKETPLACE")
    print("=" * 60)
    
    # Bước 1: Upload nginx.ssl.conf
    success = run_command(
        f'pscp -P {SSH_PORT} -pw "{SSH_PASSWORD}" nginx.ssl.conf {SSH_USER}@{SERVER_IP}:{PROJECT_PATH}/nginx.ssl.conf',
        "Upload nginx.ssl.conf"
    )
    if not success:
        print("❌ Không thể upload nginx.ssl.conf")
        return False
    
    # Bước 2: Upload docker-compose.prod.yml
    success = run_command(
        f'pscp -P {SSH_PORT} -pw "{SSH_PASSWORD}" docker-compose.prod.yml {SSH_USER}@{SERVER_IP}:{PROJECT_PATH}/docker-compose.prod.yml',
        "Upload docker-compose.prod.yml"
    )
    if not success:
        print("❌ Không thể upload docker-compose.prod.yml")
        return False
    
    # Bước 3: Tạo thư mục ssl trong project nếu chưa có
    success = run_command(
        f'plink -P {SSH_PORT} -pw "{SSH_PASSWORD}" {SSH_USER}@{SERVER_IP} "mkdir -p {PROJECT_PATH}/ssl"',
        "Tạo thư mục ssl trong project"
    )
    
    # Bước 4: Copy chứng chỉ SSL từ /root/ssl vào project
    success = run_command(
        f'plink -P {SSH_PORT} -pw "{SSH_PASSWORD}" {SSH_USER}@{SERVER_IP} "cp /root/ssl/cert.pem {PROJECT_PATH}/ssl/ && cp /root/ssl/key.pem {PROJECT_PATH}/ssl/"',
        "Copy chứng chỉ SSL vào project"
    )
    if not success:
        print("❌ Không thể copy chứng chỉ SSL")
        return False
    
    # Bước 5: Kiểm tra file SSL đã được copy
    success = run_command(
        f'plink -P {SSH_PORT} -pw "{SSH_PASSWORD}" {SSH_USER}@{SERVER_IP} "ls -la {PROJECT_PATH}/ssl/"',
        "Kiểm tra file SSL trong project"
    )
    
    # Bước 6: Dừng các container hiện tại
    success = run_command(
        f'plink -P {SSH_PORT} -pw "{SSH_PASSWORD}" {SSH_USER}@{SERVER_IP} "cd {PROJECT_PATH} && docker-compose -f docker-compose.prod.yml down"',
        "Dừng các container hiện tại"
    )
    
    # Bước 7: Khởi động lại với cấu hình SSL mới
    success = run_command(
        f'plink -P {SSH_PORT} -pw "{SSH_PASSWORD}" {SSH_USER}@{SERVER_IP} "cd {PROJECT_PATH} && docker-compose -f docker-compose.prod.yml up -d"',
        "Khởi động container với SSL"
    )
    if not success:
        print("❌ Không thể khởi động container với SSL")
        return False
    
    # Bước 8: Chờ container khởi động
    print("\n⏳ Chờ container khởi động...")
    time.sleep(30)
    
    # Bước 9: Kiểm tra trạng thái container
    success = run_command(
        f'plink -P {SSH_PORT} -pw "{SSH_PASSWORD}" {SSH_USER}@{SERVER_IP} "cd {PROJECT_PATH} && docker-compose -f docker-compose.prod.yml ps"',
        "Kiểm tra trạng thái container"
    )
    
    # Bước 10: Kiểm tra log nginx
    success = run_command(
        f'plink -P {SSH_PORT} -pw "{SSH_PASSWORD}" {SSH_USER}@{SERVER_IP} "cd {PROJECT_PATH} && docker-compose -f docker-compose.prod.yml logs nginx | tail -20"',
        "Kiểm tra log nginx"
    )
    
    print("\n" + "=" * 60)
    print("✅ TRIỂN KHAI SSL HOÀN THÀNH!")
    print("🌐 Kiểm tra trang web tại: https://vn-nextstep.cftenant.com")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎉 Triển khai SSL thành công!")
            sys.exit(0)
        else:
            print("\n💥 Triển khai SSL thất bại!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ Triển khai bị hủy bởi người dùng")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Lỗi không mong muốn: {str(e)}")
        sys.exit(1)