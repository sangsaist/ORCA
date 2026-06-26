import sys
import os

sys.path.append(os.path.abspath("src"))

from digital_twin.simulator import SpacecraftSimulator

sim = SpacecraftSimulator()

mission = {

    0: {

        "PNT": "ACTIVE"

    },

    10: {

        "SATCOM": "TX_ACTIVE"

    },

    20: {

        "EARTH_OBSERVATION": "ACTIVE"

    },

    30: {

        "EDGE_AI": "PROCESSING"

    }

}

history = sim.run(

    duration=40,

    mission_events=mission

)

for packet in history:

    print(

        f'T={packet["simulation_time"]:3d}s | '

        f'SoC={packet["soc"]:6.2f}% | '

        f'Solar={packet["solar_power"]:7.2f}W | '

        f'Load={packet["total_load"]:7.2f}W | '

        f'Temp={packet["temperature"]:6.2f}°C | '

        f'RF={packet["rf_status"]:9s}'

    )