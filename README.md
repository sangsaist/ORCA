# ORCA

> **Onboard Resource Conflict Arbitrator**

ORCA is an Edge AI research project that explores **autonomous onboard resource management** for future software-defined satellites.

Instead of relying on predefined operating schedules and continuous ground intervention, ORCA aims to make spacecraft capable of allocating their own onboard resources while respecting electrical, thermal, and RF constraints.

The project combines a lightweight spacecraft **Digital Twin** with an onboard decision engine that will autonomously determine which payloads should operate at any given time.

---

# Motivation

Future spacecraft are becoming increasingly software-defined.

A single satellite may simultaneously host:

* Navigation (PNT)
* Satellite Communications (SatCom)
* Earth Observation payloads
* Onboard AI processors

These payloads compete for limited spacecraft resources including:

* Electrical Power
* Battery Energy
* Thermal Capacity
* RF Spectrum
* Onboard Compute

Traditional spacecraft typically resolve these conflicts using fixed schedules designed before launch.

ORCA investigates whether these decisions can instead be performed autonomously onboard using Edge AI.

---

# Project Objectives

* Develop a lightweight Digital Twin of a multi-payload LEO satellite
* Generate realistic spacecraft telemetry in real time
* Model key spacecraft resource constraints
* Provide a simulation environment for autonomous resource scheduling
* Build an onboard AI resource arbitrator

---
---
# Architecture 

                 ORCA

        Spacecraft Digital Twin
                  │
             Telemetry Engine
                  │
         Operational Scenarios
                  │
      ┌───────────┴───────────┐
      │                       │
 Rule-Based Scheduler   ORCA Decision Engine
      │                       │
      └───────────┬───────────┘
                  │
          Safety Supervisor
                  │
        Approved Commands
                  │
         Spacecraft State
                  │
          Metrics & Logger
                  │
             Dashboard

---
# Current Progress

## ✅ Phase 1 — Digital Twin

The Digital Twin has been implemented and currently includes:

* Battery Model
* Solar Power Model
* Payload Model
* Electrical Power Bus
* Thermal Model
* RF Coexistence Model
* Telemetry Generator
* Spacecraft Simulator

These modules execute together at a fixed **1 Hz simulation rate** and continuously generate spacecraft telemetry.

---

## 🚧 Phase 2 — ORCA Decision Engine

The next phase focuses on developing the onboard intelligence responsible for autonomous resource arbitration.

Planned capabilities include:

* Autonomous payload scheduling
* Mission-aware decision making
* Battery-aware power allocation
* Thermal constraint management
* RF conflict avoidance
* Priority-based resource optimization
* Explainable decision logging

---

# Repository Structure

```text
ORCA/
│
├── src/
│   └── digital_twin/
│       ├── battery_model.py
│       ├── solar_model.py
│       ├── payload_model.py
│       ├── power_bus.py
│       ├── thermal_model.py
│       ├── rf_model.py
│       ├── telemetry.py
│       ├── simulator.py
│       └── config.py
│
├── test/
│
├── docs/
│   └── digital_twin_design.md
│
├── README.md
│
└── LICENSE
```

---

# Quick Start

Clone the repository:

```bash
git clone https://github.com/sangsaist/ORCA.git
```

Navigate into the project:

```bash
cd ORCA
```

Run the Digital Twin simulator:

```bash
python test/test_simulator.py
```

---

# Example Output

```text
T=10s

Battery SoC : 99.89 %

Solar Power : 4.13 W

Total Load  : 186.32 W

Temperature : 20.56 °C

RF Status   : SAFE
```

Mission events dynamically modify payload activity, causing changes in electrical load, battery state, thermal conditions, and RF coexistence.

---

# Technology Stack

* Python
* Object-Oriented Design
* Systems Engineering
* Digital Twin Architecture
* Edge AI (Planned)

---

## Documentation

Detailed engineering documentation is available in:

```text
docs/
└── digital_twin_design.md
```

This document describes the architecture, engineering assumptions, subsystem models, and implementation rationale behind the Digital Twin.

---

## Project Roadmap

* ✅ Digital Twin
* 🔄 Autonomous Decision Engine
* ⏳ Mission Planning
* ⏳ Dashboard & Visualization
* ⏳ Reinforcement Learning Integration
* ⏳ Hardware-in-the-Loop Support

---

## Disclaimer

ORCA is a systems-engineering research prototype.

The Digital Twin is intentionally simplified and is designed for autonomous resource scheduling research rather than high-fidelity spacecraft physics simulation.

---

## License

This project is released for research and educational purposes.

