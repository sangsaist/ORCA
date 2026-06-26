"""
payload_model
----------------
Payload subsystem for the ORCA Digital Twin.

Represents the operational state and power consumption of
spacecraft payloads.

"""

from .config import PAYLOADS


class PayloadModel:
    """
    Simplified spacecraft payload model.
    """

    def __init__(self):
        # Payload definitions from config
        self.payloads = PAYLOADS

        # Current payload states
        self.states = {
            "PNT": "OFF",
            "SATCOM": "OFF",
            "EARTH_OBSERVATION": "OFF",
            "EDGE_AI": "OFF",
        }

        # State-to-power lookup tables
        self.power_map = {
            "PNT": {
                "OFF": 0.0,
                "ACTIVE": self.payloads["PNT"]["power"],
            },
            "SATCOM": {
                "OFF": 0.0,
                "STANDBY": 15.0,
                "TX_ACTIVE": self.payloads["SATCOM"]["power"],
            },
            "EARTH_OBSERVATION": {
                "OFF": 0.0,
                "ACTIVE": self.payloads["EARTH_OBSERVATION"]["power"],
            },
            "EDGE_AI": {
                "OFF": 0.0,
                "STANDBY": 10.0,
                "PROCESSING": self.payloads["EDGE_AI"]["power"],
            },
        }

        self.total_power = 0.0

    def update(self, commands: dict):
        """
        Update payload operating states.

        Parameters
        ----------
        commands : dict

        Example
        -------
        {
            "PNT":"ACTIVE",
            "SATCOM":"TX_ACTIVE"
        }
        """

        # Update requested states
        for payload, state in commands.items():

            if payload in self.power_map:

                if state in self.power_map[payload]:

                    self.states[payload] = state

        # Compute total payload power
        self.total_power = 0.0

        for payload, state in self.states.items():
            self.total_power += self.power_map[payload][state]

        return self.total_power

    def get_total_power(self):
        """Return total payload power."""
        return round(self.total_power, 2)

    def get_states(self):
        """Return payload operating states."""
        return self.states.copy()

    def get_state(self):
        """
        Return payload telemetry.
        """

        return {
            "payload_power": self.get_total_power(),
            "payload_states": self.get_states(),
        }