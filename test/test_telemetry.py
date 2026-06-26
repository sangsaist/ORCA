import sys
import os

sys.path.append(os.path.abspath("src"))

from digital_twin.telemetry import TelemetryGenerator
from digital_twin.battery_model import BatteryModel
from digital_twin.solar_model import SolarModel
from digital_twin.payload_model import PayloadModel
from digital_twin.power_bus import PowerBusModel

battery = BatteryModel()
solar = SolarModel()
payload = PayloadModel()
power_bus = PowerBusModel()

telemetry = TelemetryGenerator()

solar.update(1200)

payload.update({
    "PNT": "ACTIVE",
    "SATCOM": "STANDBY"
})

power_bus.update(
    solar.get_power(),
    payload.get_total_power(),
    battery.get_soc()
)

battery.update(power_bus.get_net_power())

packet = telemetry.generate(
    battery,
    solar,
    payload,
    power_bus,
)

print(packet)