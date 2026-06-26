import sys
import os

sys.path.append(os.path.abspath("src"))

from digital_twin.power_bus import PowerBusModel

power_bus = PowerBusModel()

print("========== CASE 1 ==========")

power_bus.update(
    solar_power=420,
    payload_power=100,
    battery_soc=80,
)

print(power_bus.get_state())

print("\n========== CASE 2 ==========")

power_bus.update(
    solar_power=0,
    payload_power=300,
    battery_soc=65,
)

print(power_bus.get_state())

print("\n========== CASE 3 ==========")

power_bus.update(
    solar_power=20,
    payload_power=350,
    battery_soc=15,
)

print(power_bus.get_state())