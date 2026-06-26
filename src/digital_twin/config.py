"""
ORCA Digital Twin Configuration
--------------------------------
Central configuration file containing all spacecraft constants
used by the Digital Twin simulation.

Project: ORCA (Onboard Resource Conflict Arbitrator)
"""


# SIMULATION CONFIGURATION
SIMULATION_RATE_HZ = 1          # Updates per second
TIME_STEP = 1.0                 # Seconds
ORBIT_PERIOD = 5700             # 95 minutes (seconds)

# ORBIT CONFIGURATION
ORBIT_ALTITUDE_KM = 550
SUNLIGHT_DURATION = 3420        # 57 minutes
ECLIPSE_DURATION = 2280         # 38 minutes


# ELECTRICAL POWER SYSTEM (EPS)
BUS_VOLTAGE = 28.0              # Volts
BATTERY_CAPACITY_WH = 500.0     # Watt-hours
BATTERY_INITIAL_SOC = 100.0     # %
BATTERY_CHARGE_EFFICIENCY = 0.92
BATTERY_DISCHARGE_EFFICIENCY = 0.95
ESSENTIAL_BUS_POWER = 60.0      # Watts


# SOLAR ARRAY
SOLAR_MAX_POWER = 450.0         # Watts


# PAYLOAD CONFIGURATION
PAYLOADS = {
    "PNT": {
        "power": 120,
        "priority": "CRITICAL",
        "default_state": "OFF"
    },
    "SATCOM": {
        "power": 180,
        "priority": "HIGH",
        "default_state": "OFF"
    },
    "EARTH_OBSERVATION": {
        "power": 200,
        "priority": "MEDIUM",
        "default_state": "OFF"
    },
    "EDGE_AI": {
        "power": 90,
        "priority": "LOW",
        "default_state": "OFF"
    }
}


# THERMAL MODEL
INITIAL_TEMPERATURE = 20.0          # °C
THERMAL_CAPACITANCE = 4000.0        # J/°C
SPACE_TEMPERATURE = -270.0          # °C
SOLAR_HEATING = 40.0                # Watts
THERMAL_RADIATION = 4.0             # W/°C
WARNING_TEMPERATURE = 45.0          # °C
CRITICAL_TEMPERATURE = 55.0         # °C


# RF MODEL
RF_SAFE = "SAFE"
RF_WARNING = "WARNING"
RF_CRITICAL = "CRITICAL"
RF_MARGIN_MAX = 12.0                # dB
RF_MARGIN_MIN = -100.0              # dB


# TELEMETRY
TELEMETRY_RATE = 1                  # Hz


# MISSION MODES
MISSION_IDLE = "IDLE"
MISSION_PNT = "PNT"
MISSION_EARTH_OBSERVATION = "EARTH_OBSERVATION"
MISSION_COMMUNICATION = "COMMUNICATION"
MISSION_EMERGENCY = "EMERGENCY"


# RF MODEL CONFIGURATION
RF_BASE_MARGIN = 12.0

RF_WARNING_MARGIN = 9.0

RF_CRITICAL_MARGIN = 4.0

RF_CONFLICT_MATRIX = {

    ("PNT", "ACTIVE", "SATCOM", "TX_ACTIVE"): 4.5,

    ("SATCOM", "TX_ACTIVE", "EARTH_OBSERVATION", "ACTIVE"): 2.0,

    ("EARTH_OBSERVATION", "ACTIVE", "EDGE_AI", "PROCESSING"): 0.5,

    ("PNT", "ACTIVE", "EARTH_OBSERVATION", "ACTIVE"): 0.0,

}