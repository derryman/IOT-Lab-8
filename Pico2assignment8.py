import network
import machine
import time
from umqtt.simple import MQTTClient

# Set up Connection same code as previous lab
SSID = "Derry"               
PASSWORD = "Verysafepassword"   # Not real password

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

if not wlan.isconnected():
    wlan.connect(SSID, PASSWORD)
    print("Connecting to Wi-Fi...")
    while not wlan.isconnected():
        time.sleep(1)  
print("Connected:", wlan.ifconfig())  # Print IP details

# MQTT Setup
PiID = "172.20.10.8"          # Raspberry Pi IP address
TOPIC = "temp/pico"           # MQTT topic
client = MQTTClient("pico_pub", PiID)
client.connect()              # Connect to MQTT broker

# Temp Sensor Setup from previous lab
sensor_temp = machine.ADC(4)  
conversion_factor = 3.3 / 65535  

# Function to read temperature in Celsius
def read_temp():
    reading = sensor_temp.read_u16() * conversion_factor
    return 27 - (reading - 0.706)/0.001721  # Formula for RP2040 sensor

# Publish Loop
while True:
    temp = read_temp()  # Get temperature
    print("Publishing temperature:", temp)
    # Publish temperature to MQTT topic rounded 2 dec places
    client.publish(TOPIC, str(round(temp, 2)))
    time.sleep(1)  
