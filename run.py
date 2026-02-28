#!/usr/bin/env python3

import os
import sys
import subprocess
import importlib.util

REQUIRED_DEPENDENCIES = {
    "jinja2": "jinja2",
    "markdown2": "markdown2",
    "sass": "libsass",
}


def _missing_dependencies():
    missing = []
    for module_name, package_name in REQUIRED_DEPENDENCIES.items():
        if importlib.util.find_spec(module_name) is None:
            missing.append(package_name)
    return missing


def ensure_dependencies():
    missing = _missing_dependencies()
    if not missing:
        return True

    print("Missing dependencies detected:", ", ".join(missing))
    print(f"Installing with interpreter: {sys.executable}")
    result = subprocess.run([sys.executable, "-m", "pip", "install", *missing], text=True)
    if result.returncode != 0:
        print("❌ Dependency install failed.")
        print(f"Please run: {sys.executable} -m pip install -r requirements.txt")
        return False
    return True

def build_site():
    if not ensure_dependencies():
        return False

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
