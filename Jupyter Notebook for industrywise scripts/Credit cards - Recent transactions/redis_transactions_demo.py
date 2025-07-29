import redis
import json
from redis.commands.search.query import Query
from redis.commands.search.field import TextField, NumericField, TagField, GeoField
from redis.commands.search.index_definition import IndexDefinition, IndexType
from datetime import datetime
import random
from faker import Faker

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
            "amount": round(random.uniform(10, 5000), 2),
            "currency": "INR",
            "merchant": fake.company(),
            "timestamp": datetime.utcnow().isoformat(),
            "category": random.choice(["Shopping", "Travel", "Grocery", "Fuel", "Dining"]),
            "location": {
                "lat": round(fake.latitude(), 6),
                "lon": round(fake.longitude(), 6)
            },
            "status": "SUCCESS"
        }
        r.json().set(f"txn:{i}", "$", txn)

def list_recent_transactions(account_id, limit=10):
    q = Query(f"@accountId:{{{account_id}}}").sort_by("timestamp", asc=False).paging(0, limit)
    return r.ft("idx:transactions").search(q).docs

def quick_search(account_id, keyword):
    q = Query(f"@accountId:{{{account_id}}} @merchant:{keyword} | @category:{keyword}").paging(0, 10)
    return r.ft("idx:transactions").search(q).docs

def geo_search(account_id, lat, lon, radius_km=50):
    q = Query(f"@accountId:{{{account_id}}} @location:[{lon} {lat} {radius_km} km]").paging(0, 10)
    return r.ft("idx:transactions").search(q).docs

# Run demo
create_index()
add_dummy_transactions(100)

print("=== Recent Transactions for acc1 ===")
for txn in list_recent_transactions("acc1"):
    print(txn.id, txn.amount, txn.merchant)

print("\n=== Quick Search for 'Amazon' ===")
for txn in quick_search("acc1", "Amazon"):
    print(txn.id, txn.merchant)

print("\n=== Geo Search near Mumbai ===")
for txn in geo_search("acc1", 19.0760, 72.8777):
    print(txn.id, txn.location)
