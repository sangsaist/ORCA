"""
battery_model
----------------
Battery subsystem for the ORCA Digital Twin.

The model maintains the spacecraft battery state by tracking
energy storage, charging, and discharging based on the net
power balance supplied by the Power Bus.
"""

from .config import (
    BATTERY_CAPACITY_WH,
    BATTERY_INITIAL_SOC,
    BATTERY_CHARGE_EFFICIENCY,
    BATTERY_DISCHARGE_EFFICIENCY,
    BUS_VOLTAGE,
    TIME_STEP,
)

class BatteryModel:
    """
    Simplified spacecraft battery model.
    """

    def __init__(self):
        # Battery properties
        self.capacity_wh = BATTERY_CAPACITY_WH
        self.soc = BATTERY_INITIAL_SOC

        # Current stored energy (Wh)
        self.energy_wh = (self.soc / 100.0) * self.capacity_wh

        # Electrical state
        self.voltage = BUS_VOLTAGE
        self.current = 0.0

    def update(self, net_power):
        """
        Update battery state.

        Parameters
        ----------
        net_power : float
            Positive -> battery charging
            Negative -> battery discharging
        """

        # Apply efficiency
        if net_power >= 0:
            battery_power = net_power * BATTERY_CHARGE_EFFICIENCY
        else:
            battery_power = net_power / BATTERY_DISCHARGE_EFFICIENCY

        # Convert W -> Wh
        energy_change = battery_power * (TIME_STEP / 3600.0)

        # Update stored energy
        self.energy_wh += energy_change

        # Clamp energy
        self.energy_wh = max(
            0.0,
            min(self.energy_wh, self.capacity_wh)
        )

        # Update State of Charge
        self.soc = (self.energy_wh / self.capacity_wh) * 100.0

        # Battery current
        self.current = battery_power / BUS_VOLTAGE

        # Simple voltage estimation
        self.voltage = BUS_VOLTAGE + (self.soc * 0.04)

    def get_soc(self):
        return round(self.soc, 2)

    def get_voltage(self):
        return round(self.voltage, 2)

    def get_current(self):
        return round(self.current, 2)

    def get_available_energy(self):
        return round(self.energy_wh, 2)

    def get_state(self):
        """
        Return battery telemetry.
        """

        return {
            "soc": self.get_soc(),
            "voltage": self.get_voltage(),
            "current": self.get_current(),
            "energy_wh": self.get_available_energy(),
        }