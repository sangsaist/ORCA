# ORCA Digital Twin Design Specification

**Project:** ORCA – Onboard Resource Conflict Arbitrator

**Version:** 1.0

**Status:** Design Frozen (Phase 1)

---

## 1. Purpose

The ORCA Digital Twin is a lightweight systems-engineering model of a software-defined multi-payload Low Earth Orbit (LEO) satellite.

Its purpose is **not** to reproduce spacecraft physics with high fidelity, but to generate realistic spacecraft telemetry that can be consumed by the ORCA Edge AI resource management engine.

The Digital Twin executes at **1 Hz** and continuously updates the spacecraft state based on environmental conditions, payload activity, and resource utilization.

---

## 2. 0Digital Twin Architecture

``
  
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
``

---

## 3. Spacecraft Assumptions

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

## 4. Simulation Configuration

Simulation Frequency

* 1 update / second

Execution

* Local Python Simulation

Programming Language

* Python

Target Platform

* Windows Laptop

---

## 5. Battery Model

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

✅ Ready for implementation

---

## 6. Solar Model

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

✅ Ready for implementation

---

## 7. Payload Model

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

✅ Ready for implementation

---

## 8. Power Bus Model

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

✅ Ready for implementation

---

## 9. Thermal Model

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

✅ Ready for implementation

---

## 10. RF Margin Model

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

✅ Ready for implementation

---

## 11. Telemetry Generator

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

✅ Ready for implementation

---

## 12. Simulation Loop

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

## 13. Validation Strategy

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

## 14. Assumptions & Limitations

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

## 15. Python Module Structure

``
Not yet defined
``

---

## 16. Current Development Status

| Module               | Status      |
| -------------------- | ------------|
| Architecture         | ✅ Complete |
| Design Specification | ✅ Complete |
| Battery Model        | ⏳ Pending  |
| Solar Model          | ⏳ Pending  |
| Payload Model        | ⏳ Pending  |
| Power Bus            | ⏳ Pending  |
| Thermal Model        | ⏳ Pending  |
| RF Margin Model      | ⏳ Pending  |
| Telemetry Generator  | ⏳ Pending  |
| Simulator            | ⏳ Pending  |

---

## 17. Next Milestone

Implement the Digital Twin modules in the following order:

1. Battery Model
2. Solar Model
3. Payload Model
4. Power Bus Model
5. Thermal Model
6. RF Margin Model
7. Telemetry Generator
8. Simulator
