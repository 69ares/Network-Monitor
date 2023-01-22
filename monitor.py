import subprocess
import requests
import json
import time
import ipaddress

info = subprocess.STARTUPINFO()
info.dwFlags = subprocess.STARTF_USESHOWWINDOW
info.wShowWindow = subprocess.SW_HIDE

first_ips = set()
ip_bad = set()
ip_trust = set()

API_KEY = "API"
THRESHOLD = 70

def check_ip(ip):
    try:
        ip_address = ipaddress.ip_address(ip.split(':')[0])
        if ip_address.is_private:
            return
        url = f"https://api.abuseipdb.com/api/v2/check?ip={ip.split(':')[0]}&key={API_KEY}"
        response = requests.get(url)
        data = json.loads(response.text)
        if data.get("abuseConfidenceScore"):
            if data["abuseConfidenceScore"] >= THRESHOLD:
                with open("ip_bad.txt", "a") as f:
                    f.write(ip.split(':')[0] + "\n")
                    ip_bad.add(ip)
            else:
                with open("ip_trust.txt", "a") as f:
                    f.write(ip.split(':')[0] + "\n")
                    ip_trust.add(ip)
        else:
            with open("ip_trust.txt", "a") as f:
                f.write(ip.split(':')[0] + "\n")
    except ValueError:
        return

while True:
    # Get the list of IPs from the active connections
    result = subprocess.run(["netstat", "-n"], startupinfo=info, stdout=subprocess.PIPE)
    output = result.stdout.decode()
    print(output)
    for line in output.splitlines():
        if "ESTABLISHED" in line:
            ip = line.split()[2]
            if ip not in first_ips:
                first_ips.add(ip)
                check_ip(ip)
                print(ip)
    # Write the current IPs to the file
    with open("ip.txt", "w") as f:
        for ip in first_ips:
            f.write(ip + "\n")
    time.sleep(10)
