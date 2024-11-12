import json
import time
import paho.mqtt.client as mqtt
import pyaudio
from opuslib import Decoder

FORMAT = pyaudio.paInt16
CHUNK = 960  # Opus는 특정 프레임 크기를 사용합니다.
CHANNELS = 2
RATE = 24000  # Opus는 8000, 12000, 16000, 24000, 48000Hz를 지원합니다.

audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

decoder = Decoder(RATE, CHANNELS)

def on_connect(client, userdata, flag, rc, prop=None):
    print("Connect result: "+str(rc))
    client.subscribe("audio")

def on_message(client, userdata, msg):
    if msg.topic == "audio":
        receive_time_start = time.time()

        # JSON 역직렬화
        message = json.loads(msg.payload.decode())
        send_time = message['timestamp']

        receive_tmp_end = time.time();

        print(f"역직렬화 시간: {(receive_tmp_end - receive_time_start) * 1000:.2f} ms")

        receive_time_end = time.time()
        total_latency = receive_time_end - send_time
        print(f"지연 시간 (압축 해제 포함): {total_latency * 1000:.2f} ms")

        # 오디오 재생
        stream.write(message['data'])

ip_address = '220.67.231.91'
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

client.connect(ip_address, 80)

client.loop_forever()

