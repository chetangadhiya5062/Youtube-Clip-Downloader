import os

HISTORY_FILE = "download_history.txt"

def add_to_history(url, segments, format_id):
    with open(HISTORY_FILE, "a") as f:
        f.write(f"{url} | {segments} | {format_id}\n")

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as f:
        lines = f.readlines()
    return [line.strip() for line in lines[-10:]]  # last 10 downloads
