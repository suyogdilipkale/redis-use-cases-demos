# upi_limits_management.ipynb

import redis
import json
from datetime import timedelta

# Redis Enterprise Connection (use appropriate credentials)
r = redis.Redis(
    host='localhost', port=6379,
    decode_responses=True  # for string responses
)

# -------------------------------
# Configurable UPI Limits
# -------------------------------

UPI_LIMITS = {
    'balance_checks': 50,
    'bank_list_views': 25,
    'status_checks': 3
}

TTL_24H = 86400
TTL_TXN_STATUS = 900  # 15 min for pending txns

# -------------------------------
# Helper: Check & Increment Limit
# -------------------------------

def increment_limit(key, max_limit, ttl=TTL_24H):
    current = r.get(key)
    if current is None:
        r.set(key, 1, ex=ttl)
        return True, 1
    elif int(current) < max_limit:
        r.incr(key)
        return True, int(current) + 1
    else:
        return False, int(current)

# -------------------------------
# 1. Balance Check (max 50/day)
# -------------------------------

def balance_check(user_id):
    key = f"user:{user_id}:balance_checks"
    allowed, count = increment_limit(key, UPI_LIMITS['balance_checks'])
    return allowed, f"Balance checks used: {count}/50"

# -------------------------------
# 2. Linked Bank Account Views (max 25/day)
# -------------------------------

def view_linked_banks(user_id):
    key = f"user:{user_id}:bank_list_views"
    allowed, count = increment_limit(key, UPI_LIMITS['bank_list_views'])
    return allowed, f"Bank views used: {count}/25"

# -------------------------------
# 3. Transaction Status Check (max 3 per txn, 90 sec gap)
# -------------------------------

def check_txn_status(user_id, txn_id):
    key = f"user:{user_id}:txn:{txn_id}:status_checks"
    field = 'count'
    timestamp_field = 'last_check_ts'

    pipeline = r.pipeline()
    pipeline.hget(key, field)
    pipeline.hget(key, timestamp_field)
    count, last_ts = pipeline.execute()

    if count is None:
        # First time
        pipeline.hset(key, mapping={'count': 1, 'last_check_ts': r.time()[0]})
        pipeline.expire(key, TTL_TXN_STATUS)
        pipeline.execute()
        return True, "First check allowed"
    elif int(count) < UPI_LIMITS['status_checks']:
        now = r.time()[0]
        if last_ts is None or (now - int(last_ts)) >= 90:
            pipeline.hincrby(key, field, 1)
            pipeline.hset(key, timestamp_field, now)
            pipeline.execute()
            return True, f"Check allowed. Count: {int(count)+1}/3"
        else:
            return False, f"Wait before retrying. {90 - (now - int(last_ts))}s left"
    else:
        return False, f"Limit exceeded. Used: {count}/3"

# -------------------------------
# 4. Insert/Delete Payee Audit Logs using RedisJSON
# -------------------------------

def log_payee_check(user_id, txn_id, payee_name, status='confirmed'):
    key = f"user:{user_id}:payee_checks:{txn_id}"
    payload = {
        'payee': payee_name,
        'status': status,
        'ts': r.time()[0]
    }
    r.execute_command('JSON.SET', key, '.', json.dumps(payload))
    r.expire(key, TTL_TXN_STATUS)
    return f"Logged payee check for txn {txn_id}"

def delete_payee_log(user_id, txn_id):
    key = f"user:{user_id}:payee_checks:{txn_id}"
    r.delete(key)
    return f"Deleted log for txn {txn_id}"

# -------------------------------
# 5. Simulate User Events
# -------------------------------

def simulate_user_flow():
    user_id = 'user123'
    txn_id = 'txnABC001'

    print(balance_check(user_id))
    print(view_linked_banks(user_id))

    for _ in range(4):
        print(check_txn_status(user_id, txn_id))

    print(log_payee_check(user_id, txn_id, 'Rahul Sharma'))
    print(delete_payee_log(user_id, txn_id))

simulate_user_flow()
