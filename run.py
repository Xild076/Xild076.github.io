#!/usr/bin/env python3

import os
import sys
import subprocess

def build_site():
    print("Building site...")
    original_dir = os.getcwd()
    result = subprocess.run([sys.executable, "src/app.py"], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Site built successfully!")
        print(result.stdout)
        return True
    else:
        print("❌ Build failed!")
        print(result.stderr)
        return False

def serve_site():
    print("Starting local server...")
    original_dir = os.getcwd()
    os.chdir(os.path.join(original_dir, "src"))
    subprocess.run([sys.executable, "server.py"])
    os.chdir(original_dir)

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "build":
            build_site()
        elif sys.argv[1] == "serve":
            serve_site()
        elif sys.argv[1] == "dev":
            if build_site():
                serve_site()
        else:
            print("Usage: python run.py [build|serve|dev]")
    else:
        if build_site():
            serve_site()

if __name__ == "__main__":
    main()
