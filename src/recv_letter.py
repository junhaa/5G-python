import paho.mqtt.client as mqtt
import time


def on_connect(client, userdata, flag, rc, prop=None):
	print("Connect result: "+str(rc))
	client.subscribe("jmleehs")

def on_message(client, userdata, msg):
	print(str(msg.payload.decode('utf-8')) + " was received")

ip_address = '220.67.231.91'
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

client.connect(ip_address, 80)

client.loop_forever()
