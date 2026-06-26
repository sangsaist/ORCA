"""
thermal_model
----------------
Thermal subsystem for the ORCA Digital Twin.

Models the spacecraft as a single lumped thermal node.
Temperature changes based on internal power consumption,
environmental heating, and passive cooling.
"""

from .config import (
    INITIAL_TEMPERATURE,
    THERMAL_CAPACITANCE,
    THERMAL_RADIATION,
    SOLAR_HEATING,
    WARNING_TEMPERATURE,
    CRITICAL_TEMPERATURE,
    TIME_STEP,
)


class ThermalModel:
    """
    Simplified spacecraft thermal model.
    """

    def __init__(self):

        # Configuration
        self.thermal_capacitance = THERMAL_CAPACITANCE

        # Cooling coefficient (W/°C)
        self.cooling_factor = THERMAL_RADIATION

        # Environmental heating
        self.solar_heating = SOLAR_HEATING

        # Reference operating temperature
        self.reference_temperature = INITIAL_TEMPERATURE

        # Limits
        self.warning_temperature = WARNING_TEMPERATURE
        self.critical_temperature = CRITICAL_TEMPERATURE

        # State
        self.temperature = INITIAL_TEMPERATURE
        self.status = "NOMINAL"

        self.heat_in = 0.0
        self.heat_out = 0.0

    def update(self, total_load, orbit_phase):
        """
        Update spacecraft thermal state.

        Parameters
        ----------
        total_load : float
            Total spacecraft electrical load (Watts)

        orbit_phase : str
            "SUNLIGHT" or "ECLIPSE"
        """

        # ---------------------------------
        # Environmental heating
        # ---------------------------------

        environmental_heat = (
            self.solar_heating
            if orbit_phase == "SUNLIGHT"
            else 0.0
        )

        # ---------------------------------
        # Internal heat generation
        # ---------------------------------

        self.heat_in = total_load + environmental_heat

        # ---------------------------------
        # Passive cooling
        #
        # Cooling begins only after the
        # spacecraft rises above its nominal
        # operating temperature.
        # ---------------------------------

        self.heat_out = max(
            0.0,
            (self.temperature - self.reference_temperature)
            * self.cooling_factor
        )

        # ---------------------------------
        # First-order thermal model
        # ---------------------------------

        dT_dt = (
            self.heat_in - self.heat_out
        ) / self.thermal_capacitance

        self.temperature += dT_dt * TIME_STEP

        # ---------------------------------
        # Thermal Status
        # ---------------------------------

        if self.temperature >= self.critical_temperature:

            self.status = "CRITICAL"

        elif self.temperature >= self.warning_temperature:

            self.status = "WARNING"

        else:

            self.status = "NOMINAL"

        return self.temperature

    # ---------------------------------
    # Getter Functions
    # ---------------------------------

    def get_temperature(self):
        return round(self.temperature, 2)

    def get_status(self):
        return self.status

    def get_heat_in(self):
        return round(self.heat_in, 2)

    def get_heat_out(self):
        return round(self.heat_out, 2)

    # ---------------------------------
    # Telemetry
    # ---------------------------------

    def get_state(self):

        return {
            "temperature": self.get_temperature(),
            "thermal_status": self.get_status(),
            "heat_in": self.get_heat_in(),
            "heat_out": self.get_heat_out(),
        }