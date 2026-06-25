# CHAKRA-VIEW:
Graph-Powered Real-Time UPI Mule Account Detection

> **🥈 2nd Place Winner & won 20k cash price at FORTEX 36HRS National Hackathon, SRM AP.**
>* An internal, bank-side analytical engine designed for risk teams to detect and mitigate sophisticated digital mule account networks in real-time before fraudulent funds disappear.*

##  The Challenge & Core Problem
With the rise of sophisticated digital scams (like the "digital arrest" phone scams), fraudsters are rapidly routing stolen money across complex webs of bank accounts to obscure their tracks. 

Traditional rule-based banking systems and basic machine learning models often fail because **fraud is about relationships and connections, not isolated incidents.** Once stolen money splits across multiple mule layers, it becomes nearly impossible for law enforcement or banks to trace or recover.

##  Our Solution: A Bank-Side Graph Analytics Engine
**Chakra-View** approaches fraud through connection analysis. By leveraging **Neo4j**, the engine models bank accounts as *Nodes* and transactions as *Edges*. Instead of evaluating transactions in silos, Chakra-View computes real-time composite risk scores (0–100) using three advanced behavioral signals:

### 1.  Fan-In Analysis (Unmasking Unusual Inflows)
Examines how many unique, unrelated accounts are transferring funds into a single destination. While legitimate accounts (like local shopkeepers) might experience high fan-in, their transaction volumes are regular and consistent. A sudden explosion of unique senders to a personal account is a critical indicator of a mule node.

### 2.  Velocity Analysis (Money Dwell Time)
Measures the speed at which funds are drained from an account after being received. Fraud syndicates aim for rapid movement to break audit trails. Chakra-View tracks the precise time gap between inflows and subsequent outflows.

### 3.  Cluster Detection (Coordinated Networks)
Identifies accounts deeply embedded within larger transaction loops. Fraudsters distribute risk across multiple structured profiles to maintain money flow even if one account gets flagged. 

---

##  Comprehensive Risk Scoring Model
Individual signals can sometimes produce false positives. Chakra-View's true strength lies in its **Holistic Risk Matrix**. The engine aggregates metrics into a singular score capped at 100:

- **High Fan-In + Large Network Size** triggers a high risk score, even if money velocity is artificially delayed by scammers trying to bypass simple detection triggers.
- **Actionable Outputs:** Based on the risk threshold, the engine immediately outputs structural actions for the bank infrastructure:
  - 🛑 **Hold Transaction** (High Risk)
  - ⚠️ **Alert Fraud Analyst Team** (Medium-High Risk)
  - 🔔 **Warn User** (Suspicious Pattern Match)

---

##  System Architecture & Tech Stack

- **Backend Logic / Processing:** [Node.js / Python / Express]
- **Graph Database:** Neo4j (Cypher Query Language)
- **Frontend Analyst Dashboard:** [React.js / HTML / Tailwind CSS ]

---

##  The Architect

- **Nihari Akilandeswari** — End-to-End System Architect
  *Designed, engineered, and implemented the entire project solo, including backend services, graph database data modeling, and risk scoring logic.*


---
*Chakra-View doesn’t accuse users. It connects transaction behavior patterns to expose mule activity before money disappears.*
