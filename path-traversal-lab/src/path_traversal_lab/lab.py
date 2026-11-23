from pathlib import Path

BASE = Path("files").resolve()


def read_file(name):
    path = (BASE / name).resolve()

    if not path.is_relative_to(BASE):
        raise ValueError("Access denied")

    with open(path, "r", encoding="utf-8") as file:
        return file.read()


tests = [
    "report.txt",
    "notes.txt",
    "../secret.txt",
    "../src/path_traversal_lab/lab.py",
]

for name in tests:
    try:
        print(name, "-->", read_file(name).strip())
    except ValueError:
        print(name, "--> Access denied")
