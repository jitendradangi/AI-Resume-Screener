import subprocess
import time
import urllib.request
import urllib.parse
import urllib.error
import json
import uuid

def main():
    print("Starting uvicorn server...")
    process = subprocess.Popen(
        ["venv\\Scripts\\python.exe" if False else "python", "-m", "uvicorn", "app.main:app", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    time.sleep(3)
    
    unique_id = str(uuid.uuid4())[:8]
    test_email = f"test_{unique_id}@example.com"
    test_password = "password123"
    
    try:
        # 1. Register with JSON
        print(f"Testing registration for {test_email}...")
        req = urllib.request.Request(
            "http://127.0.0.1:8000/auth/register",
            data=json.dumps({"full_name": "Test User", "email": test_email, "password": test_password}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        try:
            with urllib.request.urlopen(req) as f:
                res = json.loads(f.read().decode("utf-8"))
                print("Register response:", res)
        except urllib.error.HTTPError as e:
            print("Register failed:", e.read().decode("utf-8"))
            return
            
        # 2. Login with application/x-www-form-urlencoded (like Swagger)
        print("Testing login with form data (simulating Swagger)...")
        form_data = urllib.parse.urlencode({
            "username": test_email,
            "password": test_password
        }).encode("utf-8")
        
        req = urllib.request.Request(
            "http://127.0.0.1:8000/auth/login",
            data=form_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            method="POST"
        )
        try:
            with urllib.request.urlopen(req) as f:
                res = json.loads(f.read().decode("utf-8"))
                print("Login response:", res)
        except urllib.error.HTTPError as e:
            print("Login failed:", e.read().decode("utf-8"))
            
    finally:
        print("Shutting down server...")
        process.terminate()
        try:
            process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            process.kill()

if __name__ == "__main__":
    main()
