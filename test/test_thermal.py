import sys
import os

sys.path.append(os.path.abspath("src"))

from digital_twin.thermal_model import ThermalModel

thermal = ThermalModel()

print("========== SUNLIGHT ==========")

for i in range(10):

    thermal.update(
        total_load=300,
        orbit_phase="SUNLIGHT"
    )

    print(thermal.get_state())

print("\n========== ECLIPSE ==========")

for i in range(10):

    thermal.update(
        total_load=60,
        orbit_phase="ECLIPSE"
    )

    print(thermal.get_state())