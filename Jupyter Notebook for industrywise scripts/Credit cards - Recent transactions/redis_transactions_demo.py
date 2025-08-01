import redis
import decimal
import json
from redis.commands.search.query import Query
from redis.commands.search.field import TextField, NumericField, TagField, GeoField
from redis.commands.search.index_definition import IndexDefinition, IndexType
from datetime import datetime
import random
from faker import Faker
import re

def escape_tag_value(value):
    return re.sub(r'([,{}\s])', r'\\\1', value)
# Setup
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
fake = Faker()

def create_index():
    try:
        r.ft("idx:transactions").create_index(
            fields=[
                TagField("$.accountId", as_name="accountId"),
                TagField("$.customerId", as_name="customerId"),
                NumericField("$.amount", as_name="amount"),
                TagField("$.currency", as_name="currency"),
                TextField("$.merchant", as_name="merchant"),
                TagField("$.category", as_name="category"),
                TextField("$.timestamp", as_name="timestamp"),
                GeoField("$.location", as_name="location")
            ],
            definition=IndexDefinition(prefix=["txn:"], index_type=IndexType.JSON)
        )
    except redis.ResponseError:
        print("Index already exists")

def add_dummy_transactions(n=100):
    for i in range(n):
        txn = {
            "transactionId": f"tx{i}",
            "accountId": f"acc{random.randint(1, 5)}",
            "customerId": f"cust{random.randint(1, 3)}",
            "amount": float(round(random.uniform(10, 5000), 2)),
            "currency": "INR",
            "merchant": fake.company(),
            "timestamp": datetime.utcnow().isoformat(),
            "category": random.choice(["Shopping", "Travel", "Grocery", "Fuel", "Dining"]),
            "location": f"{round(fake.longitude(), 6)},{round(fake.latitude(), 6)}",
            "status": "SUCCESS"
        }
        r.json().set(f"txn:{i}", "$", sanitize_for_json(txn))

def list_recent_transactions(account_id, limit=10):
    q = Query(f"@accountId:{{{account_id}}}")\
        .sort_by("timestamp", asc=False)\
        .paging(0, limit)\
        .return_fields("transactionId", "amount", "merchant", "timestamp", "location", "category")
    return r.ft("idx:transactions").search(q).docs
    
def quick_search(account_id, keyword):
    q = Query(f"@accountId:{{{account_id}}} @category:{{{keyword}}}")\
        .paging(0, 10)\
        .return_fields("transactionId", "amount", "merchant", "timestamp", "location", "category")
    return r.ft("idx:transactions").search(q).docs

def geo_search(account_id, lat, lon, radius_km=50):
    q = Query(f"@accountId:{{{account_id}}} @location:[{lon} {lat} {radius_km} km]")\
        .paging(0, 10)\
        .return_fields("transactionId", "amount", "merchant", "timestamp", "location", "category")
    return r.ft("idx:transactions").search(q).docs

def sanitize_for_json(obj):
    if isinstance(obj, dict):
        return {k: sanitize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_for_json(elem) for elem in obj]
    elif isinstance(obj, decimal.Decimal):
        return float(obj)
    else:
        return obj
        
# Run demo
create_index()
last_long=None
last_lat=None
add_dummy_transactions(100)
print("=== Recent Transactions for acc1 ===")
for txn in list_recent_transactions("acc1"):
    last_long, last_lat = txn.location.split(',')
    print(txn.id, txn.timestamp, txn.amount, txn.merchant, txn.category, txn.location)

print("\n=== Quick Search for 'Travel' ===")
for txn in quick_search("acc1", "Travel"):
     print(txn.id, txn.timestamp, txn.amount, txn.merchant, txn.category, txn.location)

print("\n=== Geo Search near Mumbai ===")
print(last_long, last_lat)
for txn in geo_search("acc1", last_lat, last_long):
    print(txn.id, txn.timestamp, txn.amount, txn.merchant, txn.category, txn.location)
