import paho.mqtt.client as mqtt
import pyaudio

# 오디오 설정
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 22050
mqtt_ip = '220.67.231.91'
mqtt_port = 80
# PyAudio 설정
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)


def on_connect(client, userdata, flag, rc, prop=None):
    print("접속 결과: " + str(rc))
    client.subscribe("audio")


def on_message(client, userdata, msg):
    audio_data = msg.payload
    stream.write(audio_data)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtt_ip, mqtt_port)
client.loop_forever()

# 스트림 및 PyAudio 종료 (실행이 끝날 때 호출)
stream.stop_stream()
stream.close()
audio.terminate()
