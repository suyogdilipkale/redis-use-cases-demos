Here is a complete technical approach document and a single Python Jupyter Notebook script using Redis Enterprise to implement and enforce the new UPI transaction limits per user (as effective from August 1, 2025). This includes inserting, updating, deleting, and expiring Redis keys.


# UPI Transaction Limit Enforcement Using Redis Enterprise

This project demonstrates how to enforce UPI transaction rules (effective August 1, 2025) using Redis Enterprise. It includes rate-limiting logic, TTL-based expiration, and RedisJSON audit logging for various UPI features like balance checks, transaction status queries, etc.

## 📌 UPI Rules Implemented

| Feature                     | Rule                                 |
|----------------------------|--------------------------------------|
| Balance Checks             | Max 50 checks/day                    |
| Linked Bank Account Views  | Max 25 views/day                     |
| Transaction Status Checks  | Max 3 per transaction, 90 sec apart  |
| Payee Name Audit Logs      | Logged via RedisJSON                 |

## 💡 Why Redis Enterprise?

- **High Availability (HA)**: Ensures fault tolerance for critical UPI operations
- **Persistence**: Guarantees recovery of transaction state across restarts
- **Active-Active Deployment**: Multi-region sync using CRDTs for global consistency
- **Enterprise Security**: TLS, ACLs, Role-based access control
- **Multi-model**: Uses Strings, Hashes, TTLs, RedisJSON for optimized modeling

## 🧱 Redis Data Modeling

| Use Case            | Data Type  | Key Pattern                          | TTL     |
|---------------------|------------|--------------------------------------|---------|
| Balance Check       | String     | user:{user_id}:balance_checks        | 24h     |
| Account Views       | String     | user:{user_id}:bank_list_views       | 24h     |
| Status Check        | Hash       | user:{user_id}:txn:{txn_id}:status_checks | 15 min  |
| Payee Audit Log     | RedisJSON  | user:{user_id}:payee_checks:{txn_id} | 15 min  |

## 🚀 Usage

Run the `upi_limits_management.ipynb` notebook to simulate user actions:
- Balance check
- Linked account views
- Status check enforcement (3 max with time gap)
- Logging and deleting payee verification logs

## 🛠 Requirements

- Redis Enterprise or Redis Stack (with RedisJSON module enabled)
- Python `redis` client

## 🧪 Example Output

```python
(True, 'Balance checks used: 1/50')
(True, 'Bank views used: 1/25')
(True, 'First check allowed')
(True, 'Check allowed. Count: 2/3')
(False, 'Limit exceeded. Used: 3/3')
'Logged payee check for txn txnABC001'
'Deleted log for txn txnABC001'
```

---

© 2025 Redis Enterprise Demo for UPI Compliance
