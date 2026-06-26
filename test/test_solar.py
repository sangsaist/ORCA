import sys
import os

sys.path.append(os.path.abspath("src"))

from digital_twin.solar_model import SolarModel

solar = SolarModel()

test_points = [
    0,
    500,
    1000,
    1710,
    2500,
    3419,
    3420,
    4000,
    5000,
    5700,
]

for t in test_points:

    solar.update(t)

    print(
        f"Time: {t:4d}s | "
        f"Phase: {solar.get_orbit_phase():9s} | "
        f"Power: {solar.get_power():7.2f} W"
    )