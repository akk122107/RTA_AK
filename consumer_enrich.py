from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers='broker:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for message in consumer:
    tx = message.value
    amount = tx['amount']
    
    if amount > 3000:
        risk_level = 'HIGH'
    elif amount > 1000:
        risk_level = 'MEDIUM'
    else:
        risk_level = 'LOW'
    
    print(f"[{risk_level}] {tx['tx_id']} | {amount:.2f} PLN | {tx['store']} | {tx['category']}")