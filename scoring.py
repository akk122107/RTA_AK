def score_transaction(tx):
    score = 0
    rules = []

    # R1 — duża kwota
    if tx['amount'] > 3000:
        score += 3
        rules.append('R1: kwota > 3000')

    # R2 — elektronika i duża kwota
    if tx['category'] == 'elektronika' and tx['amount'] > 1500:
        score += 2
        rules.append('R2: elektronika > 1500')

    # R3 — godzina nocna
    hour = tx.get('hour', None)
    if hour is None:
        from datetime import datetime
        hour = datetime.fromisoformat(tx['timestamp']).hour
    if hour < 6:
        score += 2
        rules.append('R3: godzina nocna')

    return score, rules

# Test
test_tx = {
    'tx_id': 'TX999',
    'amount': 4500.0,
    'category': 'elektronika',
    'hour': 3,
    'timestamp': '2026-04-01T03:15:00'
}

score, rules = score_transaction(test_tx)
print(f"Score: {score} | Reguły: {rules}")
print("PODEJRZANA!" if score >= 3 else "OK")