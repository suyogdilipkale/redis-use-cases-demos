import redis
from redis.commands.json.path import Path
from redis.commands.search.field import TextField, TagField
from redis.commands.search.index_definition import IndexDefinition, IndexType
from redis.commands.search.query import Query
import uuid
import datetime
import json

r = redis.Redis(host='redis-19205.c330.asia-south1-1.gce.redns.redis-cloud.com', port=19205,password='admin', decode_responses=True)

def create_index():
    try:
        r.ft("beneficiary_idx").create_index(
            fields=[
                TagField("$.beneficiaryId", as_name="beneficiaryId"),
                TagField("$.accountId", as_name="accountId"),
                TagField("$.customerId", as_name="customerId"),
                TextField("$.name", as_name="name"),
                TextField("$.bankName", as_name="bankName"),
                TextField("$.ifsc", as_name="ifsc"),
                TagField("$.mobile", as_name="mobile"),
                TagField("$.type", as_name="type"),
                TextField("$.dateAdded", as_name="dateAdded")
            ],
            definition=IndexDefinition(prefix=["beneficiary:"], index_type=IndexType.JSON)
        )
    except Exception as e:
        print(f"Index already exists or error: {e}")

def add_or_update_beneficiary(customer_id, data):
    beneficiary_id = data.get("beneficiaryId") or str(uuid.uuid4())
    key = f"beneficiary:{customer_id}:{beneficiary_id}"
    data["beneficiaryId"] = beneficiary_id
    data["customerId"] = customer_id
    data["dateAdded"] = data.get("dateAdded") or datetime.datetime.utcnow().isoformat()
    r.json().set(key, Path.root_path(), data)
    return beneficiary_id

def delete_beneficiary(customer_id, beneficiary_id):
    key = f"beneficiary:{customer_id}:{beneficiary_id}"
    return r.delete(key)

def quick_search(term, limit=10):
    q = Query(f"@name:{term}* | @ifsc:{term}* | @mobile:{term}*").paging(0, limit)
    return r.ft("beneficiary_idx").search(q).docs

def advanced_search(customer_id=None, bank=None, type=None, limit=10):
    query_parts = []
    if customer_id:
        query_parts.append(f"@customerId:{{{customer_id}}}")
    if bank:
        query_parts.append(f"@bankName:{bank}")
    if type:
        query_parts.append(f"@type:{{{type}}}")
    final_query = " ".join(query_parts) or "*"
    q = Query(final_query).paging(0, limit)
    print(q)
    return r.ft("beneficiary_idx").search(q).docs

def load_dummy_data():
    data_samples = [
        {"name": "Ravi Mehta", "bankName": "HDFC Bank", "ifsc": "HDFC0000123", "mobile": "9876543210", "type": "internal", "accountId": "acc001"},
        {"name": "Anjali Rao", "bankName": "SBI", "ifsc": "SBIN0000456", "mobile": "9123456789", "type": "external", "accountId": "acc001"},
        {"name": "Rohit Das", "bankName": "ICICI", "ifsc": "ICIC0000789", "mobile": "9988776655", "type": "internal", "accountId": "acc002"},
        {"name": "Subhash Kumar", "bankName": "HDFC Bank", "ifsc": "HDFC0000003", "mobile": "9876543410", "type": "internal", "accountId": "acc001"},
        {"name": "Anil Rao", "bankName": "SBI", "ifsc": "SBIN0000006", "mobile": "9123456489", "type": "external", "accountId": "acc001"},
        {"name": "Rohit Das", "bankName": "ICICI", "ifsc": "ICIC0000700", "mobile": "9988776455", "type": "internal", "accountId": "acc002"},
    ]
    for record in data_samples:
        add_or_update_beneficiary("cust001", record)

if __name__ == "__main__":
    create_index()
    load_dummy_data()

    print("\n🔍 Quick Search for 'Ravi'")
    results = quick_search("Ravi")
    for re in results:
        print(json.dumps(re.__dict__, indent=2))

    print("\n🔎 Advanced Search for internal type")
    adv_results = advanced_search(customer_id="cust001", type="internal")
    for re in adv_results:
        print(json.dumps(re.__dict__, indent=2))
