import pyaudio
import threading
import json
import queue
import paho.mqtt.client as mqtt
import time
from opuslib import Encoder, Decoder

# 설정 변수
CHUNK = 480  # Opus는 특정 프레임 크기를 사용합니다.
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 24000  # Opus는 8000, 12000, 16000, 24000, 48000Hz를 지원합니다.
BUFFER_SIZE = 10
# mqtt_ip = 'broker.hivemq.com'

HOST = '0.0.0.0'  # 서버 IP 주소
PORT = 12345      # 포트 번호

mqtt_ip = 'localhost'
mqtt_port = 80

# Opus 인코더 및 디코더 초기화
encoder = Encoder(RATE, CHANNELS, 'audio')
decoder = Decoder(RATE, CHANNELS)

audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

# 큐 생성
audio_queue = queue.Queue(maxsize=BUFFER_SIZE)

def record_audio():
    try:
        audio = pyaudio.PyAudio()
        stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        while True:
            timestamp = time.time()
            data = stream.read(CHUNK)
            # 음성 데이터 압축
            encoded_data = encoder.encode(data, CHUNK)
            audio_queue.put((encoded_data, timestamp))
    except KeyboardInterrupt:
        print('녹음 종료.')
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

# mqtt 전송 스레드 함수
def send_audio_mqtt():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(mqtt_ip, mqtt_port)
    client.loop_start()
    try:
        while True:
            if not audio_queue.empty():
                encoded_data, send_time = audio_queue.get()
                # 데이터와 타임스탬프를 하나의 딕셔너리로 묶음
                message = {
                    'data': encoded_data.hex(),  # 바이너리 데이터를 헥사 문자열로 변환
                    'timestamp': send_time
                }
                # JSON 직렬화
                payload = json.dumps(message)
                client.publish("audio", payload)
    except KeyboardInterrupt:
        print('mqtt 전송 종료.')


# 녹음 및 소켓 스레드 생성
record_thread = threading.Thread(target=record_audio)
send_thread = threading.Thread(target=send_audio_mqtt)

# 스레드 시작
record_thread.start()
send_thread.start()

# 스레드 종료 대기
record_thread.join()
send_thread.join()


