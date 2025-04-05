import json
import time

REPORT_FILE = "proxy_report.json"
LOGS = []

def log_access(ip, url, category, code):
    LOGS.append({
        "timestamp": time.ctime(),
        "ip": ip,
        "url": url,
        "category": category,
        "response_code": code
    })

def generate_report():
    with open(REPORT_FILE, 'w') as f:
        json.dump(LOGS, f, indent=4)
    print(f"Report written to {REPORT_FILE}")
