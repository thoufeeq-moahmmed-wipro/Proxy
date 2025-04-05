import json
from datetime import datetime

entries = []
with open("curl_log.txt", "r") as f:
    lines = f.readlines()

for i in range(0, len(lines), 3):  # every 3 lines = one request
    if i+2 < len(lines):
        url = lines[i].strip().replace("Requesting: ", "")
        status = lines[i+1].strip().split(":")[1]
        time = lines[i+2].strip().split(":")[1]
        entries.append({
            "timestamp": datetime.now().isoformat(),
            "url": url,
            "status_code": int(status),
            "response_time": float(time)
        })

with open("final_output.json", "w") as f:
    json.dump(entries, f, indent=2)

print("Results written to final_output.json")
