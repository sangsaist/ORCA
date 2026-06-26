import sys
import os

sys.path.append(os.path.abspath("src"))

from digital_twin.payload_model import PayloadModel

payload = PayloadModel()

print("========== INITIAL ==========")
print(payload.get_state())

print("\n========== PNT ACTIVE ==========")

payload.update({
    "PNT": "ACTIVE"
})

print(payload.get_state())

print("\n========== SATCOM TX ==========")

payload.update({
    "SATCOM": "TX_ACTIVE"
})

print(payload.get_state())

print("\n========== ALL PAYLOADS ==========")

payload.update({
    "PNT": "ACTIVE",
    "SATCOM": "TX_ACTIVE",
    "EARTH_OBSERVATION": "ACTIVE",
    "EDGE_AI": "PROCESSING"
})

print(payload.get_state())