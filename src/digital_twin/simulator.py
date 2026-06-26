"""
simulator.py
------------
Master Simulator for the ORCA Digital Twin.

Coordinates every subsystem and executes the spacecraft
simulation at a fixed 1 Hz time step.
"""

from .config import ORBIT_PERIOD

from .battery_model import BatteryModel
from .solar_model import SolarModel
from .payload_model import PayloadModel
from .power_bus import PowerBusModel
from .thermal_model import ThermalModel
from .rf_model import RFModel
from .telemetry import TelemetryGenerator


class SpacecraftSimulator:

    def __init__(self):

        # -----------------------------------
        # Simulation Clock
        # -----------------------------------

        self.sim_time = 0
        self.orbit_counter = 0

        # -----------------------------------
        # Subsystems
        # -----------------------------------

        self.battery = BatteryModel()

        self.solar = SolarModel()

        self.payload = PayloadModel()

        self.power_bus = PowerBusModel()

        self.thermal = ThermalModel()

        self.rf = RFModel()

        self.telemetry = TelemetryGenerator()

    # -----------------------------------
    # Reset
    # -----------------------------------

    def reset(self):

        self.sim_time = 0
        self.orbit_counter = 0

        self.__init__()

    # -----------------------------------
    # Single Simulation Step
    # -----------------------------------

    def step(self, payload_commands=None):

        if payload_commands is None:
            payload_commands = {}

        # Advance simulation clock

        self.sim_time += 1

        orbit_time = self.sim_time % ORBIT_PERIOD

        if orbit_time == 0:
            self.orbit_counter += 1

        # -----------------------------------
        # 1. Solar
        # -----------------------------------

        self.solar.update(orbit_time)

        # -----------------------------------
        # 2. Payload
        # -----------------------------------

        self.payload.update(payload_commands)

        # -----------------------------------
        # 3. Power Bus
        # -----------------------------------

        self.power_bus.update(

            solar_power=self.solar.get_power(),

            payload_power=self.payload.get_total_power(),

            battery_soc=self.battery.get_soc()

        )

        # -----------------------------------
        # 4. Battery
        # -----------------------------------

        self.battery.update(

            self.power_bus.get_net_power()

        )

        # -----------------------------------
        # 5. Thermal
        # -----------------------------------

        self.thermal.update(

            total_load=self.power_bus.get_total_load(),

            orbit_phase=self.solar.get_orbit_phase()

        )

        # -----------------------------------
        # 6. RF
        # -----------------------------------

        self.rf.update(

            self.payload.get_states()

        )

        # -----------------------------------
        # 7. Telemetry
        # -----------------------------------

        packet = self.telemetry.generate(

            battery=self.battery,

            solar=self.solar,

            payload=self.payload,

            power_bus=self.power_bus,

            thermal=self.thermal,

            rf=self.rf,

        )

        packet["simulation_time"] = self.sim_time

        packet["orbit_time"] = orbit_time

        packet["orbit_counter"] = self.orbit_counter

        return packet

    # -----------------------------------
    # Run Simulation
    # -----------------------------------

    def run(self, duration, mission_events=None):

        if mission_events is None:
            mission_events = {}

        history = []

        commands = {}

        for _ in range(duration):

            if self.sim_time in mission_events:

                commands.update(

                    mission_events[self.sim_time]

                )

            packet = self.step(commands)

            history.append(packet)

        return history