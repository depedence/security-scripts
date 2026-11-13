import json

events = []

with open("scripts/auth-log-parser/data/auth_small.txt", "r", encoding="utf-8") as file:
    for line in file:
        words = line.split()
        idx = words.index("from")
        time = words[2]
        ip = words[idx + 1]
        user = words[idx - 1]

        if "Failed" in line:
            result = "failed"
        else:
            result = "accepted"

        events.append({"time": time, "result": result, "user": user, "ip": ip})

with open("scripts/auth-log-parser/data/events.json", "w", encoding="utf-8") as file:
    json.dump(events, file, indent=2)

with open("scripts/auth-log-parser/data/events.json", "r", encoding="utf-8") as file:
    failed = 0
    accepted = 0
    failed_by_ip = {}

    loaded = json.load(file)

print(f"Total events: {len(loaded)}")
for event in loaded:
    if event["result"] == "failed":
        failed += 1
        ip = event["ip"]
        failed_by_ip[ip] = failed_by_ip.get(ip, 0) + 1
    else:
        accepted += 1

print(f"Failed: {failed}")
print(f"Accepted: {accepted}")
print("Failed by IP:")
for ip, count in failed_by_ip.items():
    if count >= 2:
        print(f"{ip}: {count}")
