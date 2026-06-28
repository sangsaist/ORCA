# ORCA Operational Scenarios Research

**Project:** ORCA – Onboard Resource Conflict Arbitrator

**Version:** 1.0

**Status:** Research Phase (Phase 2)

---

## 1. Purpose

This document establishes a rigorous operational research framework for the Onboard Resource Conflict Arbitrator (ORCA) prototype. The objective is to identify, analyze, and catalog realistic Low Earth Orbit (LEO) spacecraft operational scenarios that introduce state-space resource contentions.

In advanced software-defined satellites, resource management must adapt dynamically to multi-payload requirements, varying environmental envelopes, and subsystem contingencies. Ground-generated, deterministic command timelines are increasingly unable to optimize or safely arbitrate these runtime interactions. By mapping these complexities into an authoritative scenario database, this research provides the deterministic and stochastic operational test vectors required to validate the ORCA Decision Engine inside a lightweight Digital Twin environment.

---

## 2. Background

The paradigm of modern spacecraft design is rapidly transitioning from single-mission, hardware-static configurations to multi-payload, **Software-Defined Satellites (SDS)**. These next-generation platforms leverage high-performance processing architectures, including Field Programmable Gate Arrays (FPGAs) and Radio Frequency System-on-Chips (RFSoCs), to dynamically reconfigure subsystem logic, communication waveforms, and instrument processing pipelines mid-mission.

Concurrently, the integration of multiple distinct payloads—such as Earth Observation (EO) imagers, Satellite Communications (SatCom) transponders, Positioning, Navigation, and Timing (PNT) receivers, and dedicated **Edge AI Compute** nodes—creates systemic resource dependencies. For example, executing computer vision models directly onboard for real-time hazard or cloud detection reduces ground-link latency and optimizes downlink data volumes.

However, these concurrent tasks compete for a rigid physical allocation of spacecraft resources. High-throughput processing creates localized thermal dissipation bottlenecks; transmission windows generate electromagnetic interference (EMI); and rapid observation slews demand significant peak power. Because ground station passes in LEO are infrequent (typically 8–12 minutes per window) and subject to latency, ground control cannot resolve transient, real-time resource contentions.

Mitigating these issues requires onboard edge autonomy. An autonomous arbitrator must evaluate the instantaneous state of the satellite, predict short-horizon resource trends, and resolve scheduling conflicts while preserving platform health and mission priorities.

---

## 3. Scope

This document serves as an operational systems engineering reference for scenario modeling within the ORCA ecosystem.

### 3.1 Included in Scope

* Conceptual definition of multi-variable resource contentions across power, thermal, RF, and mission control domains.
* Mapping of parametric telemetry inputs and expected onboard decision logic trees.
* Categorization of scenarios into immediate deployment (ORCA v1) and future expansion phases.
* Verification that scenarios conform to established space agency guidelines (NASA, ESA, ECSS, CCSDS).

### 3.2 Excluded from Scope

* High-fidelity structural mechanics, finite element analysis (FEA), and low-level computational fluid dynamics (CFD).
* Complex orbital mechanics propagation (e.g., non-spherical Earth gravity perturbations, precise ballistic coefficients for atmospheric drag).
* Low-level software code implementations, database schemas, or communication register definitions.
* Continuous physical equations operating outside a discrete 1 Hz simulator step interval.

---

## 4. ORCA Digital Twin Overview

The ORCA Digital Twin is designed as a discrete-time, lumped-parameter simulation framework operating at a baseline execution rate of 1 Hz. It does not attempt to simulate precise, continuous physics; instead, it tracks the state-space transitions and resource consumption metrics of the satellite's core subsystems.

### 4.1 Functional Architecture

```
+-------------------------------------------------------------------------+
|                          SPACECRAFT SIMULATOR                           |
|       (1 Hz Discrete Time-Step Engine / Environmental Flag Driver)       |
+-------------------------------------------------------------------------+
         |                        |                       |
         v                        v                       v
+-----------------+      +-----------------+     +-----------------+
|   SOLAR MODEL   |      |  BATTERY MODEL  |     |  THERMAL MODEL  |
| (Efficiency/    |      | (Coulomb Count/ |     | (Lumped Mass Nodes/|
|  Sun Vector)    |      |  V-I Impedance) |     |  Dissipation)   |
+-----------------+      +-----------------+     +-----------------+
         |                        |                       |
         +------------------------+-----------------------+
                                  |
                                  v
                       +---------------------+
                       | ELECTRICAL POWER BUS|
                       | (Load Summation /   |
                       |  Switch Isolation)  |
                       +---------------------+
                                  |
         +------------------------+-----------------------+
         |                        |                       |
         v                        v                       v
+-----------------+      +-----------------+     +-----------------+
|  PAYLOAD MODEL  |      | RF MARGIN MODEL |     |TELEMETRY GEN.   |
| (EO / SatCom /  |      | (Attenuation /  |     | (CCSDS Packet-  |
|  PNT / Edge AI) |      |  Co-site Noise) |     |  ized Stream)   |
+-----------------+      +-----------------+     +-----------------+
                                                          |
                                                          v
                                                 [To ORCA Decision Engine]

```

The subsystem modules operate under the following parameters:

* **Solar Power Model:** Computes generation wattage using a step-function sun visibility flag (Eclipse/Sunlight) and parameterized solar panel degradation factors.
* **Battery Model:** Simulates capacity via a simplified linear Coulomb-counting method, adjusting internal cell impedance and voltage thresholds as a function of temperature and state of charge (SoC).
* **Electrical Power Bus:** Summates individual subsystem and payload current draws against a rigid voltage rail, triggering under-voltage or over-current trip states if thresholds are breached.
* **Thermal Model:** Tracks localized temperature trends using a coarse, multi-node lumped mass heat transfer approximation ($C_{th} \frac{dT}{dt} = Q_{in} - Q_{out}$).
* **RF Margin Model:** Evaluates link margins and signal degradation using pre-calculated co-site attenuation lookup matrices to identify receiver desensitization.
* **Payload Model:** Emulates operational state-machines (Off, Standby, Operational, Fault) and data generation trends for the four primary software-defined payload architectures.
* **Telemetry Generator:** Compiles subsystem parameter vectors into structured, discrete packets matching CCSDS formatting principles for intake by the arbitrator.

---

## 5. Resource Conflict Philosophy

The core architectural tenet of the ORCA subsystem is that **onboard autonomy must treat resource arbitration as a multi-dimensional utility maximization problem under strict constraint boundaries**. Spacecraft operations are fundamentally defined by overlapping bottlenecks:

### 5.1 The Power-Thermal-RF Dependency Loop

When a payload changes state from Standby to Operational, it acts as an electrical load on the Power Bus, drawing energy from either the Solar Model or the Battery Model. Unused electrical energy is dissipated as heat, raising the node temperature within the Thermal Model. Simultaneously, RF transmissions alter the RF Margin Model, potentially degrading adjacent payload receivers.

### 5.2 The Role of ORCA

ORCA evaluates these cross-subsystem interactions at every 1 Hz clock cycle. Its objective is to arbitrate scheduling conflicts by tracking resource consumption against soft warning thresholds and hard safety limits. If a conflict arises—such as an ongoing task threatening to exceed a thermal limit or cause an under-voltage event—ORCA must modify the payload schedule, adjust duty cycles, or reallocate power based on instantaneous mission priorities.

---

## 6. Scenario Classification

To validate the resource-allocation and anomaly-handling performance of the arbitrator, operational scenarios are structured into ten distinct technical domains:

1. **Power Management (PWR):** Transient imbalances on the main power bus and load-shedding responses.
2. **Battery Management (BAT):** Chemical capacity shifts and variations in deep discharge states.
3. **Thermal Management (THM):** Heat accumulation from high-duty-cycle payloads and localized thermal boundary violations.
4. **RF & Communications (COM):** Inter-payload signal degradation and regulatory transmission boundaries.
5. **Payload Operations (PLD):** Concurrent processing demands and software-defined payload reconfigurations.
6. **Mission Operations (OPS):** Conflicts between pre-scheduled ground commands and real-time onboard opportunities.
7. **Fault Management (FLT):** Unexpected subsystem component degradation, latch-ups, and isolation routines.
8. **Environmental Operations (ENV):** Direct external changes in solar flux, orbital variations, and orbital shadow entry.
9. **Spacecraft Health (HLTH):** Long-term degradations affecting subsystem trends and efficiency parameters.
10. **Future Autonomous Operations (AUT):** Multi-agent coordination and complex multi-satellite networking tasks.

---

## 7. Operational Scenario Research

### 7.1 Scenario PWR-01: Main Power Bus Overload / High Transient Load Spikes

* **Mission Context:** Simultaneous initialization of software-defined payload components (e.g., powering up the SatCom transmitter amplifiers while the Edge AI compute node initializes a neural network memory allocation) causes a transient current draw that tests the headroom of the power regulation system.
* **Trigger:** Overlapping operational duty cycles of two high-power subsystems.
* **Resources Affected:** Electrical Power Bus, Available System Margin.
* **Telemetry Changes:** `BUS_CURRENT` spikes above warning limits; `BUS_VOLTAGE` exhibits a brief transient dip; `BATTERY_CURRENT` switches to high discharge.
* **Operational Decisions:** Stagger subsystem initialization sequences; delay the non-time-critical payload startup routine by a predefined time horizon to level the power profile.
* **Digital Twin Compatibility:** Yes. Modeled as a multi-channel current summation step function.
* **ORCA Compatibility:** Yes (ORCA v1 Candidate). Tests time-domain load interleaving.
* **Implementation Complexity:** Low.
* **Engineering Notes:** Essential for validating that the arbitrator can mitigate voltage sags before hard hardware protection breakers trip.
* **References:** ECSS-E-ST-20C (Spacecraft Electrical Power).

### 7.2 Scenario BAT-01: Deep Eclipse High-Discharge Capacity Collapse

* **Mission Context:** During long-duration orbital eclipses, the spacecraft relies entirely on chemical battery storage. Sustained operation of the processing array accelerates battery depletion, pushing the state of charge down into a non-linear voltage drop curve.
* **Trigger:** Spacecraft Simulator sets the solar illumination flag to zero while payloads maintain a high power draw.
* **Resources Affected:** Battery Model capacity, Main Power Bus stability.
* **Telemetry Changes:** `BATTERY_SOC` decreases below a 40% warning threshold; `BATTERY_CELL_VOLTAGE` trends downward toward a critical bus drop limit.
* **Operational Decisions:** Transition non-essential payloads (Edge AI background image processing) to Standby or Off; reduce the SatCom duty cycle; enforce a low-power housekeeping profile until orbital dawn.
* **Digital Twin Compatibility:** Yes. Utilizes the discrete Coulomb counter and parameterized V-I state lookup matrices.
* **ORCA Compatibility:** Yes (ORCA v1 Candidate). Tests state-of-charge tracking and safety-first constraint optimization.
* **Implementation Complexity:** Medium.
* **References:** Space Mission Engineering: The New SMAD (Battery discharge profile models).

### 7.3 Scenario THM-01: Edge AI Compute Acceleration Core Thermal Overload

* **Mission Context:** High-throughput onboard image processing using specialized hardware accelerators generates significant localized heat. If the processing duration outpaces the structural thermal dissipation paths, the component temperature will approach its maximum operational limit.
* **Trigger:** Edge AI Compute payload runs high-duty-cycle inference tasks continuously for an extended duration.
* **Resources Affected:** Thermal Model (Compute Node), Edge AI payload availability.
* **Telemetry Changes:** `NODE_TEMP_EDGE_AI` exceeds the high-temperature alert threshold; local thermal gradient metrics increase.
* **Operational Decisions:** Throttle processing frame rates (duty-cycling $<50\%$); temporarily pause inference pipelines; divert raw data into local memory storage to allow thermal cooling.
* **Digital Twin Compatibility:** Yes. Evaluated using a multi-node lumped-parameter thermal inertia algorithm.
* **ORCA Compatibility:** Yes (ORCA v1 Candidate). Validates core arbitration between processing throughput and hardware thermal boundaries.
* **Implementation Complexity:** High. Requires predictive calculation of thermal trends.
* **References:** NASA Systems Engineering Handbook (Thermal margin structures).

### 7.4 Scenario THM-02: Payload Structural Cold Soak During Prolonged Inactivity

* **Mission Context:** When an Earth Observation payload remains inactive across multiple orbits, its internal optical components cool down due to passive radiation into deep space, potentially misaligning optical mounts.
* **Trigger:** Extended period of payload inactivity coupled with minimal structural heating.
* **Resources Affected:** Thermal Model (Optical Payload Node), Electrical Power Bus.
* **Telemetry Changes:** `NODE_TEMP_EO_OPTICS` drops below its minimum operational threshold.
* **Operational Decisions:** Activate local patch survival heaters; reallocate electrical power from non-essential background tasks to ensure the thermal control system maintains optical alignment.
* **Digital Twin Compatibility:** Yes. Simulated as a negative thermal power injection paired with thermostat switch rules.
* **ORCA Compatibility:** Yes (ORCA v1 Candidate). Tests multi-variable optimization where power must be spent on environmental control instead of payload execution.
* **Implementation Complexity:** Medium.
* **References:** ESA Mission Operations Publications (Rosetta/LEO spacecraft thermal balancing).

### 7.5 Scenario COM-01: Co-Site RF Harmonic Desensitization (SatCom vs. PNT)

* **Mission Context:** High-power SatCom downlinks can generate harmonic frequencies or signal leakage that enters the sensitive front-end of the onboard PNT receiver, raising its noise floor and disrupting signal tracking.
* **Trigger:** Co-scheduled execution of a SatCom data transmission pass and a PNT signal observation window.
* **Resources Affected:** RF Margin Model, PNT Payload functionality.
* **Telemetry Changes:** `PNT_SIGNAL_TO_NOISE_RATIO` (SNR) drops significantly; `RF_DESENSE_FLAG` switches to True; data packet errors increment.
* **Operational Decisions:** Apply Time-Division Multiplexing (TDM) to separate payload execution windows; restrict transmitter output power during critical tracking passes.
* **Digital Twin Compatibility:** Yes. Managed via an internal mutual interference compatibility matrix.
* **ORCA Compatibility:** Yes (ORCA v1 Candidate). Confirms ORCA's ability to handle multi-variable mutual exclusion constraints.
* **Implementation Complexity:** Low.
* **References:** CCSDS Standards for Space Link Protocols.

### 7.6 Scenario COM-02: Regulatory Transmission Cease-Fire (RF Silent Geofence)

* **Mission Context:** Satellites must strictly cease transmissions on specific radio frequencies when passing over designated ground locations (e.g., radio astronomy reserves or international boundaries without licensing rights) to comply with telecommunication regulations.
* **Trigger:** Ground simulation engine sets an RF geofence boundary violation flag.
* **Resources Affected:** SatCom Payload state, RF Margin Model.
* **Telemetry Changes:** `GEOFENCE_VIOLATION_ALERT` = True; `SATCOM_TRANSMITTER_POWER` forced to zero.
* **Operational Decisions:** Suspend ongoing SatCom data downlinks; buffer generated mission telemetry to local storage; shift remaining power headroom to compute operations.
* **Digital Twin Compatibility:** Yes. Modeled as a coordinate-triggered state override event flag.
* **ORCA Compatibility:** Yes (ORCA v1 Candidate). Validates enforcement of regulatory constraints over scheduling efficiency.
* **Implementation Complexity:** Low.
* **References:** ITU Radio Regulations for Space Services.

### 7.7 Scenario PLD-01: Multi-Payload Mission Profile Scheduling Conflict

* **Mission Context:** Concurrent operational requests occur over a specific geographic target. The Earth Observation payload requires stable power and platform pointing to capture imagery, while the PNT sensor requires active background compute capability to catalog localized signals.
* **Trigger:** Overlapping scheduling requests from different mission control centers.
* **Resources Affected:** Payload Model states, Power Bus capacity, Telemetry processing bandwidth.
* **Telemetry Changes:** `RESOURCE_REQUEST_CONFLICT` flag = True; calculated aggregate power usage exceeds instantaneous capacity limits.
* **Operational Decisions:** Parse the relative mission priority weights; dynamically allocate structural resources to the higher-priority payload while degrading or delaying the secondary request.
* **Digital Twin Compatibility:** Yes. Implemented via dual command queue ingestion inputs.
* **ORCA Compatibility:** Yes (ORCA v1 Candidate). Validates basic programmatic priority evaluation.
* **Implementation Complexity:** Medium.
* **References:** Space Mission Analysis and Design (SMAD) (Mission planning and scheduling).

### 7.8 Scenario PLD-02: Software-Defined Payload Reconfiguration Failure & Hang

* **Mission Context:** Modifying an FPGA payload pipeline (e.g., reconfiguring a SatCom router from an IoT mesh to a high-rate transponder) involves uploading a new bitstream. A memory read error or transient bit-flip can stall the boot process, leaving the payload in an unresponsive, high-power state.
* **Trigger:** Reconfiguration timeout flag trips without receiving a valid payload hand-shake signal.
* **Resources Affected:** Payload Model state-machine, Electrical Power Bus stability.
* **Telemetry Changes:** `PAYLOAD_STATUS_WORD` indicates a hung configuration state; `CHANNEL_CURRENT` remains high without data processing indicators.
* **Operational Decisions:** Command a hard power-cycle to the affected payload switch; fall back to a safe backup boot image; reallocate the remaining observation time window to alternative payloads.
* **Digital Twin Compatibility:** Yes. Represented as a state-machine fault injection driven by the simulator engine.
* **ORCA Compatibility:** Yes (ORCA v1 Candidate). Confirms that the arbitrator can adapt schedules when a system resource fails.
* **Implementation Complexity:** Medium.
* **References:** NASA Trick Simulation Environment Case Studies.

### 7.9 Scenario OPS-01: Ground Command Verification Timeline Conflict

* **Mission Context:** A rigid command sequence uploaded during a previous ground station pass conflicts with real-time operational constraints encountered on orbit (e.g., an unexpected drop in battery performance during eclipse).
* **Trigger:** The time-tagged execution of an uploaded command sequence violates updated onboard resource margins.
* **Resources Affected:** Mission Schedule Queue, Platform Safety Bounds.
* **Telemetry Changes:** `COMMAND_VALIDATION_FAILED` flag; `ORCA_AUTONOMY_LEVEL` overrides the command queue.
* **Operational Decisions:** Intercept and suspend the invalid command block; drop down into a verified low-risk resource preservation state; notify ground tracking loops during the next visibility window.
* **Digital Twin Compatibility:** Yes. Modeled as an active checking loop that evaluates commands against state-space capacity.
* **ORCA Compatibility:** Yes (ORCA v1 Candidate). Demonstrates that onboard autonomy can safely evaluate and override stale ground commands to protect the spacecraft.
* **Implementation Complexity:** Medium.
* **References:** ECSS-E-ST-70C (Space Operations Engineering).

### 7.10 Scenario OPS-02: Real-Time Onboard Autonomous Opportunity Detection

* **Mission Context:** The Edge AI payload processes Earth Observation imagery in real time and detects an active wildfire or natural disaster. This triggers an emergency, high-priority request to downlink data, overriding the standard, pre-planned timeline.
* **Trigger:** Edge AI core asserts an emergency event detection flag into the telemetry system.
* **Resources Affected:** Mission Schedule Matrix, SatCom Payload priority, Storage constraints.
* **Telemetry Changes:** `AI_DETECTION_METRIC` exceeds threshold; `EMERGENCY_DOWNLINK_REQUEST` is active; timeline priority variables scale up dynamically.
* **Operational Decisions:** Suspend non-essential scheduled activities; prioritize the SatCom transmission loop; stream the critical event telemetry over available channels.
* **Digital Twin Compatibility:** Yes. Modeled as an asynchronous priority change event within the scheduling framework.
* **ORCA Compatibility:** Yes (ORCA v1 Candidate). Validates responsive, event-driven scheduling capabilities.
* **Implementation Complexity:** Medium.
* **References:** NASA Autonomous Systems Working Group Research.

### 7.11 Scenario FLT-01: Radiation-Induced Single Event Latch-Up (SEL) on Power Switch

* **Mission Context:** Heavy ions in LEO can strike the drive circuitry of an electronic power switch, causing a localized short-circuit condition that draws high current and threatens to damage the power bus.
* **Trigger:** Simulated radiation particle strike flag creating an over-current fault condition on a payload power line.
* **Resources Affected:** Electrical Power Bus routing, Payload availability.
* **Telemetry Changes:** `CHANNEL_CURRENT_PNT` spikes past safety limits; `BUS_VOLTAGE` drops briefly; hardware protection trips the breaker.
* **Operational Decisions:** Identify the tripped channel; isolate the payload within the scheduling framework; reallocate the unspent power budget to other healthy subsystems; schedule a diagnostic power-cycle later in the orbit.
* **Digital Twin Compatibility:** Yes. Modeled as a step-function current load surge followed by an automated switch disconnect.
* **ORCA Compatibility:** Yes (ORCA v1 Candidate). Evaluates autonomous recovery and real-time contingency scheduling.
* **Implementation Complexity:** Low to Medium.
* **References:** NASA Fault Management Handbook.

### 7.12 Scenario FLT-02: Telemetry Stream Corruption / Generator Sync Anomaly

* **Mission Context:** Transient Single Event Upsets inside the memory buffers of the telemetry generation module can corrupt packet formatting or CCSDS headers, causing downstream processing errors in the arbitrator.
* **Trigger:** Memory corruption flag modifies the output structure of the telemetry subsystem.
* **Resources Affected:** Telemetry Generator stability, Arbitrator parsing pipelines.
* **Telemetry Changes:** `CCSDS_HEADER_ERRORS` increment; checksum validations fail; `TELEMETRY_STREAM_VALID` flag drops to False.
* **Operational Decisions:** Switch the data parsing pipeline to an alternative telemetry buffer partition; degrade gracefully by using the last known valid state-space values; request a soft reset of the generation module.
* **Digital Twin Compatibility:** Yes. Simulates random or burst errors inside the telemetry transmission frame arrays.
* **ORCA Compatibility:** Yes (ORCA v1 Candidate). Tests the arbitrator's resilience and robust handling of bad data.
* **Implementation Complexity:** Medium.
* **References:** CubeSat Design Specification (Data handling and resilience guidelines).

### 7.13 Scenario ENV-01: Enhanced Atmospheric Drag Due to Space Weather Events

* **Mission Context:** Solar particle events can heat and expand Earth's upper atmosphere, rapidly increasing aerodynamic drag on LEO satellites. Compensating for this drag requires continuous, high-duty-cycle operations from active attitude control systems.
* **Trigger:** Space weather entry parameter scales up background current demands within the environmental model.
* **Resources Affected:** Electrical Power Bus capacity, Available structural margins.
* **Telemetry Expected:** `ADCS_BACKGROUND_CURRENT_DRAW` doubles; net solar power extraction margins narrow.
* **Operational Decisions:** Compress payload execution windows; down-scale background data processing tasks to accommodate the increased baseline power requirements of the attitude control system.
* **Digital Twin Compatibility:** Yes. Modeled as an unexpected increase in baseline background current draw on the primary power bus.
* **ORCA Compatibility:** Yes (ORCA v1 Candidate). Demonstrates that ORCA can manage payload operations when external environmental events reduce available resource margins.
* **Implementation Complexity:** Low to Medium.
* **References:** Space Mission Engineering: The New SMAD (Space weather impacts).

---

## 8. ORCA v1 Candidate Scenarios

The matrix below maps the 13 researched scenarios against the current capabilities of the ORCA v1 Digital Twin subsystem models. Only scenarios requiring no auxiliary physics modules (e.g., ADCS kinematics, propulsion tracking, or constellation mesh networks) are approved for the core implementation baseline.

| ID | Scenario Name | BAT | SOL | THM | RF | PLD | OPS | TLM | ORCA Decision Strategy | Twin Fit |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **PWR-01** | Main Power Bus Overload |  |  |  |  | **X** |  | **X** | Stagger startup; enforce time delays. | **Yes** |
| **BAT-01** | Deep Eclipse Discharge | **X** | **X** |  |  | **X** |  | **X** | Load-shed background tasks. | **Yes** |
| **THM-01** | Compute Core Thermal Overload |  |  | **X** |  | **X** |  | **X** | Adjust duty cycles; throttle processing rates. | **Yes** |
| **THM-02** | Payload Structural Cold Soak |  |  | **X** |  |  |  | **X** | Prioritize survival heating lines. | **Yes** |
| **COM-01** | Co-Site RF Harmonic Desense |  |  |  | **X** | **X** |  | **X** | Enforce Time-Division Multiplexing (TDM). | **Yes** |
| **COM-02** | Regulatory RF Silent Geofence |  |  |  | **X** | **X** | **X** | **X** | Terminate transmissions; buffer local data. | **Yes** |
| **PLD-01** | Multi-Payload Profile Conflict |  |  |  |  | **X** | **X** | **X** | Evaluate priority weights; defer tasks. | **Yes** |
| **PLD-02** | Payload Reconfig Failure |  |  |  |  | **X** |  | **X** | Isolate and power-cycle the switch channel. | **Yes** |
| **OPS-01** | Ground Command Conflict |  |  |  |  |  | **X** | **X** | Intercept and override invalid timelines. | **Yes** |
| **OPS-02** | Real-Time Opportunity Detection |  |  |  |  | **X** | **X** | **X** | Reallocate resources to high-priority alerts. | **Yes** |
| **FLT-01** | Radiation Switch SEL |  |  |  |  | **X** |  | **X** | Trip breaker; isolate fault; update schedule. | **Yes** |
| **FLT-02** | Telemetry Stream Corruption |  |  |  |  |  |  | **X** | Switch buffer lines; use last known safe states. | **Yes** |
| **ENV-01** | Space Weather Drag Surge |  |  |  |  |  |  | **X** | Compress payload windows; match new margins. | **Yes** |

---

## 9. Future Research Scenarios

Advanced validation phases will expand the operational capabilities of the prototype. These complex scenarios require additional high-fidelity subsystem modules and are excluded from the current ORCA v1 baseline.

### 9.1 Reaction Wheel Saturation & Kinetic Slew Failures

* **Subsystems Needed:** Full Attitude Determination and Control System (ADCS), Reaction Wheel Models, Momentum Desaturation Thrusters.
* **Operational Scope:** Tracking momentum accumulation across three axes during rapid, multi-target imaging paths. When a reaction wheel reaches its maximum RPM, the spacecraft can no longer execute pointing maneuvers until magnetic torquers or thrusters desaturate the wheels. ORCA must integrate momentum buildup predictions into its scheduling decisions to avoid target dropouts.

### 9.2 Precision Orbital Orbit Degradation & Aerodynamic Decay Transitions

* **Subsystems Needed:** High-Fidelity Orbit Propagation, Atmospheric Density Variations, Active Chemical/Electric Propulsion Models.
* **Operational Scope:** Simulating orbital lifecycle changes where altitude loss increases atmospheric drag and modifies ground track cross-over times. The scheduling system must coordinate thruster firing sequences, which require significant power and impose constraints on payload operations.

### 9.3 Secondary Single Event Transients (SET) & Structural Radiation Dose Modeling

* **Subsystems Needed:** Cosmic Ray Fluctuation Engines, Total Ionizing Dose (TID) Accumulation Arrays.
* **Operational Scope:** Simulating cumulative radiation damage in polar regions or the South Atlantic Anomaly (SAA). This includes managing gradual increases in sensor noise floors and handling transient bit-flips across multiple processing cores simultaneously.

### 9.4 Inter-Satellite Link (ISL) Handover Bottlenecks & Network Rejections

* **Subsystems Needed:** Multi-Satellite Constellation Simulators, Dynamic Routing Protocol Stacks.
* **Operational Scope:** Coordinating resource allocations across multiple satellites in a constellation mesh network. If a neighbor satellite encounters local power or thermal limits and rejects an Inter-Satellite Link data transfer, the arbitrator must adapt by compressing data or finding alternative network routing pathways.

---

## 10. Engineering Discussion

A common pitfall when developing autonomous spacecraft software is over-allocating engineering resources to building high-fidelity physical simulations within the testing framework. While accurate orbital dynamics and detailed multi-node finite element thermal modeling are necessary for structural vehicle design, they can be counterproductive when validating an onboard resource scheduler.

An autonomous arbitrator like ORCA operates entirely on **state logic boundary crossings, constraint optimization rules, and discrete decision matrices**. The arbitrator does not need to know the continuous temperature gradient down to a fraction of a degree; it simply needs a mathematically consistent representation of trends to know if a specific task will violate a safety limit ($T_{node} \ge T_{max}$).

```
+-------------------------------------------------------------------------+
|                       ABSTRACTION LAYER VALIDATION                      |
+-------------------------------------------------------------------------+
| [HIGH-FIDELITY PHYSICS SIMULATION]                                      |
| -> Continuous Differential Calculations (e.g., 6-DOF Kinematics)       |
| -> High Computational Resource Requirements                             |
|                                                                         |
|                       REDUCED BY LUMPED MODEL TO:                       |
|                                                                         |
| [ORCA STATE ABSTRACT REPRESENTATION]                                    |
| -> State: Slew Settle Flag == TRUE / Current Load Accumulation          |
| -> Fast, Deterministic Validation of Decision Logic trees               |
+-------------------------------------------------------------------------+

```

By abstracting physical subsystems into lumped-parameter models with simplified state transitions, developers can test edge-case conditions quickly and deterministically. This abstraction focuses validation on the scheduler's decision-making capabilities—such as its ability to safely handle multi-variable conflicts, manage unexpected component failures, and adapt timelines under resource scarcity—rather than debugging complex physics code.

---

## 11. Conclusions

This research document establishes the operational baseline for validating autonomous onboard resource management software. By organizing these realistic, multi-variable engineering scenarios, the project can proceed with structured development across subsequent execution phases:

* **Phase 2 (Current - Scenario Engine):** Integrating the 13 prioritized ORCA v1 scenarios into the Simulator Engine to provide consistent, reproducible state transitions and telemetry outputs.
* **Phase 3 (Rule-Based Scheduler):** Developing a deterministic, rule-based scheduling engine capable of managing hard constraints, handling geofence zones, and executing basic load-shedding routines.
* **Phase 4 (ORCA Decision Engine):** Implementing the full, multi-variable optimization engine to evaluate complex trade-offs, predictive thermal behaviors, and dynamic mission priority shifts.
* **Phase 5 (Validation):** Executing automated test loops across the scenario library to verify system performance, stability, and response times under high-contention operations.

---

## 12. References

1. *NASA Systems Engineering Handbook*, NASA/SP-2016-6105 Rev 2. National Aeronautics and Space Administration, Washington, D.C., 2016.
2. *NASA Fault Management Handbook*, NASA-HDBK-1002. National Aeronautics and Space Administration, Washington, D.C., 2012.
3. Wertz, J. R., Everett, D. F., and Puschell, J. J., *Space Mission Engineering: The New SMAD*, Microcosm Press, Torrance, CA, 2011.
4. Larson, W. J., and Wertz, J. R., *Space Mission Analysis and Design (SMAD)*, 3rd ed., Space Technology Library, Kluwer Academic Publishers, Dordrecht, 1999.
5. *CubeSat Design Specification*, California Polytechnic State University, San Luis Obispo, Rev. 14.1, 2022.
6. *Space Engineering - Ground Systems and Mission Operations*, ECSS-E-ST-70C, European Cooperation for Space Standardization, Noordwijk, Netherlands, 2008.
7. *Space Engineering - Spacecraft Electrical Power*, ECSS-E-ST-20C, European Cooperation for Space Standardization, Noordwijk, Netherlands, 2016.
8. *CCSDS Packet Telemetry Standard*, CCSDS 132.0-B-3, Consultative Committee for Space Data Systems, Washington, D.C., 2020.
9. *The Trick Simulation Environment Product Overview*, NASA Lyndon B. Johnson Space Center, Software Robotics and Simulation Division, Houston, TX, 2024.
10. Chien, S., et al., "Autonomous Mission Operations on the Earth Observing One Mission," *IEEE Intelligent Systems*, Vol. 20, No. 3, 2005, pp. 16-24.
11. Selected Papers on Edge AI Processing Architectures, *Proceedings of the Annual Small Satellite Conference*, Logan, UT, 2022–2025.