"""
telemetry
------------
Telemetry Generator for the ORCA Digital Twin.

Collects telemetry from every subsystem and generates a
single telemetry packet every simulation step.
"""


class TelemetryGenerator:

    def __init__(self):

        self.packet_id = 0
        self.timestamp = 0

    def generate(
        self,
        battery,
        solar,
        payload,
        power_bus,
        thermal=None,
        rf=None,
    ):
        """
        Generate a complete telemetry packet.

        Parameters
        ----------
        battery : BatteryModel

        solar : SolarModel

        payload : PayloadModel

        power_bus : PowerBusModel

        thermal : ThermalModel (optional)

        rf : RFModel (optional)
        """

        self.packet_id += 1
        self.timestamp += 1

        packet = {

            # Packet Header
            "packet_id": self.packet_id,
            "timestamp": self.timestamp,
        }

        # Merge subsystem telemetry

        packet.update(battery.get_state())

        packet.update(solar.get_state())

        packet.update(payload.get_state())

        packet.update(power_bus.get_state())

        # Thermal (optional)

        if thermal is not None:

            packet.update(thermal.get_state())

        # RF (optional)

        if rf is not None:

            packet.update(rf.get_state())

        return packet