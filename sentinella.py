import subprocess
import requests
import json
import time
import ipaddress
import tkinter as tk
from tkinter import messagebox, simpledialog

info = subprocess.STARTUPINFO()
info.dwFlags = subprocess.STARTF_USESHOWWINDOW
info.wShowWindow = subprocess.SW_HIDE

first_ips = set()
ip_bad = set()
ip_trust = set()

root = tk.Tk()
root.withdraw()
#API_KEY = ""
API_KEY = simpledialog.askstring("API KEY", "Inserisci la tua API KEY:", parent=root)
THRESHOLD = simpledialog.askinteger("THRESHOLD", "Inserisci il valore dello score:", parent=root)

def check_ip(ip, process, pid):
    try:
        ip_address = ipaddress.ip_address(ip.split(':')[0])
        if ip_address.is_private:
            return
        url = f"https://api.abuseipdb.com/api/v2/check?ipAddress={ip_address}&maxAgeInDays=90&verbose&key={API_KEY}"
        info = subprocess.STARTUPINFO()
        info.dwFlags = subprocess.STARTF_USESHOWWINDOW
        info.wShowWindow = subprocess.SW_HIDE
        response = subprocess.run(["curl", "-G", url, "-H", f"Key: {API_KEY}", "-H", "Accept: application/json"], stdout=subprocess.PIPE, startupinfo=info)

        try:
            data = json.loads(response.stdout.decode())
        except json.decoder.JSONDecodeError:
            print("JSON errato")
            return
        score = data["data"]["abuseConfidenceScore"]
        if score >= THRESHOLD:
            with open("ip_bad.txt", "a") as f:
                f.write(ip.split(':')[0] + ':' + process + ':' + pid + "\n")
                ip_bad.add(ip)
                result = messagebox.askquestion("Termina processo", f"Terminare il processo con PID {pid} il processo è {process}. Score abuse: {score}", icon='warning')
                if result == 'no':
                    from datetime import datetime
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    with open("bad_ip_trust.txt", "a") as f:
                        f.write(ip.split(':')[0] + ':' + process + ':' + pid + ':' + current_time + "\n")
                elif result == 'yes':
                    subprocess.run(["taskkill", "/PID", pid, '/F'], stdout=subprocess.PIPE)

        else:
            with open("ip_trust.txt", "a") as f:
                f.write(ip.split(':')[0] + "\n")
                ip_trust.add(ip)
    except ValueError:
        return



while True:
    result = subprocess.run(["netstat", "-ano"], startupinfo=info, stdout=subprocess.PIPE)
    output = result.stdout.decode(errors='ignore',encoding='cp437')
    for line in output.splitlines():
        if "ESTABLISHED" in line:
            ip = line.split()[2]
            if ip not in first_ips:
                first_ips.add(ip)
                for line in output.splitlines():
                    if ip in line:
                        pid = line.split()[-1]
                        process_result = subprocess.run(["tasklist", "/FI", f"PID eq {pid}"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
                        process_output = process_result.stdout.decode(errors='ignore',encoding='cp850')
                        try:
                            process = process_output.splitlines()[3].split()[0]
                        except IndexError:
                            process = "Bo"
                        print(process)
                        check_ip(ip,process,pid)
    with open("ip.txt", "w") as f:
        for ip in first_ips:
            f.write(ip + "\n")
    time.sleep(10)
