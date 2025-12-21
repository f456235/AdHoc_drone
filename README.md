# 🚁 Decentralized Drone Swarm over MANET

![Python](https://img.shields.io/badge/Language-Python-blue)
![Platform](https://img.shields.io/badge/Platform-Raspberry%20Pi%20%7C%20Pixhawk-red)
![Network](https://img.shields.io/badge/Network-MANET%20(Ad--Hoc)-green)
![Simulation](https://img.shields.io/badge/Simulation-DroneKit--SITL-orange)

> **Role:** System Architect & Lead Developer
> **Key Contributions:** Designed the UDP-based broadcast protocol, implemented the Counter-Based Scheme for broadcast storm mitigation, and engineered the distributed V-formation logic.

## 📖 Project Overview

This project implements a fully **decentralized Mobile Ad-Hoc Network (MANET)** for autonomous drone swarms[cite: 43]. Unlike traditional centralized control systems, our architecture enables drones to communicate directly with each other (P2P) without relying on a ground station, ensuring resilience and scalability.

The system focuses on **Real-time Decision Making** by optimizing the communication layer. We engineered a custom **lightweight UDP protocol** and a **Counter-Based Suppression Scheme** to solve network congestion (Broadcast Storm Problem) inherent in multi-hop ad-hoc networks[cite: 43, 64].

## ⚙️ Key Features

* **Decentralized MANET Architecture:** Enables dynamic topology where drones can freely join/leave without collapsing the network[cite: 53].
* **Custom UDP Protocol:** A fixed-width, position-based byte stream designed to minimize latency and payload overhead[cite: 68].
* **Broadcast Storm Mitigation:** Implemented a **Counter-Based Scheme** with random delays to reduce redundant packet rebroadcasting and collisions[cite: 63, 64].
* **Distributed Formation Control:**
    * **V-Shape Formation:** Reduces air resistance and maintains visual contact[cite: 100, 101].
    * **Boids Algorithm:** Integration of Separation, Alignment, and Cohesion rules to prevent collisions during dynamic turns[cite: 112, 117].

---

## 🏗️ System Architecture

### 1. Hardware Setup
* **Flight Controller:** Pixhawk 4
* **Onboard Computer:** Raspberry Pi 4 (Computing Node)
* **Network Interface:**
    * `wlan0`: Configured in **Ad-Hoc Mode** for inter-drone communication (MANET).
    * `wlan1`: Wi-Fi mode for telemetry monitoring and debugging.

### 2. Communication Protocol
To ensure real-time responsiveness, we replaced standard JSON with a **custom byte-level protocol**.

| Type | Byte ID | Content |
| :--- | :--- | :--- |
| **Coordinates** | `0` | Longitude, Latitude, Altitude, Timestamp |
| **Takeoff** | `1` | Command Instruction |
| **Tookoff** | `2` | ACK |
| **Next_Coord** | `5` | Target Lat/Lon, Drone ID, Heading |



### 3. Coordinate Calculation Logic
Each drone independently calculates its target position based on the leader's telemetry, eliminating the need for central computation.
* **Formation Logic:** Calculates offsets $(dx, dy)$ based on V-shape angle $\theta = 30^\circ$.
* **Rotation Matrix:** Applies rotation based on the leader's heading to generate absolute GPS coordinates.

---

## 🚀 Simulation & Usage

We utilize **DroneKit-SITL** and **Mission Planner** for hardware-in-the-loop simulation.

### Prerequisites
* Python 3.x
* DroneKit & DroneKit-SITL
* Mission Planner (for GCS monitoring)

### Setup Network (Ad-Hoc)
Configure the Raspberry Pi network interfaces to join the MANET mesh:
```bash
# Example configuration for /etc/network/interfaces
auto wlan0
iface wlan0 inet static
    address 10.0.0.x
    netmask 255.255.255.0
    wireless-channel 1
    wireless-essid drone-manet
    wireless-mode ad-hoc
```
## Run Simulation

### 1. Start the SITL instances for multiple drones.
### 2. Run the main control script on each node:
``` bash
python3 main_controller.py --id [DRONE_ID] --role [LEADER/FOLLOWER]
```
### 3. Monitor the swarm behavior in Mission Planner.

## 🧪 Experimental Results

Our simulation experiments using **DroneKit-SITL** and **Mission Planner** demonstrated significant improvements in swarm stability and network efficiency:

### 1. Broadcast Storm Mitigation
* **Challenge:** In a decentralized MANET, blind flooding of telemetry packets caused high collision rates and network congestion (Broadcast Storm).
* **Solution:** We implemented a **Counter-Based Suppression Scheme** with random delays.
* **Result:** The scheme successfully reduced redundant packet rebroadcasts, maintaining low latency for critical control messages even as the number of nodes increased.

### 2. Formation Stability & Collision Avoidance
* **V-Shape Formation:** Adopted a V-formation inspired by bird flocks to reduce air resistance and improve visual coordination.
* **Boids Algorithm Integration:** During initial tests, drones risked collision during sharp turns. We integrated the **Boids Algorithm** (Separation, Alignment, Cohesion) to dynamically adjust speed and heading.
* **Result:** The swarm successfully executed complex maneuvers (turns and speed changes) without collisions, validating the effectiveness of the decentralized coordination logic.

---

## 👥 Contributors

This project was a collaborative effort focusing on different layers of the system architecture:

* **Shu-Jui Chang (張書睿)**
    * Network Protocol Design & Architecture
    * Simulation Implementation (DroneKit-SITL)
    * Algorithm Optimization (Boids & Formation Logic)
    
* **Hsu Hao-Wen (許昊彣)**
    * Embedded System Configuration (Raspberry Pi Ad-Hoc Setup)
    * Message Passing Implementation
    * Hardware Testing & Validation

---

## 📚 References

The development of this project relied on the following core literature and documentations:

1.  **Broadcast Storm Problem:** Ni, S., et al. "The Broadcast Storm Problem in a Mobile Ad Hoc Network." *Wireless Networks*.
2.  **DroneKit API:** [DroneKit-Python Documentation](https://github.com/dronekit/dronekit-python) for MAVLink communication.
3.  **Simulation Tools:** [DroneKit-SITL](https://github.com/dronekit/dronekit-sitl) for hardware-in-the-loop simulation.
4.  **Ad-Hoc Networking:** "Turn a Raspberry Pi into a Web Server with Its Own Wifi Network" (Steve Murch) for `wlan0` interface configuration.
5.  **Swarm Behavior:** [Boids Algorithm - Wikipedia](https://en.wikipedia.org/wiki/Boids).


this is a project to accomplish drone swarm via mesh network

for meeting slide per two weeks: https://docs.google.com/presentation/d/12PsGeB6dTJHsjw45wY_NwRveT9ywWn0ZtthjgJ2Z6CI/edit#slide=id.g2717a8b5346_0_0
