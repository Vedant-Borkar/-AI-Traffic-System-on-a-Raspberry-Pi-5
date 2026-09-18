# 🚦 AI-Based Traffic Signaling with Accident Detection System

> **An edge-AI powered intelligent traffic management system built on Raspberry Pi 5, combining real-time vehicle detection, adaptive traffic signaling, and accident detection.**

**Final Year Major Project**

### 👨‍💻 Built By

* **Vedant Borkar**
* **Sagar Manchakatla**
* **Pooja Makhijani**
* **Siddhi Mehta**

---

## 📌 Overview

Traditional traffic signals operate on fixed timers, regardless of the actual traffic conditions at an intersection. This project explores an **AI-driven traffic signaling system** capable of analyzing multiple camera feeds in real time and dynamically controlling physical traffic lights based on detected traffic conditions.

The system also incorporates **AI-based accident detection**, enabling the system to identify potential accidents from camera feeds and provide an automated response.

The entire system is designed to run locally on a **Raspberry Pi 5**, making it an edge-computing solution that minimizes dependence on cloud infrastructure and enables real-time processing.

### Core Capabilities

* 🚗 Real-time vehicle detection
* 🚦 Dynamic traffic signal control
* 📹 Multi-camera video processing
* 🧠 AI-based accident detection
* ⚡ Edge AI inference
* 🔌 Physical traffic-light control through GPIO
* 📊 Real-time traffic analysis
* 🔄 Continuous 24/7 operation

---

# 🏗️ System Architecture

```text
                 ┌──────────────────────┐
                 │    Camera Feeds      │
                 │   Multiple Streams   │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   Video Processing   │
                 │       OpenCV         │
                 │        V4L2          │
                 └──────────┬───────────┘
                            │
                            ▼
              ┌─────────────────────────────┐
              │       AI Inference Layer    │
              │                             │
              │  YOLO → Vehicle Detection  │
              │  CNN  → Accident Detection │
              └─────────────┬───────────────┘
                            │
              ┌─────────────┴──────────────┐
              │                            │
              ▼                            ▼
   ┌─────────────────────┐      ┌─────────────────────┐
   │ Traffic Analysis    │      │ Accident Detection  │
   │ & Decision Engine   │      │ & Response Logic    │
   └──────────┬──────────┘      └──────────┬──────────┘
              │                            │
              └─────────────┬──────────────┘
                            ▼
                 ┌──────────────────────┐
                 │   Raspberry Pi GPIO  │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   Physical Traffic   │
                 │       Signals        │
                 └──────────────────────┘
```

---

# 🧠 AI & Computer Vision

The system uses computer vision and machine learning models to process live camera feeds directly on the edge device.

### Vehicle Detection

A **YOLO-based object detection pipeline** is used to identify and count vehicles from incoming camera streams.

The detected traffic information can then be used by the traffic-control logic to determine signal timing dynamically.

### Accident Detection

A **CNN-based classification/detection pipeline** is used to identify potential accident events from the video stream.

The accident detection subsystem is designed to work alongside the traffic-control system so that an abnormal event can trigger an appropriate automated response.

---

# 🚦 Intelligent Traffic Signaling

Instead of relying solely on predefined signal timings, the system uses detected traffic information to make signaling decisions.

The basic flow is:

```text
Camera Input
     ↓
Vehicle Detection
     ↓
Vehicle Count / Traffic Density
     ↓
Traffic Decision Engine
     ↓
Signal Timing
     ↓
GPIO Output
     ↓
Physical Traffic Light
```

This enables the traffic signal to respond to **real-time traffic conditions** rather than operating purely on fixed intervals.

---

# 🍓 Raspberry Pi 5 Edge Computing

One of the biggest engineering challenges of this project was getting a computer-vision workload to run reliably on a small embedded device.

The Raspberry Pi 5 is surprisingly powerful, but running multiple AI workloads continuously introduces several constraints.

## 🔥 The Reality Check

### Thermal Throttling Is Real

The Raspberry Pi 5 can generate substantial heat under sustained workloads.

Without adequate cooling:

```text
High AI workload
      ↓
Higher CPU/GPU utilization
      ↓
Temperature increases
      ↓
Thermal throttling
      ↓
Reduced performance / FPS
```

Active cooling became an essential part of the final system.

With an appropriate cooling solution, the system was able to maintain significantly more stable operating temperatures during continuous workloads.

---

### 🧠 RAM Is Gold

Running multiple camera streams, computer-vision pipelines, AI models and supporting processes simultaneously can consume memory quickly.

Memory optimization therefore became an important part of making the system reliable for long-running operation.

---

### 📹 V4L2 & Multi-Camera Challenges

USB cameras are not always completely plug-and-play when multiple video streams are being processed simultaneously.

Managing:

* Camera device enumeration
* Video formats
* Resolution
* Frame rates
* Buffering
* V4L2 configuration
* Multiple concurrent streams

became an important part of the system implementation.

---

### 🔌 GPIO Is Unforgiving

The Raspberry Pi GPIO interface provides direct control over physical hardware, but incorrect wiring or electrical conditions can damage components.

Let's just say one LED didn't make it through development.

> 🪦 **RIP LED #3 — gone but not forgotten.**

---

# ⚡ Performance Optimizations

Several optimizations were implemented to make real-time inference practical on the Raspberry Pi.

## Active Cooling

Adding active cooling significantly reduced operating temperatures and helped prevent thermal throttling during sustained inference workloads.

---

## OpenCV Headless

Removing unnecessary graphical interfaces reduced memory overhead and allowed more resources to be dedicated to the actual AI and video-processing pipelines.

---

## Quantized AI Models

Quantized TensorFlow Lite models were used to reduce inference overhead.

Compared with full-precision models, quantized models can significantly reduce:

* Model size
* Memory usage
* Computational requirements
* Inference latency

In our testing, quantized models achieved approximately **3× faster inference** compared with the corresponding full TensorFlow setup.

---

# 🧠 AI Acceleration

CPU-only inference reaches a practical performance ceiling when multiple camera streams and AI models need to operate simultaneously.

To address this, the system architecture supports dedicated AI acceleration using the **Raspberry Pi M.2 HAT+ with a Hailo AI accelerator**.

This moves computationally intensive AI inference away from the Raspberry Pi CPU and toward dedicated AI hardware.

### Conceptually:

```text
Without Accelerator

Camera
  ↓
OpenCV
  ↓
YOLO / CNN
  ↓
Raspberry Pi CPU
  ↓
GPIO


With AI Accelerator

Camera
  ↓
OpenCV
  ↓
AI Model
  ↓
Hailo Accelerator
  ↓
Raspberry Pi
  ↓
GPIO
```

This architecture makes it possible to scale toward more demanding real-time edge-AI workloads.

---

# 📊 Current System

The optimized system is capable of:

| Capability                     | Status |
| ------------------------------ | ------ |
| Multiple camera feeds          | ✅      |
| 4 simultaneous camera feeds    | ✅      |
| Real-time YOLO inference       | ✅      |
| CNN-based accident detection   | ✅      |
| Physical traffic-light control | ✅      |
| Raspberry Pi GPIO integration  | ✅      |
| Edge AI processing             | ✅      |
| 24/7 continuous operation      | ✅      |
| Stable operating temperature   | ~60°C  |

---

# 🛠️ Technology Stack

### Hardware

* 🍓 Raspberry Pi 5
* 📹 USB Cameras
* 🚦 Traffic Light LEDs
* 🔌 GPIO Interface
* ❄️ Active Cooling
* 🧠 Hailo AI Accelerator *(supported architecture)*

### Software

* 🐍 Python
* 👁️ OpenCV
* 🤖 YOLO
* 🧠 CNN
* ⚡ TensorFlow Lite
* 📹 V4L2
* 🔌 Raspberry Pi GPIO
* 🐧 Linux

---

# 🔬 Engineering Challenges

Building an AI system for an embedded platform introduced challenges that aren't immediately obvious when developing on a desktop.

### The major challenges included:

* Running multiple camera streams simultaneously
* Maintaining real-time inference performance
* Preventing thermal throttling
* Managing limited RAM
* Optimizing AI models for edge inference
* Handling V4L2 camera configuration
* Integrating AI decisions with physical GPIO hardware
* Designing the system for continuous operation
* Balancing accuracy against inference latency

The project therefore became more than simply training an AI model.

It became an exercise in **systems engineering, optimization, computer vision, embedded computing and hardware-software integration.**

---

# 📈 Future Improvements

Potential future improvements include:

* [ ] Dedicated Hailo AI acceleration for all inference workloads
* [ ] Improved accident-event classification
* [ ] Emergency-vehicle detection and priority signaling
* [ ] Automatic emergency-service notification
* [ ] Traffic analytics dashboard
* [ ] Historical traffic-data storage
* [ ] Adaptive signal optimization using reinforcement learning
* [ ] Number-plate recognition
* [ ] Pedestrian detection
* [ ] Vehicle-type classification
* [ ] Remote monitoring
* [ ] Multi-intersection coordination
* [ ] Cloud-based analytics while keeping inference on-device

---

# 💡 Key Takeaway

The biggest lesson from this project was simple:

> **Don't just build. Optimize.**

Getting an AI model to work on a powerful development machine is one problem.

Getting multiple AI models, multiple cameras, computer vision, physical hardware and traffic-control logic to operate **continuously on an embedded system** is a completely different engineering challenge.

The Raspberry Pi 5 is powerful hardware, but it needs to be treated like what it is:

**an edge-computing platform, not a desktop replacement.**

Once the software, models and hardware are designed around those constraints, the possibilities become much more interesting.

---

# 👨‍💻 Team

### Vedant Borkar

### Sagar Manchakatla

### Pooja Makhijani

### Siddhi Mehta


---

# 📜 Academic Project

This project was developed as a **Final Year Major Project** with the objective of exploring the practical application of **Artificial Intelligence, Computer Vision, Embedded Systems and Edge Computing** in intelligent transportation systems.

---

## ⭐ If you found this project interesting

Feel free to explore the implementation, experiment with the system, and learn from the engineering decisions behind the project.

**Built with Python, AI, Raspberry Pi, computer vision, and a lot of debugging. 🚦🤖🍓**
