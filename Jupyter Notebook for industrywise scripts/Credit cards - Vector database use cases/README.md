# 🚀 Redis Vector Database Use Cases in Banking - Credit Card Domain

This repository demonstrates how Redis Enterprise can be used to solve advanced **vector search use cases** in the **banking credit card** ecosystem. It includes Jupyter notebooks, schema definitions, and Redis Stream integrations.

---

## 📘 Use Cases Overview

### 1. 🧠 Personalized Credit Card Offers

#### 🔴 Challenges with RDBMS:
- No support for vector-based similarity search.
- Complex joins reduce performance for real-time recommendation.
- Difficult to integrate personalization logic using embeddings.

#### ✅ Redis Enterprise Approach:
- Customer profiles are vectorized and stored using `RedisJSON`.
- `RediSearch` indexes vectors for KNN (k-nearest neighbor) search.
- Query by vector to serve real-time personalized offers.

---

### 2. 🔒 Fraud Detection Using Transaction Embeddings

#### 🔴 Challenges with RDBMS:
- High-latency queries on large historical datasets.
- No efficient way to store and search transactional behavior patterns using embeddings.
- No stream processing for real-time anomaly detection.

#### ✅ Redis Enterprise Approach:
- Transactional data is ingested through `Redis Streams`.
- A consumer processes and stores vector embeddings using `RedisJSON`.
- Semantic vector queries detect anomalies by comparing with fraud vector patterns.

---

### 3. 🗣️ Semantic Customer Support Search

#### 🔴 Challenges with RDBMS:
- Limited support for semantic or fuzzy text matching.
- Slow full-text search; no deep context matching.
- Inflexible metadata + unstructured query combination.

#### ✅ Redis Enterprise Approach:
- Support queries and responses are vectorized.
- Indexed using `RediSearch` for hybrid semantic + metadata querying.
- Real-time semantic search on user questions improves support experience.

---

## ⚙️ Redis Enterprise Advantages

| Feature                           | Benefit                                                                 |
|----------------------------------|-------------------------------------------------------------------------|
| `RedisJSON`                      | Store structured JSON + vector fields in a single key                   |
| `RediSearch`                     | Combine metadata, full-text, and vector queries                         |
| `Redis Streams`                  | Real-time ingestion and processing of transactional embeddings          |
| **Horizontal Scaling**           | Seamless scale-out across shards and nodes                              |
| **High Availability**            | Auto failover, multi-AZ/multi-region deployments                        |
| **Active-Active**                | Multi-data-center sync using CRDTs                                      |
| **Persistence**                  | AOF and RDB for durability with fast recovery                           |
| **Security**                     | TLS, ACL, Role-based Access, and SOC2/ISO certifications                |

---

## 📦 Project Structure

redis-credit-vector/
├── README.md
├── requirements.txt
├── notebooks/
│ ├── 1_offer_semantic_search.ipynb
│ ├── 2_fraud_detection_semantic.ipynb
│ └── 3_support_query_semantic.ipynb
└── redis_schema/
├── index_creation.py
├── stream_ingestion.py
└── stream_consumer.py

---

## 🧪 Example Vector Schema

```json
{
  "customer_id": "12345",
  "embedding": [0.23, 0.67, ..., 0.12],
  "segment": "platinum",
  "last_activity_ts": 1729573981
}
```
Use HNSW index for fast vector retrieval and add filters like segment, status, and geography.

---

## 📌 Best Practices

| Area            | Recommendation                                                    |
| --------------- | ----------------------------------------------------------------- |
| Vector Storage  | Use `FLOAT32` with normalized vectors                             |
| Indexing        | Use HNSW with filterable tags and range fields                    |
| Query Precision | Tune `K`, `EF_RUNTIME`, `EF_CONSTRUCTION` in RediSearch           |
| Data Sync       | Use RedisGears or Streams for online ingestion                    |
| Hybrid Search   | Combine vector search with JSON filters for better targeting      |
| Security        | Use ACLs for different microservices and enable TLS for transport |
| Durability      | Enable append-only file (AOF) with fsync for critical workloads   |
