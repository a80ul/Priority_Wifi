# Priority_Wifi
## **🌐 NEXA HYPER - Network Priority Engine**
NEXA HYPER is a high-performance network optimization tool designed to stabilize and prioritize desktop internet traffic. Built with a sleek Cyber-UI, it leverages low-level packet injection and TCP stack optimization to ensure your connection remains at peak performance.

## **🛠️ Prerequisites**
Before running the application, ensure your environment meets these requirements:
-Python 3.9+: Download and install from python.org.
 PATH Configuration: During Python installation, you must check the "Add Python to PATH" box
-Npcap Driver: Required for low-level network packet handling. Download from npcap.com

## **🚀 How to Run**
We provide an automated script to handle dependencies and optimizations.
1.Clone/Download this repository.
2.Right-Click and select "Run as Administrator".
3.The script will perform a system integrity check and install required libraries (`Scapy`, `Psutil`, `Pillow`) automatically.

## **⚠️ System Integrity Alerts (Simulation)**

If your system is not properly configured, the `run_priority.bat` will display the following warnings:
<br>
<br>
**1. Python Not Found**
<br>
Occurs if Python is missing or not in your System PATH.

<pre>
[*] Checking Python Installation...

[ ERROR: PYTHON NOT FOUND ]
--------------------------------------------------
Python is not installed or not added to PATH.
--------------------------------------------------
</pre>

**2. Npcap Driver Missing**
<br>
Occurs if the required network drivers are not installed.

<pre>
  [*] Checking Npcap Driver...

[ ERROR: NPCAP NOT FOUND ]
--------------------------------------------------
Npcap driver is required for network packet injection.
--------------------------------------------------
</pre>

## **📑 Core Features**
+ Priority Mode: Active packet injection engine to minimize latency.
+ Network Tuner: One-click TCP Stack optimization and ARP cache clearing.
+ WiFi Manager: Retrieve and manage saved WiFi profiles and passwords.
+ Live Dashboard: Real-time monitoring of Upload/Download rates and data flow.

## **🛡️ Security Note**

+ Administrator Access: This app requires elevated privileges to modify network tables `(netsh` & `arp`).
+ Antivirus: Some security software may flag the ARP clearing activity. This is a False Positive as the app is performing legitimate network maintenance.
