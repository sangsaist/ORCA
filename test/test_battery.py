import sys
import os

sys.path.append(os.path.abspath("src"))

from digital_twin.battery_model import BatteryModel

battery = BatteryModel()

print("========== INITIAL ==========")
print(battery.get_state())

print("\n========== DISCHARGING ==========")

for i in range(10):
    battery.update(-150)

print(battery.get_state())

print("\n========== CHARGING ==========")

for i in range(10):
    battery.update(200)

print(battery.get_state())