from fastapi import FastAPI
from neo4j import GraphDatabase
from statistics import mean

app = FastAPI()

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "chakra123"  # change only if different

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)

@app.get("/")
def root():
    return {"status": "Chakra-View Backend Running"}

# ---------------- FAN-IN ----------------
@app.get("/fan_in")
def fan_in(vpa: str):
    query = """
    MATCH (s:Account)-[:TRANSFERRED]->(r:Account {vpa:$vpa})
    RETURN count(DISTINCT s) AS senders, collect(s.vpa) AS sender_list
    """
    with driver.session() as session:
        result = session.run(query, vpa=vpa).single()

    if not result:
        return {"vpa": vpa, "unique_senders": 0, "senders": []}

    return {
        "vpa": vpa,
        "unique_senders": result["senders"],
        "senders": result["sender_list"]
    }

# ---------------- VELOCITY ----------------
@app.get("/velocity")
def velocity(vpa: str):
    query = """
    MATCH (a:Account {vpa:$vpa})-[t:TRANSFERRED]->()
    RETURN t.timestamp AS time, t.amount AS amount
    ORDER BY time
    """
    with driver.session() as session:
        rows = session.run(query, vpa=vpa).data()

    if len(rows) < 2:
        return {
            "vpa": vpa,
            "velocity": "LOW",
            "details": []
        }

    times = [row["time"].to_native() for row in rows]
    deltas = [
        (times[i+1] - times[i]).total_seconds()
        for i in range(len(times)-1)
    ]

    avg_dwell = mean(deltas)

    return {
        "vpa": vpa,
        "velocity": "HIGH" if avg_dwell < 120 else "LOW",
        "avg_dwell_seconds": avg_dwell,
        "transactions": rows
    }

# ---------------- LOUVAIN CLUSTER ----------------
@app.get("/cluster")
def cluster(vpa: str):
    query = """
    CALL gds.louvain.stream({
        nodeProjection: 'Account',
        relationshipProjection: {
            TRANSFERRED: {
                type: 'TRANSFERRED',
                orientation: 'UNDIRECTED'
            }
        }
    })
    YIELD nodeId, communityId
    WITH gds.util.asNode(nodeId) AS node, communityId
    WHERE node.vpa = $vpa
    RETURN communityId
    """

    try:
        with driver.session() as session:
            result = session.run(query, vpa=vpa).single()

        if not result:
            return {"vpa": vpa, "cluster_id": None}

        return {"vpa": vpa, "cluster_id": result["communityId"]}

    except Exception as e:
        return {
            "vpa": vpa,
            "cluster_id": None,
            "error": str(e)
        }







# ---------------- FINAL RISK ----------------
@app.get("/final_score")
def final_score(vpa: str):
    fan = fan_in(vpa)
    vel = velocity(vpa)
    clu = cluster(vpa)

    score = 0

    if fan["unique_senders"] > 10:
        score += 40
    if vel["velocity"] == "HIGH":
        score += 30
    if clu["cluster_id"] is not None:
        score += 30

    if score >= 70:
        risk = "HIGH"
    elif score >= 40:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return {
        "vpa": vpa,
        "risk": risk,
        "score": score,
        "signals": {
            "fan_in": fan["unique_senders"],
            "velocity": vel["velocity"],
            "cluster": clu["cluster_id"]
        }
    }
from pyvis.network import Network
import tempfile
import os

@app.get("/fan_in_graph")
def fan_in_graph(vpa: str):
    query = """
    MATCH (s:Account)-[t:TRANSFERRED]->(r:Account {vpa:$vpa})
    RETURN s.vpa AS sender, r.vpa AS receiver, t.amount AS amount
    """

    with driver.session() as session:
        rows = session.run(query, vpa=vpa).data()

    if not rows:
        return {"error": "No fan-in data found"}

    net = Network(height="500px", width="100%", directed=True)
    net.barnes_hut()

    # center node
    net.add_node(vpa, label=vpa, color="red", size=30)

    for row in rows:
        sender = row["sender"]
        amount = row["amount"]

        net.add_node(sender, label=sender, color="skyblue", size=15)
        net.add_edge(sender, vpa, label=f"₹{amount}")

    tmp_dir = tempfile.gettempdir()
    file_path = os.path.join(tmp_dir, f"fanin_{vpa}.html")
    net.save_graph(file_path)

    return {"graph_path": file_path}
