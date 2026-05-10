from kafka import KafkaConsumer, KafkaProducer
from datetime import datetime
import json, requests

consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers='broker:9092',
    auto_offset_reset='earliest',
    group_id='ml-scoring',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

alert_producer = KafkaProducer(
    bootstrap_servers='broker:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

API_URL = "http://localhost:8001/score"

for message in consumer:
    tx = message.value

    # Wyciągnij cechy
    hour = tx.get('hour', None)
    if hour is None:
        hour = datetime.fromisoformat(tx['timestamp']).hour

    features = {
        'amount': tx['amount'],
        'is_electronics': 1 if tx['category'] == 'elektronika' else 0,
        'tx_per_minute': 12 if hour < 6 else 5
    }

    # Odpytaj API
    response = requests.post(API_URL, json=features)
    result = response.json()

    if result['is_fraud']:
        alert = {**tx, **result}
        alert_producer.send('alerts', value=alert)
        print(f"🚨 ML ALERT | {tx['tx_id']} | {tx['amount']:.2f} PLN | prob={result['fraud_probability']:.2f}")