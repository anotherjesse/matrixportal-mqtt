# SPDX-FileCopyrightText: 2019 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
import time
import terminalio
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_matrixportal.matrixportal import MatrixPortal
from adafruit_matrixportal.network import Network


# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# print("ESP32 SPI webclient test")

# TEXT_URL = "http://wifitest.adafruit.com/testwifi/index.html"

matrixportal = MatrixPortal(status_neopixel=board.NEOPIXEL, debug=True)
network = matrixportal.network
network.connect()

matrixportal.add_text(
    text_font=terminalio.FONT,
    text_position=(0, (matrixportal.graphics.display.height // 2) - 1),
    scrolling=False,
)

# matrixportal.set_text("hiya world")


def connect(mqtt_client, userdata, flags, rc):
    # This function will be called when the mqtt_client is connected
    # successfully to the broker.
    print("Connected to MQTT Broker!")
    print("Flags: {0}\n RC: {1}".format(flags, rc))

def disconnect(mqtt_client, userdata, rc):
    # This method is called when the mqtt_client disconnects
    # from the broker.
    print("Disconnected from MQTT Broker!")


def subscribe(mqtt_client, userdata, topic, granted_qos):
    # This method is called when the mqtt_client subscribes to a new feed.
    print("Subscribed to {0} with QOS level {1}".format(topic, granted_qos))


def unsubscribe(mqtt_client, userdata, topic, pid):
    # This method is called when the mqtt_client unsubscribes from a feed.
    print("Unsubscribed from {0} with PID {1}".format(topic, pid))


def message(client, topic, message):
    matrixportal.set_background(int(message, 16))
    # matrixportal.set_text_color('#'+message)
    # matrixportal.set_text(message)
    # Method callled when a client's subscribed feed has a new value.
    print("New message on topic {0}: {1}".format(topic, message))

m = MQTT.MQTT(
    broker=secrets["broker"],
    port=secrets["port"],
    socket_pool=socket,
    is_ssl=False
)

mqtt_topic = "matrix"
m.on_connect = connect
m.on_disconnect = disconnect
m.on_subscribe = subscribe
m.on_unsubscribe = unsubscribe
m.on_message = message

print("Attempting to connect to %s" % m.broker)
m.connect()

print("Subscribing to %s" % mqtt_topic)
m.subscribe(mqtt_topic)

while True:
    try:
        m.is_connected()
        m.loop()
    except (MQTT.MMQTTException, RuntimeError):
        network.connect()
        m.reconnect()
