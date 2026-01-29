from fastapi import FastAPI
import random

app = FastAPI()

# =========================
# HARD-CODED DEMO MULE ACCOUNTS (5 / 500)
# =========================
MULE_ACCOUNTS = {
    "user_17",
    "user_83",
    "user_221",
    "user_342",
    "user_498"
}

def is_mule(vpa: str) -> bool:
    return vpa in MULE_ACCOUNTS


# =========================
# FAN-IN ANALYSIS
# =========================
@app.get("/fan_in")
def fan_in(vpa: str):
    mule = is_mule(vpa)

    if mule:
        unique_senders = 35
        risk_score = 85
    else:
        unique_senders = 3
        risk_score = 15

    rows = []
    for _ in range(unique_senders):
        rows.append({
            "sender": f"user_{random.randint(1,500)}",
            "amount": random.randint(500, 5000)
        })

    return {
        "unique_senders": unique_senders,
        "risk_score": risk_score,
        "rows": rows
    }


# =========================
# VELOCITY (MONEY DWELL TIME)
# =========================
@app.get("/velocity")
def velocity(vpa: str):
    mule = is_mule(vpa)

    rows = []
    if mule:
        for _ in range(5):
            rows.append({
                "money_in_from": f"user_{random.randint(1,500)}",
                "money_out_to": f"user_{random.randint(1,500)}",
                "amount": random.randint(1000, 9000),
                "time_minutes": random.randint(1, 4),
                "risk": "HIGH"
            })
        risk_score = 90
    else:
        risk_score = 10

    return {
        "rows": rows,
        "risk_score": risk_score
    }


# =========================
# CLUSTER / NETWORK ANALYSIS
# =========================
@app.get("/cluster")
def cluster(vpa: str):
    mule = is_mule(vpa)

    if mule:
        return {
            "in_network": True,
            "network_size": 120,
            "risk_score": 95
        }
    else:
        return {
            "in_network": False,
            "network_size": 2,
            "risk_score": 5
        }


# =========================
# FINAL RISK SCORE
# =========================
@app.get("/final_score")
def final_score(vpa: str):
    mule = is_mule(vpa)

    if mule:
        return {
            "score": 95,
            "level": "HIGH",
            "label": "CONFIRMED MULE ACCOUNT"
        }
    else:
        return {
            "score": 20,
            "level": "LOW",
            "label": "NORMAL ACCOUNT"
        }
