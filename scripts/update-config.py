#!/usr/bin/env python3

import os
import re

def update_config_file():
    """Update config.php to use environment variables"""
    
    config_file = "config.php"
    
    if not os.path.exists(config_file):
        print(f"❌ {config_file} not found")
        return False
    
    # Read the current config
    with open(config_file, 'r') as f:
        content = f.read()
    
    # Check if already updated
    if "$_ENV" in content:
        print("✅ config.php already uses environment variables")
        return True
    
    # Update the database connection part
    old_pattern = r'(\$servername = ")[^"]+(";\s*\n\s*\$username = ")[^"]+(";\s*\n\s*\$password = ")[^"]+(";\s*\n\s*\$dbname = ")[^"]+(";)'
    
    new_replacement = r'\1$_ENV[\'DB_HOST\'] ?? "103.9.205.28"\2$_ENV[\'DB_USER\'] ?? "callmeserein"\3$_ENV[\'DB_PASSWORD\'] ?? "Fpt1409!@"\4$_ENV[\'DB_NAME\'] ?? "marketplace"\5'
    
    updated_content = re.sub(old_pattern, new_replacement, content)
    
    if updated_content != content:
        # Backup original file
        with open(f"{config_file}.backup", 'w') as f:
            f.write(content)
        
        # Write updated content
        with open(config_file, 'w') as f:
            f.write(updated_content)
        
        print("✅ config.php updated to use environment variables")
        print(f"📁 Backup saved as {config_file}.backup")
        return True
    else:
        print("❌ No changes made to config.php")
        return False

def main():
    print("🔧 Updating config.php for containerized deployment...")
    
    if update_config_file():
        print("✅ Configuration update completed successfully!")
    else:
        print("❌ Configuration update failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
