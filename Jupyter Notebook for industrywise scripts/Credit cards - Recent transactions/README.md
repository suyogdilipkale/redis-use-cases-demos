# Credit Card Recent Transactions - Redis Enterprise Implementation

## Overview

This project demonstrates how to implement a high-performance, scalable, and feature-rich **Recent Transactions List** service for credit card systems using **Redis Enterprise**.

The service supports:

- 📄 Listing transactions by Account ID or Customer ID
- 🔍 Quick and Advanced Search (date, amount, merchant, etc.)
- 📍 Geospatial Queries (by transaction location)
- 📑 Pagination Support

---

## 🔥 Challenges with Traditional RDBMS

| Challenge | Explanation |
|----------|-------------|
| **Scalability** | Scaling RDBMS for millions of transactions per user becomes costly and complex. |
| **Latency** | Joins, indexes, and complex search reduce performance for real-time use cases. |
| **Search Flexibility** | Full-text and faceted search are limited or require additional systems. |
| **Geo Queries** | Geospatial indexing is slower and more complex. |
| **HA/DR Setup** | Multi-DC setups require external tooling, replication tuning. |

---

## ✅ Redis Enterprise Advantages

| Feature | Benefit |
|--------|---------|
| **RedisJSON** | Natively store transactions as JSON documents. |
| **RediSearch** | Perform full-text and numeric range search with filters, faceting, geo-indexing. |
| **Horizontal Scaling** | Auto-shard and scale for high throughput. |
| **High Availability** | Built-in HA with 99.999% uptime. |
| **Active-Active** | CRDT-based multi-region deployments. |
| **Persistence** | Durable AOF + RDB persistence. |
| **Security** | Role-based access control (RBAC), TLS, VPC peering, audit logs. |

---

## 📦 Data Model

```json
{
  "transactionId": "tx123456",
  "accountId": "acc987",
  "customerId": "cust123",
  "amount": 999.99,
  "currency": "INR",
  "merchant": "Amazon",
  "timestamp": "2025-07-28T10:00:00Z",
  "category": "Shopping",
  "location": "72.8777,19.0760",
  "status": "SUCCESS"
}
```
---
## 🔍 Indexing with RediSearch
```
FT.CREATE idx:transactions ON JSON PREFIX 1 "txn:" SCHEMA
  $.accountId AS accountId TAG
  $.customerId AS customerId TAG
  $.amount AS amount NUMERIC
  $.currency AS currency TAG
  $.merchant AS merchant TEXT
  $.category AS category TAG
  $.timestamp AS timestamp TEXT
  $.location AS location GEO
```
---
## 🔧 Features

| Feature                  | Redis Component                |
| ------------------------ | ------------------------------ |
| Recent Transactions List | RedisJSON, Sorted Sets         |
| Quick Search             | RediSearch                     |
| Advanced Filter          | RediSearch Faceted Query       |
| Geo Search               | RediSearch GEO filter          |
| Pagination               | `.paging(offset, limit)`       |
| Multi-region Sync        | Redis Enterprise Active-Active |
| Secure Access            | RBAC, TLS, VPC Peering         |

---
## 🧠 Redis Use Cases for Transactions List

| Use Case                         | Description                                                                                  |
| -------------------------------- | -------------------------------------------------------------------------------------------- |
| **Personalized Recommendations** | Suggest merchants or categories based on past transactions using Redis sorted sets and tags. |
| **Fraud Detection**              | Detect abnormal spending patterns or geo-locations using Redis Streams + Alerts.             |
| **Statement Generation**         | Aggregate transactions for user/month using RedisJSON & pipelines.                           |
| **EMI Offers**                   | Flag high-value purchases in eligible categories.                                            |
| **Alerts & Notifications**       | Push alerts in real time using Redis Pub/Sub.                                                |

---

