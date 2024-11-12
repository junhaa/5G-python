import paho.mqtt.client as mqtt
import time

ip_address = '220.67.231.91'
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(ip_address, 80)
client.loop_start()

index = 0
messages = ["Hello, Seoul", "How are you?"]
while True:
	msg = messages[index%len(messages)] + ":" + str(index)
	index = (index+1) % 1000000

	client.publish("jmleehs", msg)
	print("'%s' was sent" % msg)
	time.sleep(1)

client.loop_stop()
