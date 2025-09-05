#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import datetime
import json
from pathlib import Path

class SystemBackup:
    def __init__(self):
        self.server_ip = "103.9.205.28"
        self.server_user = "root"
        self.server_password = "Next-Step@2310"
        self.backup_dir = "backups"
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def create_backup_directory(self):
        """Tạo thư mục backup local"""
        backup_path = Path(self.backup_dir)
        backup_path.mkdir(exist_ok=True)
        
        current_backup = backup_path / f"backup_{self.timestamp}"
        current_backup.mkdir(exist_ok=True)
        
        return current_backup
    
    def backup_database(self, backup_path):
        """Sao lưu database MySQL từ server"""
        print("🗄️ Đang sao lưu database MySQL...")
        
        # Lệnh mysqldump trên server
        dump_command = (
            "docker exec marketplace-mysql-prod mysqldump "
            "-u root -pNext-Step@2310 marketplace_db > /tmp/marketplace_backup.sql"
        )
        
        # Thực hiện dump trên server
        plink_dump = [
            "plink", "-ssh", f"{self.server_user}@{self.server_ip}",
            "-P", "2012", "-pw", self.server_password,
            "-batch", dump_command
        ]
        
        try:
            result = subprocess.run(plink_dump, capture_output=True, text=True, check=True)
            print("✅ Database dump thành công")
            
            # Download file backup về local
            pscp_download = [
                "pscp", "-P", "2012", "-pw", self.server_password,
                f"{self.server_user}@{self.server_ip}:/tmp/marketplace_backup.sql",
                str(backup_path / "database_backup.sql")
            ]
            
            subprocess.run(pscp_download, check=True)
            print("✅ Database backup đã tải về local")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Lỗi backup database: {e}")
            return False
            
        return True
    
    def backup_application_files(self, backup_path):
        """Sao lưu source code và files từ server"""
        print("📁 Đang sao lưu application files...")
        
        try:
            # Tạo archive trên server
            archive_command = (
                "cd /var/www && "
                "tar -czf /tmp/marketplace_files.tar.gz html/"
            )
            
            plink_archive = [
                "plink", "-ssh", f"{self.server_user}@{self.server_ip}",
                "-P", "2012", "-pw", self.server_password,
                "-batch", archive_command
            ]
            
            subprocess.run(plink_archive, check=True)
            print("✅ Application files archive thành công")
            
            # Download archive về local
            pscp_download = [
                "pscp", "-P", "2012", "-pw", self.server_password,
                f"{self.server_user}@{self.server_ip}:/tmp/marketplace_files.tar.gz",
                str(backup_path / "application_files.tar.gz")
            ]
            
            subprocess.run(pscp_download, check=True)
            print("✅ Application files đã tải về local")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Lỗi backup application files: {e}")
            return False
            
        return True
    
    def backup_docker_configs(self, backup_path):
        """Sao lưu Docker configurations"""
        print("🐳 Đang sao lưu Docker configurations...")
        
        config_files = [
            "/root/docker-compose.prod.yml",
            "/root/nginx.prod.conf",
            "/root/config.php"
        ]
        
        try:
            for config_file in config_files:
                filename = os.path.basename(config_file)
                
                pscp_download = [
                    "pscp", "-P", "2012", "-pw", self.server_password,
                    f"{self.server_user}@{self.server_ip}:{config_file}",
                    str(backup_path / filename)
                ]
                
                try:
                    subprocess.run(pscp_download, check=True)
                    print(f"✅ Đã backup {filename}")
                except subprocess.CalledProcessError:
                    print(f"⚠️ Không thể backup {filename} (có thể file không tồn tại)")
            
        except Exception as e:
            print(f"❌ Lỗi backup Docker configs: {e}")
            return False
            
        return True
    
    def backup_docker_volumes(self, backup_path):
        """Sao lưu Docker volumes data"""
        print("💾 Đang sao lưu Docker volumes...")
        
        try:
            # Backup MySQL data volume
            volume_command = (
                "docker run --rm -v marketplace_mysql_data_prod:/data "
                "-v /tmp:/backup alpine tar -czf /backup/mysql_volume.tar.gz -C /data ."
            )
            
            plink_volume = [
                "plink", "-ssh", f"{self.server_user}@{self.server_ip}",
                "-P", "2012", "-pw", self.server_password,
                "-batch", volume_command
            ]
            
            subprocess.run(plink_volume, check=True)
            print("✅ MySQL volume backup thành công")
            
            # Download volume backup
            pscp_download = [
                "pscp", "-P", "2012", "-pw", self.server_password,
                f"{self.server_user}@{self.server_ip}:/tmp/mysql_volume.tar.gz",
                str(backup_path / "mysql_volume.tar.gz")
            ]
            
            subprocess.run(pscp_download, check=True)
            print("✅ MySQL volume đã tải về local")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Lỗi backup Docker volumes: {e}")
            return False
            
        return True
    
    def get_system_info(self, backup_path):
        """Lấy thông tin hệ thống hiện tại"""
        print("ℹ️ Đang thu thập thông tin hệ thống...")
        
        commands = {
            "docker_ps": "docker ps -a",
            "docker_images": "docker images",
            "docker_volumes": "docker volume ls",
            "docker_networks": "docker network ls",
            "disk_usage": "df -h",
            "memory_info": "free -h",
            "system_info": "uname -a"
        }
        
        system_info = {}
        
        for info_name, command in commands.items():
            try:
                plink_cmd = [
                    "plink", "-ssh", f"{self.server_user}@{self.server_ip}",
                    "-P", "2012", "-pw", self.server_password,
                    "-batch", command
                ]
                
                result = subprocess.run(plink_cmd, capture_output=True, text=True, check=True)
                system_info[info_name] = result.stdout.strip()
                
            except subprocess.CalledProcessError as e:
                system_info[info_name] = f"Error: {e}"
        
        # Lưu thông tin hệ thống
        with open(backup_path / "system_info.json", "w", encoding="utf-8") as f:
            json.dump(system_info, f, indent=2, ensure_ascii=False)
        
        print("✅ Thông tin hệ thống đã được lưu")
        return True
    
    def create_restore_script(self, backup_path):
        """Tạo script khôi phục"""
        restore_script = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Script khôi phục hệ thống từ backup {self.timestamp}
# Sử dụng: python restore_system.py

import subprocess
import sys

class SystemRestore:
    def __init__(self):
        self.server_ip = "103.9.205.28"
        self.server_user = "root"
        self.server_password = "Next-Step@2310"
        self.backup_timestamp = "{self.timestamp}"
    
    def restore_database(self):
        print("🗄️ Đang khôi phục database...")
        
        # Upload database backup
        pscp_upload = [
            "pscp", "-pw", self.server_password,
            "database_backup.sql",
            f"{{self.server_user}}@{{self.server_ip}}:/tmp/restore_db.sql"
        ]
        
        subprocess.run(pscp_upload, check=True)
        
        # Restore database
        restore_cmd = (
            "docker exec -i marketplace-mysql-prod mysql "
            "-u root -pNext-Step@2310 marketplace_db < /tmp/restore_db.sql"
        )
        
        plink_restore = [
            "plink", "-ssh", f"{{self.server_user}}@{{self.server_ip}}",
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
            f"{{self.server_user}}@{{self.server_ip}}:/tmp/restore_files.tar.gz"
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
            "plink", "-ssh", f"{{self.server_user}}@{{self.server_ip}}",
            "-pw", self.server_password,
            "-batch", extract_cmd
        ]
        
        subprocess.run(plink_extract, check=True)
        print("✅ Application files đã được khôi phục")

if __name__ == "__main__":
    restore = SystemRestore()
    
    print(f"🔄 Bắt đầu khôi phục hệ thống từ backup {{restore.backup_timestamp}}")
    
    try:
        restore.restore_database()
        restore.restore_files()
        print("✅ Khôi phục hệ thống hoàn tất!")
    except Exception as e:
        print(f"❌ Lỗi khôi phục: {{e}}")
        sys.exit(1)
'''
        
        with open(backup_path / "restore_system.py", "w", encoding="utf-8") as f:
            f.write(restore_script)
        
        print("✅ Script khôi phục đã được tạo")
    
    def run_backup(self):
        """Thực hiện toàn bộ quá trình backup"""
        print(f"🚀 Bắt đầu sao lưu hệ thống - {self.timestamp}")
        print("=" * 50)
        
        # Tạo thư mục backup
        backup_path = self.create_backup_directory()
        print(f"📁 Thư mục backup: {backup_path}")
        
        success_count = 0
        total_tasks = 5
        
        # Thực hiện các tác vụ backup
        if self.backup_database(backup_path):
            success_count += 1
        
        if self.backup_application_files(backup_path):
            success_count += 1
        
        if self.backup_docker_configs(backup_path):
            success_count += 1
        
        if self.backup_docker_volumes(backup_path):
            success_count += 1
        
        if self.get_system_info(backup_path):
            success_count += 1
        
        # Tạo script khôi phục
        self.create_restore_script(backup_path)
        
        # Tạo file thông tin backup
        backup_info = {
            "timestamp": self.timestamp,
            "server_ip": self.server_ip,
            "backup_path": str(backup_path),
            "success_tasks": success_count,
            "total_tasks": total_tasks,
            "status": "completed" if success_count == total_tasks else "partial"
        }
        
        with open(backup_path / "backup_info.json", "w", encoding="utf-8") as f:
            json.dump(backup_info, f, indent=2, ensure_ascii=False)
        
        print("=" * 50)
        print(f"📊 Kết quả backup: {success_count}/{total_tasks} tác vụ thành công")
        
        if success_count == total_tasks:
            print("✅ Sao lưu hệ thống hoàn tất!")
            print(f"📁 Backup được lưu tại: {backup_path}")
            print(f"🔄 Để khôi phục, chạy: python {backup_path}/restore_system.py")
        else:
            print("⚠️ Sao lưu hoàn tất với một số lỗi")
            print("🔍 Kiểm tra log để biết chi tiết")
        
        return success_count == total_tasks

if __name__ == "__main__":
    backup = SystemBackup()
    
    try:
        success = backup.run_backup()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n❌ Backup bị hủy bởi người dùng")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Lỗi không mong muốn: {e}")
        sys.exit(1)