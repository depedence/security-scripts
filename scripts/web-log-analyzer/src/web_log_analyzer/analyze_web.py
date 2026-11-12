import sys


def analyze(lines, threshold) -> tuple[dict, dict, list]:
    patterns = ["union", "1=1", "../", "<script"]
    status_counts = {}
    not_found_counts = {}
    suspicious = []

    for line in lines:
        words = line.split()
        if len(words) < 9:
            continue
        status = words[8]
        ip = words[0]
        status_counts[status] = status_counts.get(status, 0) + 1
        if status == "404":
            not_found_counts[ip] = not_found_counts.get(ip, 0) + 1
        url = words[6]
        for pattern in patterns:
            if pattern in url.lower():
                suspicious.append(f"{ip} {url}")
                break

    scanners = {}
    for ip, count in not_found_counts.items():
        if count >= threshold:
            scanners[ip] = count

    return status_counts, scanners, suspicious


def main():
    if len(sys.argv) < 3:
        print("Usage: python analyze_web.py <file> <threshold>")
        sys.exit(1)
    filename = sys.argv[1]
    try:
        threshold = int(sys.argv[2])
    except ValueError:
        print("Threshold must be a number")
        sys.exit(1)

    try:
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()
        status_counts, scanners, suspicious = analyze(lines, threshold)
    except FileNotFoundError:
        print(f"File not found: {filename}")
        sys.exit(1)

    print("Status codes:")
    for status, count in status_counts.items():
        print(f"{status}: {count}")

    print(f"Scanners ({threshold}+ x 404):")
    for ip, count in scanners.items():
        print(f"{ip}: {count}")

    print("Suspicious requests:")
    for item in suspicious:
        print(item)


if __name__ == "__main__":
    main()
