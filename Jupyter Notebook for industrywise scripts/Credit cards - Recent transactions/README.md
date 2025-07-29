# Credit Card Recent Transactions - Redis Enterprise Implementation

## Overview

This project demonstrates how to implement a high-performance, scalable, and feature-rich **Recent Transactions List** service for credit card systems using **Redis Enterprise**.

The service supports:

- 📄 Listing transactions by Account ID or Customer ID
- 🔍 Quick and Advanced Search (date, amount, merchant, etc.)
- 📍 Geospatial Queries (by transaction location)
- 📑 Pagination Support

...

## 🧠 Redis Use Cases for Transactions List

| Use Case | Description |
|----------|-------------|
| **Personalized Recommendations** | Suggest merchants or categories based on past transactions using Redis sorted sets and tags. |
| **Fraud Detection** | Detect abnormal spending patterns or geo-locations using Redis Streams + Alerts. |
| **Statement Generation** | Aggregate transactions for user/month using RedisJSON & pipelines. |
| **EMI Offers** | Flag high-value purchases in eligible categories. |
| **Alerts & Notifications** | Push alerts in real time using Redis Pub/Sub. |
