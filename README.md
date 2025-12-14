# 🌡️ IoT Environment Monitoring 

**My IoT environment monitoring project using ESP32, DHT22, Node-RED, InfluxDB, AWS, and Grafana.**  
This system monitors **temperature 🌡️ and humidity 💧** using the **DHT22 sensor**.  
The **ESP32 ⚙️** sends data via **MQTT 🔗** to **Node-RED 🧠**, where the data is forwarded to **AWS Lambda** and stored in **InfluxDB** and **AWS DynamoDB** for automation and analysis.  

---

## 🧠 Smart Logic
- 💡 **Turn on/off an LED** is fully controlled by **AWS Lambda** functions based on temperature thresholds (>30°C).  
- 🔔 **Data is processed and exposed via RESTful API** for external applications or dashboards.  

---

## 🔩 Tools & Languages

![Node-RED](https://img.shields.io/badge/Node--RED-8F0000?style=flat&logo=nodered&logoColor=white)
![ESP32](https://img.shields.io/badge/ESP32-000000?style=flat&logo=espressif&logoColor=white)
![MQTT](https://img.shields.io/badge/MQTT-660066?style=flat&logo=eclipse-mosquitto&logoColor=white)
![InfluxDB](https://img.shields.io/badge/InfluxDB-22ADF6?style=flat&logo=influxdb&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-FF9900?style=flat&logo=amazon-aws&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![C++](https://img.shields.io/badge/C++-00599C?style=flat&logo=c%2B%2B&logoColor=white)
![REST API](https://img.shields.io/badge/REST-0078D4?style=flat&logo=rest&logoColor=white)
![VSCode](https://img.shields.io/badge/VS_Code-0078D4?style=flat&logo=visual%20studio%20code&logoColor=white)

---

## 🧰 Technologies Used
| Component | Description |
|------------|-------------|
| ⚙️ **ESP32** | Main microcontroller sending sensor data |
| 🌡️ **DHT22** | Temperature & Humidity Sensor |
| 🔗 **MQTT** | Communication protocol |
| 🧠 **Node-RED** | Flow-based processing to forward data |
| ☁️ **AWS Lambda** | Cloud automation controlling LED and processing data |
| 💾 **InfluxDB** | Time-series database for sensor storage |
| 📈 **Grafana** | Dashboard & data visualization from InfluxDB |
| 🌐 **RESTful API** | Expose processed data for external applications |

---

## 🚀 How It Works
1. ESP32 reads temperature and humidity from the DHT22 sensor.  
2. Data is sent via **MQTT** to **Node-RED**.  
3. Node-RED forwards data to **AWS Lambda** for processing.  
4. **AWS Lambda** controls the LED if temperature exceeds 30°C.  
5. Sensor data is stored in **InfluxDB** and **AWS DynamoDB**.  
6. **RESTful API** exposes the data for dashboards or external applications.  
7. **Grafana** visualizes the stored data from InfluxDB.

---

## 🗂️ Project Files
| File | Description |
|------|--------------|
| `wokwi/esp32_MQTT_NODE.zip` | ESP32 circuit and code |
| `node_red_flow/flows.json` | Node-RED flow for forwarding MQTT data |
| `AWS/lambda_function_control_led.py` | Lambda to control LED based on thresholds |
| `AWS/lambda__handle_API_getway.py` | Lambda for RESTful API handling |
| `images/influxdb_table.png` | InfluxDB table screenshot |
| `images/influxdb_dashboard.png` | InfluxDB dashboard screenshot |
| `images/grafana_dashboard.png` | Grafana dashboard screenshot |
| `README.md` | Project documentation |

---

## 🖼️ Dashboard Preview
Here’s how the dashboards look:

### **InfluxDB**
![InfluxDB Table](images/influxdb_table.png)
![InfluxDB Dashboard](images/influxdb_dashboard.png)

### **Grafana**
![Grafana Dashboard](images/grafana_dashboard.png)

---

## 🔗 Wokwi Simulation
Try the ESP32 circuit virtually in [**Wokwi**](https://wokwi.com/projects/444711968486592513).

---

## ☁️ Future Enhancements
- Advanced **data analytics & charts**  
- **Email/SMS alerts** for threshold breaches  
- Integrate **more sensors** for a complete smart greenhouse  

---

## 💬 Feedback
Feedback and suggestions are welcome 🙌  
Open an issue or reach out with ideas for improvement!

---

📘 *Created by [Ehab Mohammed](https://github.com/ehabmo7ammed)*  
⭐ If you like this project, don’t forget to give it a star!
