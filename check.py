#!/usr/bin/env python3
"""
Simple pre-deployment check for Railway
"""

import os
import json

def main():
    print("🚀 Railway deployment check\n")
    
    # Check essential files
    required = ['Dockerfile', 'railway.json', 'requirements.txt', 'run.py', 'app/__init__.py']
    missing = [f for f in required if not os.path.exists(f)]
    
    if missing:
        print(f"❌ Missing files: {', '.join(missing)}")
        return 1
    
    print("✅ All required files present")
    
    # Check railway.json
    try:
        with open('railway.json') as f:
            config = json.load(f)
        if 'build' in config and 'deploy' in config:
            print("✅ Railway config valid")
        else:
            print("❌ Invalid railway.json")
            return 1
    except:
        print("❌ railway.json error")
        return 1
    
    print("\n📋 Configure these variables in Railway:")
    vars_needed = [
        'DATABASE_HOST', 'DATABASE_USER', 'DATABASE_PASSWORD', 
        'SECRET_KEY', 'JWT_SECRET_KEY', 'FLASK_ENV=production'
    ]
    for var in vars_needed:
        print(f"  • {var}")
    
    print("\n✅ Ready for Railway deployment!")
    return 0

if __name__ == "__main__":
    exit(main())