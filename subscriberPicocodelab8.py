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
        time.sleep(0.5)  
print("Connected:", wlan.ifconfig())  # Print IP details

# MQTT Setup
PiID = "172.20.10.8"          # Pi address
TOPIC = "temp/pico"           # MQTT topic

# GPIO setup
led = machine.Pin(0, machine.Pin.OUT)  # LED connected to GPIO pin 0

# Callback function for incoming MQTT messages
def sub_cb(topic, msg):
    temp = float(msg)  # Convert message to float (temperature)
    print("Received temperature:", temp)
    # Turn LED ON if temperature > 25°C otherwise OFF
    if temp > 25:
        led.value(1)
        print("LED ON (Temp > 25°C)")
    else:
        led.value(0)
        print("LED OFF")

# Create MQTT client and configure callback
client = MQTTClient("pico_sub", PiID)
client.set_callback(sub_cb)
client.connect()           # Connect to MQTT Broker 
client.subscribe(TOPIC)       # Subscribe to the topic (Temperature)

# Main Loop
while True:
    client.check_msg()        # Check for MQTT messages
    time.sleep(0.1)           # Added a small delay to avoid bottleneck