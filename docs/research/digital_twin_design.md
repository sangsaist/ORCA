# ORCA Digital Twin Design Specification

**Project:** ORCA – Onboard Resource Conflict Arbitrator

**Version:** 1.0

**Status:** Design Frozen (Phase 1)

---

# 1. Purpose

The ORCA Digital Twin is a lightweight systems-engineering model of a software-defined multi-payload Low Earth Orbit (LEO) satellite.

Its purpose is **not** to reproduce spacecraft physics with high fidelity, but to generate realistic spacecraft telemetry that can be consumed by the ORCA Edge AI resource management engine.

The Digital Twin executes at **1 Hz** and continuously updates the spacecraft state based on environmental conditions, payload activity, and resource utilization.

---

# 2. 0Digital Twin Architecture

```

              Simulation Loop
                      │
      ┌───────────────┼───────────────┐
      │               │               │
 Battery Model   Solar Model   Payload Model
      │               │               │
      └───────────────┼───────────────┘
                      │
               Power Bus Model
                      │
      ┌───────────────┼───────────────┐
      │                               │
 Thermal Model                RF Margin Model
      │                               │
      └───────────────┼───────────────┘
                      │
            Telemetry Generator
                      │
                     ORCA
```

---

# 3. Spacecraft Assumptions

Mission Type

* Multi-payload software-defined satellite

Orbit

* Low Earth Orbit (LEO)
* Circular Orbit
* Approximate Orbit Period: 95 minutes

Payloads

* Position Navigation and Timing (PNT)
* SatCom
* Earth Observation
* AI Compute Module

Simulation Rate

* 1 Hz

Purpose

* Demonstrate autonomous onboard resource allocation

---

# 4. Simulation Configuration

Simulation Frequency

* 1 update / second

Execution

* Local Python Simulation

Programming Language

* Python

Target Platform

* Windows Laptop

---

# 5. Battery Model

Purpose

Maintain spacecraft energy storage.

Inputs

* Net Power
* Simulation Time Step

Outputs

* State of Charge
* Battery Voltage
* Battery Current
* Available Energy

Simplified Model

Energy Balance Model

State of Charge updates every simulation cycle.

Assumptions

* Ignore battery aging
* Ignore cell balancing
* Ignore electrochemical behaviour
* Constant efficiency

Status

✅ Implemented v1

---

# 6. Solar Model

Purpose

Generate electrical power during sunlight.

Inputs

* Orbit Phase

Outputs

* Solar Power

Simplified Model

Sunlight

↓

Power Generation

Eclipse

↓

Zero Generation

Assumptions

* Ignore degradation
* Ignore pointing errors
* Ignore seasonal effects

Status

✅ Implemented v1

---

# 7. Payload Model

Purpose

Represent payload operating states and power consumption.

Payloads

* PNT
* SatCom
* Earth Observation
* AI Compute

Outputs

* Payload Status
* Payload Power

Assumptions

* Instant ON/OFF
* Constant power consumption

Status

✅ Implemented v1

---

# 8. Power Bus Model

Purpose

Distribute spacecraft electrical power.

Inputs

* Solar Power
* Payload Power

Outputs

* Net Power
* Battery Charging
* Battery Discharging

Simplified Equation

Net Power

=

Solar Generation

−

Total Power Consumption

Status

✅ Implemented v1

---

# 9. Thermal Model

Purpose

Estimate spacecraft thermal state.

Inputs

* Payload Power
* Orbit Phase

Outputs

* Core Temperature

Simplified Model

Temperature

=

Previous Temperature

*

Generated Heat

−

Cooling

Assumptions

* Lumped thermal node
* Ignore detailed conduction paths
* Ignore radiation modelling

Status

✅ Implemented v1

---

# 10. RF Margin Model

Purpose

Estimate RF coexistence margin between active payloads.

Inputs

* Active Payloads
* Mission Mode

Outputs

* RF Margin

States

* SAFE
* WARNING
* CRITICAL

Assumptions

* Simplified coexistence model
* No electromagnetic simulation
* No antenna pattern modelling

Status

✅ Implemented v1

---

# 11. Telemetry Generator

Purpose

Generate spacecraft telemetry every second.

Telemetry Fields

* Timestamp
* Orbit Phase
* Battery SoC
* Battery Voltage
* Solar Power
* Net Power
* Payload Status
* Thermal State
* RF Margin
* Mission Mode

Output Format

Python Dictionary / JSON

Status

✅ Implemented v1

---

# 12. Simulation Loop

Execution Order

1. Update Orbit Phase
2. Solar Model
3. Payload Model
4. Power Bus
5. Battery Model
6. Thermal Model
7. RF Margin Model
8. Telemetry Generation
9. Send Telemetry to ORCA

Execution Rate

1 Hz

---

# 13. Validation Strategy

Battery

* Charges during sunlight
* Discharges during eclipse

Solar

* Generates power only during sunlight

Payload

* Correct power calculation

Power Bus

* Correct net power balance

Thermal

* Temperature increases under heavy load

RF

* Margin changes according to active payload combinations

Telemetry

* Valid packet generated every second

---

# 14. Assumptions & Limitations

This Digital Twin is intentionally simplified.

Included

* Resource usage
* Power flow
* Thermal estimation
* RF margin estimation
* Telemetry generation

Excluded

* Orbital propagation
* Battery chemistry
* High-fidelity thermal analysis
* Electromagnetic modelling
* Spacecraft attitude dynamics
* Radiation effects

These simplifications are acceptable because the objective is autonomous onboard resource management rather than spacecraft physics simulation.

---

# 15. Python Module Structure

``
Not yet defined
``

---

# 16. Current Development Status

| Module               | Status      |
| -------------------- | ------------|
| Architecture         | ✅ Complete |
| Design Specification | ✅ Complete |
| Battery Model        | ✅ Complete |
| Solar Model          | ✅ Complete |
| Payload Model        | ✅ Complete |
| Power Bus            | ✅ Complete |
| Thermal Model        | ⏳ Pending  |
| RF Margin Model      | ⏳ Pending  |
| Telemetry Generator  | ✅ Complete |
| Simulator            | ⏳ Pending  |

---

# 17. Next Milestone

Implement the Digital Twin modules in the following order:

1. Battery Model
2. Solar Model
3. Payload Model
4. Power Bus Model
5. Thermal Model
6. RF Margin Model
7. Telemetry Generator
8. Simulator

# 18. Reference

* Larson & Wertz, "Space Mission Analysis and Design (SMAD)", Third Edition. – Standard orbital geometries, electrical power subsystem design limits, and solar array equation guidelines.

* NASA Systems Engineering Handbook (NASA/SP-2016-6105). – System-level margin definitions and thermal/electrical baseline guidelines for spacecraft platforms.

* Gilmore, "Satellite Thermal Control Handbook". – Formulation guidelines for first-order lumped parameter thermal node networks in space system architectures.

* NASA Spacecraft Electrical Power Systems (NASA-HDBK-4002A): Baseline engineering methods for calculating orbital photovoltaic production margins and solar array geometry constraints.

* CubeSat Design Specification (CalPoly): Empirical design ranges for electrical output characteristics on small satellites.

* Space Mission Engineering: The New SMAD (Wertz et al.): Mathematical techniques for orbital period calculations and solar array sizing constants in LEO configurations.

* NASA Space Systems Resource Management (NASA-STD-7009A): Framework practices for separating structural hardware payload behaviors into lightweight modeling state engines.

* Small Satellite Conference Technical Papers (SSC22-WKV-04): Operational paradigms for software-defined payload resource duty cycling in LEO configurations.

* ESA European Cooperation for Space Standardization (ECSS-E-ST-20C): Electrical and electronic engineering specifications for space system distribution architectures.

* CCSDS 132.0-B-2, TM Space Data Link Protocol: Context practices for structuring spacecraft telemetry frames into predictable data fields.

* NASA Command and Data Handling Systems Architecture Guidelines: Recommended formatting approaches for telemetry synchronization blocks and error-free system monitoring fields.

* NASA Satellite Thermal Control Handbook (Gilmore): Core methodologies for deploying simplified first-order lumped mass thermal representations safely in low-fidelity test benches.

* ECSS-E-ST-20-07C (Space Engineering - Electromagnetic Compatibility): Standard safety margins and testing principles for modeling onboard self-interference and hardware integration limits.

* NASA Trick Simulation Environment Architecture Guidelines: Best practices for building deterministic aerospace software models using a fixed 1 Hz cyclic scheduling pipeline.

* ECSS-E-TM-10-21A (Space Engineering - System Modeling and Simulation): Standard engineering guidelines for structural synchronization and multi-subsystem discrete time-stepping.
