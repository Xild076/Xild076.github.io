import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

def serve_site(port=8000, directory="../docs"):
    if not os.path.exists(directory):
        print(f"Directory '{directory}' not found. Please build the site first by running 'python app.py'")
        return
    
    os.chdir(directory)
    
    with socketserver.TCPServer(("", port), http.server.SimpleHTTPRequestHandler) as httpd:
        print(f"Serving site at http://localhost:{port}")
        print("Press Ctrl+C to stop the server")
        
        try:
            webbrowser.open(f"http://localhost:{port}")
        except:
            pass
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

if __name__ == "__main__":
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Invalid port number. Using default port 8000.")
    
    serve_site(port)
