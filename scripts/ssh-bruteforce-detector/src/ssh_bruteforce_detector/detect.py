import sys


def main():
    if len(sys.argv) < 3:
        print("Usage: python detect.py <file> <threshold>")
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
        result = find_bruteforce(lines, threshold)
    except FileNotFoundError:
        print(f"File not found: {filename}")
        sys.exit(1)

    with open("report.txt", "w", encoding="utf-8") as file:
        for ip, count in result.items():
            print(f"{ip}: {count}")
            file.write(f"{ip}: {count}\n")


def find_bruteforce(lines, threshold):
    counts = {}
    found = {}

    for line in lines:
        if "Failed" in line:
            words = line.split()
            if "from" not in words:
                continue
            idx = words.index("from")
            if idx + 1 >= len(words):
                continue
            ip = words[idx + 1]
            counts[ip] = counts.get(ip, 0) + 1
        elif "Accepted" in line:
            words = line.split()
            if "from" not in words:
                continue
            idx = words.index("from")
            if idx + 1 >= len(words):
                continue
            ip = words[idx + 1]
            if counts.get(ip, 0) >= threshold:
                found[ip] = counts[ip]

    return found


if __name__ == "__main__":
    main()
