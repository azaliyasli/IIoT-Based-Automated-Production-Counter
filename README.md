
# 🏭 IIoT-Based Automated Production Counter 

This project is a industrial object tracking and counting system using **YOLOv8** and **MQTT** for Industrial IoT (IIoT) applications. 

It simulates a synthetic factory production line. It uses Computer Vision to detect and count bottles moving on a conveyor belt and instantly publishes the production data to an MQTT broker, allowing real-time monitoring across the network.

## 🚀 Features
* **Real-Time Object Detection:** Utilizes Ultralytics YOLOv8 for high-speed, accurate detection.
* **Smart Tracking:** Implements ByteTrack to assign unique IDs to objects, preventing double-counting.
* **IIoT Integration:** Uses the MQTT protocol (`paho-mqtt`) for lightweight, real-time data transmission.
* **Modular Architecture:** Separation of concerns between the Computer Vision logic and the Network/Communication logic.

## 🛠️ Technologies Used
* **Python 3.x**
* **Computer Vision:** Ultralytics YOLOv8
* **Networking/IIoT:** Eclipse Paho MQTT
* **Public Broker:** HiveMQ (`broker.hivemq.com`)

## 📂 Project Structure
```text
📦 automated_product_counter
 ┣ 📜 main.py               # Core vision logic and counting algorithm
 ┣ 📜 mqtt_publisher.py     # MQTT class to handle connections and publishing
 ┣ 📜 mqtt_subscriber.py    # Standalone listener to monitor production data
 ┣ 📜 yolov8n.pt            # Pre-trained YOLOv8 Nano model 
 ┗ 🎬 BottleProductionVideo.mp4 # Sample production line video
```

## ⚙️ Installation

1. Clone the repository:
```bash
git clone [https://github.com/yourusername/visiontrack-iiot.git](https://github.com/yourusername/visiontrack-iiot.git)
cd visiontrack-iiot
```

2. Install the required dependencies:
```bash
pip install ultralytics opencv-python paho-mqtt
```

## 🚀 Usage

To see the IIoT communication in action, you need to run the publisher (vision system) and the subscriber (data listener) simultaneously.

**1. Start the Data Listener (Subscriber)**
Open a terminal and run the subscriber script to start listening to the MQTT broker:
```bash
python mqtt_subscriber.py
```

**2. Start the Production Line (Publisher)**
Open a **second** terminal and run the main vision script:
```bash
python main.py
```

As the bottles cross the virtual counting line on the video feed, you will see the `total_bottles` count increase on the screen, and the exact same data will instantly appear in your subscriber terminal via MQTT.

## 🧠 How the Counting Logic Works
The system draws a virtual vertical line in the center of the frame. It calculates the center point `(x, y)` of each bounding box detected by YOLO. When an object's center point falls within a specific pixel offset of the virtual line, the object's unique tracking ID is added to a Python `set()`. This ensures that even if the conveyor belt stops, the object is strictly counted only once.

---
*Note: This project is configured to use `broker.hivemq.com` on port `1883` by default. Ensure your network does not block this port, or switch to a mobile hotspot if you experience connection timeouts.*
```
