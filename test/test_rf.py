import sys
import os

sys.path.append(os.path.abspath("src"))

from digital_twin.rf_model import RFModel

rf = RFModel()

print("========== SCENARIO 1 ==========")

states = {

    "PNT": "ACTIVE",
    "SATCOM": "OFF",
    "EARTH_OBSERVATION": "OFF",
    "EDGE_AI": "OFF"

}

rf.update(states)

print(rf.get_state())


print("\n========== SCENARIO 2 ==========")

states = {

    "PNT": "ACTIVE",
    "SATCOM": "TX_ACTIVE",
    "EARTH_OBSERVATION": "OFF",
    "EDGE_AI": "OFF"

}

rf.update(states)

print(rf.get_state())


print("\n========== SCENARIO 3 ==========")

states = {

    "PNT": "ACTIVE",
    "SATCOM": "TX_ACTIVE",
    "EARTH_OBSERVATION": "ACTIVE",
    "EDGE_AI": "PROCESSING"

}

rf.update(states)

print(rf.get_state())