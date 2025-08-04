#!/usr/bin/env python3
"""
Riceify Polybar Extension
A polybar module for managing and displaying rice configurations
"""

import os
import sys
import json
import subprocess
import argparse
from pathlib import Path
from datetime import datetime
import glob

class RiceifyPolybar:
    def __init__(self):
        self.home_dir = os.path.expanduser("~")
        self.rice_dir = os.path.join(self.home_dir, "Riceify", "rices")
        self.db_file = os.path.join(self.home_dir, "Riceify", "db.rcf")
        self.current_rice_file = os.path.join(self.home_dir, ".riceify_current")
        
    def get_rices(self):
        """Get list of available rices"""
        if not os.path.exists(self.rice_dir):
            return []
        
        rices = []
        for item in os.listdir(self.rice_dir):
            rice_path = os.path.join(self.rice_dir, item)
            if os.path.isdir(rice_path):
                rices.append(item)
        return sorted(rices)
    
    def get_current_rice(self):
        """Get currently active rice"""
        if os.path.exists(self.current_rice_file):
            with open(self.current_rice_file, 'r') as f:
                return f.read().strip()
        return None
    
    def set_current_rice(self, rice_name):
        """Set current rice"""
        with open(self.current_rice_file, 'w') as f:
            f.write(rice_name)
    
    def get_rice_info(self, rice_name):
        """Get information about a specific rice"""
        rice_path = os.path.join(self.rice_dir, rice_name)
        if not os.path.exists(rice_path):
            return None
        
        info = {
            'name': rice_name,
            'path': rice_path,
            'config_exists': os.path.exists(os.path.join(rice_path, '.config')),
            'home_files_exist': len(glob.glob(os.path.join(rice_path, '.*'))) > 0
        }
        
        # Get creation time
        try:
            stat = os.stat(rice_path)
            info['created'] = datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M')
        except:
            info['created'] = 'Unknown'
        
        return info
    
    def switch_rice(self, rice_name):
        """Switch to a specific rice"""
        rice_path = os.path.join(self.rice_dir, rice_name)
        if not os.path.exists(rice_path):
            return False, f"Rice '{rice_name}' not found"
        
        try:
            # Copy rice files to home directory
            cmd = f"cp -rT {rice_path}/ ~"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.set_current_rice(rice_name)
                return True, f"Switched to rice '{rice_name}'"
            else:
                return False, f"Failed to switch rice: {result.stderr}"
        except Exception as e:
            return False, f"Error switching rice: {str(e)}"
    
    def add_rice(self, rice_name):
        """Add a new rice"""
        rice_path = os.path.join(self.rice_dir, rice_name)
        
        if os.path.exists(rice_path):
            return False, f"Rice '{rice_name}' already exists"
        
        try:
            # Create rice directory
            os.makedirs(rice_path, exist_ok=True)
            
            # Copy config files
            config_src = os.path.join(self.home_dir, ".config")
            config_dst = os.path.join(rice_path, ".config")
            if os.path.exists(config_src):
                subprocess.run(f"cp -r {config_src} {config_dst}", shell=True)
            
            # Copy home files
            subprocess.run(f"rsync -a {self.home_dir}/.??* {rice_path}/", shell=True)
            
            return True, f"Created rice '{rice_name}'"
        except Exception as e:
            return False, f"Error creating rice: {str(e)}"
    
    def remove_rice(self, rice_name):
        """Remove a rice"""
        rice_path = os.path.join(self.rice_dir, rice_name)
        
        if not os.path.exists(rice_path):
            return False, f"Rice '{rice_name}' not found"
        
        try:
            import shutil
            shutil.rmtree(rice_path)
            return True, f"Removed rice '{rice_name}'"
        except Exception as e:
            return False, f"Error removing rice: {str(e)}"
    
    def display_status(self):
        """Display rice status for polybar"""
        rices = self.get_rices()
        current_rice = self.get_current_rice()
        
        if not rices:
            return "🍚 No rices"
        
        if current_rice and current_rice in rices:
            return f"🍚 {current_rice} ({len(rices)})"
        else:
            return f"🍚 {len(rices)} rices"
    
    def display_menu(self):
        """Display rice menu for polybar"""
        rices = self.get_rices()
        current_rice = self.get_current_rice()
        
        menu_items = []
        for rice in rices:
            if rice == current_rice:
                menu_items.append(f"✓ {rice}")
            else:
                menu_items.append(f"  {rice}")
        
        return "\n".join(menu_items)

def main():
    parser = argparse.ArgumentParser(description="Riceify Polybar Extension")
    parser.add_argument("--status", action="store_true", help="Display current rice status")
    parser.add_argument("--menu", action="store_true", help="Display rice menu")
    parser.add_argument("--switch", metavar="RICE", help="Switch to specified rice")
    parser.add_argument("--add", metavar="RICE", help="Add new rice")
    parser.add_argument("--remove", metavar="RICE", help="Remove rice")
    parser.add_argument("--list", action="store_true", help="List all rices")
    parser.add_argument("--info", metavar="RICE", help="Get rice information")
    
    args = parser.parse_args()
    
    riceify = RiceifyPolybar()
    
    if args.status:
        print(riceify.display_status())
    elif args.menu:
        print(riceify.display_menu())
    elif args.switch:
        success, message = riceify.switch_rice(args.switch)
        print(message)
        if not success:
            sys.exit(1)
    elif args.add:
        success, message = riceify.add_rice(args.add)
        print(message)
        if not success:
            sys.exit(1)
    elif args.remove:
        success, message = riceify.remove_rice(args.remove)
        print(message)
        if not success:
            sys.exit(1)
    elif args.list:
        rices = riceify.get_rices()
        if rices:
            for rice in rices:
                print(rice)
        else:
            print("No rices found")
    elif args.info:
        info = riceify.get_rice_info(args.info)
        if info:
            print(json.dumps(info, indent=2))
        else:
            print(f"Rice '{args.info}' not found")
            sys.exit(1)
    else:
        # Default: show status
        print(riceify.display_status())

if __name__ == "__main__":
    main() 