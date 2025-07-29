
# Beneficiary List Management with Redis Enterprise

## 📌 Overview

This project demonstrates how to implement a **Beneficiary List feature** for a mobile banking interface using **Redis Enterprise** as a primary data store. It supports:

- Add / Edit / Delete Beneficiary per `customerId` or `accountId`
- Quick search (by name, mobile, IFSC, etc.)
- Advanced search (by bank, type, date added, etc.)
- Paginated listing of beneficiaries

## 🚧 Challenges with Traditional RDBMS

| Challenge | Description |
|----------|-------------|
| 💥 Latency | Querying and joining multiple normalized tables impacts performance |
| 🔍 Limited Search | Full-text search or partial match requires heavy indexes or custom logic |
| ⚖️ Scalability | Horizontal scaling is complex and costly |
| 🔄 Real-time Updates | Propagating updates in real time across regions/data centers is difficult |
| 📉 Performance | Insert/update heavy workloads increase contention and locking issues |
| 🔁 Multi-region Consistency | Managing consistency for active-active apps is complex |
| 🔐 Security | Adding data-at-rest encryption, role-based access, etc., increases ops burden |

## ✅ Why Redis Enterprise

| Feature | Benefit |
|--------|---------|
| 🧠 **RedisJSON** | Store rich beneficiary records in structured JSON format |
| 🔍 **RedisSearch** | Query on any field with full-text, prefix, numeric, geo, and fuzzy match |
| ⚙️ **High Throughput** | In-memory speed for real-time updates, lookups, and search |
| ↔️ **Horizontal Scale** | Scale reads and writes linearly with Redis Cluster |
| 🔄 **Active-Active (CRDT)** | Multi-Region write capability without conflicts |
| 💾 **Persistence** | Data durability using AOF or RDB snapshotting |
| 🛡️ **Security** | TLS encryption, role-based access control (RBAC), IP filtering |
| 📊 **Observability** | Real-time monitoring, alerting, slow log for operations |

## 🧩 Redis Schema

Each record is stored as RedisJSON under a key:

```
beneficiary:<customerId>:<beneficiaryId>
```

### Sample JSON Record

```json
{
  "beneficiaryId": "b12345",
  "accountId": "acc789",
  "customerId": "cust001",
  "name": "Ravi Mehta",
  "bankName": "HDFC Bank",
  "ifsc": "HDFC0000123",
  "mobile": "9876543210",
  "type": "internal",
  "dateAdded": "2025-07-29T08:30:00Z"
}
```

### Index Definition (RediSearch)

```
beneficiary_idx ON JSON PREFIX 1 beneficiary: SCHEMA
  $.beneficiaryId AS beneficiaryId TAG
  $.accountId AS accountId TAG
  $.customerId AS customerId TAG
  $.name AS name TEXT
  $.bankName AS bankName TEXT
  $.ifsc AS ifsc TEXT
  $.mobile AS mobile TAG
  $.type AS type TAG
  $.dateAdded AS dateAdded TEXT
```

## 🚀 Use Case Flows

1. **Add Beneficiary**: Insert new JSON document with RedisJSON
2. **Edit Beneficiary**: Update existing document by modifying JSON fields
3. **Delete Beneficiary**: Delete the Redis key
4. **Quick Search**: Full-text search on name/IFSC/mobile
5. **Advanced Search**: Filter by bankName, type, and date range
6. **Paginated List**: Use RediSearch `LIMIT` clause

## 📈 Redis Enterprise Architecture

- **Sharded Redis Enterprise Cluster** for horizontal scale
- **Active-Active CRDT Deployment** across 2+ data centers
- **AOF persistence** with periodic snapshots (RDB)
- **TLS**, **Authentication**, **IP whitelisting**, **Role-based Access Control**

## 🔐 Security with Redis Enterprise

- **TLS Encryption** for client-server communication
- **Role-based Access Control** (RBAC) via ACLs
- **IP Access Control Lists** for tenant isolation
- **Authentication** via Redis AUTH or IAM roles
- **Audit Logging** via Redis Enterprise logs

## 📦 Running the Demo

```bash
pip install redis
python redis_beneficiary_demo.py
```

Ensure RedisJSON and RediSearch modules are enabled on Redis Enterprise.
