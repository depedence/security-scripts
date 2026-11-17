import sqlite3

conn = sqlite3.connect(":memory:")
cur = conn.cursor()

cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
cur.execute("INSERT INTO users (username, password) VALUES ('alex', 'pass123')")
cur.execute("INSERT INTO users (username, password) VALUES ('admin', 'S3cr3t')")
conn.commit()

cur.execute("SELECT id, username FROM users")
print(cur.fetchall())


def login(username, password):
    query = "SELECT id FROM users WHERE username = ? AND password = ?"
    print(query)
    cur.execute(query, (username, password))
    row = cur.fetchall()
    return row != []


tests = [
    ("alex", "pass123"),
    ("alex", "wrong"),
    ("alex'", "x"),
    ("alex' --", "anything"),
    ("alex' OR 1=1 --", "anything"),
    ("nobody' OR 1=1 --", "x"),
]

for username, password in tests:
    print(username, password, login(username, password))
