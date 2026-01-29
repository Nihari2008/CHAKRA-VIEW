print("🔥 GENERATE DATA SCRIPT STARTED 🔥")

import random
import csv
import os
from datetime import datetime, timedelta
from pathlib import Path

# ---------------- CONFIG ----------------
NUM_ACCOUNTS = 500
NUM_MULES = 5
LEGIT_SENDERS_PER_MULE = 40
# ---------------------------------------

# Get absolute project root path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# Ensure data folder exists
DATA_DIR.mkdir(exist_ok=True)

accounts = [f"user_{i}" for i in range(NUM_ACCOUNTS)]
mules = random.sample(accounts, NUM_MULES)
kingpin = "kingpin_main"

nodes = set(accounts + [kingpin])
edges = []

now = datetime.now()

# Fan-in transactions
for mule in mules:
    legit_users = random.sample(
        [a for a in accounts if a not in mules],
        LEGIT_SENDERS_PER_MULE
    )
    for user in legit_users:
        edges.append({
            "from": user,
            "to": mule,
            "amount": random.randint(500, 3000),
            "timestamp": (now - timedelta(minutes=random.randint(1, 120))).isoformat()
        })

# Fan-out transactions
for mule in mules:
    edges.append({
        "from": mule,
        "to": kingpin,
        "amount": random.randint(20000, 60000),
        "timestamp": now.isoformat()
    })

# Write nodes.csv
with open(DATA_DIR / "nodes.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["vpa"])
    for node in nodes:
        writer.writerow([node])

# Write edges.csv
with open(DATA_DIR / "edges.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["from", "to", "amount", "timestamp"])
    for edge in edges:
        writer.writerow([
            edge["from"],
            edge["to"],
            edge["amount"],
            edge["timestamp"]
        ])

print("✅ DATA GENERATION COMPLETE")
print("MULE ACCOUNTS:", mules)
print("KINGPIN ACCOUNT:", kingpin)
print("📁 Files saved to:", DATA_DIR)
