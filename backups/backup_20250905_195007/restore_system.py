#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Script khôi phục hệ thống từ backup 20250905_195007
# Sử dụng: python restore_system.py

import subprocess
import sys

class SystemRestore:
    def __init__(self):
        self.server_ip = "103.9.205.28"
        self.server_user = "root"
        self.server_password = "Next-Step@2310"
        self.backup_timestamp = "20250905_195007"
    
    def restore_database(self):
        print("🗄️ Đang khôi phục database...")
        
        # Upload database backup
        pscp_upload = [
            "pscp", "-pw", self.server_password,
            "database_backup.sql",
            f"{self.server_user}@{self.server_ip}:/tmp/restore_db.sql"
        ]
        
        subprocess.run(pscp_upload, check=True)
        
        # Restore database
        restore_cmd = (
            "docker exec -i marketplace-mysql-prod mysql "
            "-u root -pNext-Step@2310 marketplace_db < /tmp/restore_db.sql"
        )
        
        plink_restore = [
            "plink", "-ssh", f"{self.server_user}@{self.server_ip}",
            "-pw", self.server_password,
            "-batch", restore_cmd
        ]
        
        subprocess.run(plink_restore, check=True)
        print("✅ Database đã được khôi phục")
    
    def restore_files(self):
        print("📁 Đang khôi phục application files...")
        
        # Upload files backup
        pscp_upload = [
            "pscp", "-pw", self.server_password,
            "application_files.tar.gz",
            f"{self.server_user}@{self.server_ip}:/tmp/restore_files.tar.gz"
        ]
        
        subprocess.run(pscp_upload, check=True)
        
        # Extract files
        extract_cmd = (
            "cd /var/www && "
            "rm -rf html_backup && "
            "mv html html_backup && "
            "tar -xzf /tmp/restore_files.tar.gz"
        )
        
        plink_extract = [
            "plink", "-ssh", f"{self.server_user}@{self.server_ip}",
            "-pw", self.server_password,
            "-batch", extract_cmd
        ]
        
        subprocess.run(plink_extract, check=True)
        print("✅ Application files đã được khôi phục")

if __name__ == "__main__":
    restore = SystemRestore()
    
    print(f"🔄 Bắt đầu khôi phục hệ thống từ backup {restore.backup_timestamp}")
    
    try:
        restore.restore_database()
        restore.restore_files()
        print("✅ Khôi phục hệ thống hoàn tất!")
    except Exception as e:
        print(f"❌ Lỗi khôi phục: {e}")
        sys.exit(1)
