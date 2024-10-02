import socket
import pyaudio
import threading
import queue
import paho.mqtt.client as mqtt

# 녹음 및 소켓 설정
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 22050  # 샘플레이트 줄이기 (44100 -> 22050)
BUFFER_SIZE = 10  # 큐의 최대 크기
HOST = '0.0.0.0'  # 서버 IP 주소
PORT = 12345      # 포트 번호

# 큐 생성
audio_queue = queue.Queue(maxsize=BUFFER_SIZE)

mqtt_ip = 'broker.hivemq.com'
# 녹음 스레드 함수
def record_audio():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    try:
        while True:
            data = stream.read(CHUNK)
            if not audio_queue.full():
                audio_queue.put(data)  # 버퍼에 데이터 저장
    except KeyboardInterrupt:
        print('녹음 종료.')
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

#mqtt 전송 스레드 함수
def send_audio_mqtt():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(mqtt_ip, 1883)
    client.loop_start()

    try:
        while True:
            if not audio_queue.empty():
                audio_data = audio_queue.get()
                client.publish("audio", audio_data)
                print("전송된 데이터:%s" %audio_data)
    except KeyboardInterrupt:
        print('mqtt 전송 종료.')

# 소켓 전송 스레드 함수
def send_audio():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print('클라이언트를 기다리는 중...')

    client_socket, client_address = server_socket.accept()
    print(f'{client_address}와 연결되었습니다.')

    try:
        while True:
            if not audio_queue.empty():
                audio_data = audio_queue.get()  # 큐에서 데이터 가져오기
                client_socket.sendall(audio_data)  # 데이터 전송
    except KeyboardInterrupt:
        print('소켓 전송 종료.')
    finally:
        client_socket.close()
        server_socket.close()

# 녹음 및 소켓 스레드 생성
record_thread = threading.Thread(target=record_audio)
send_thread = threading.Thread(target=send_audio_mqtt)

# 스레드 시작
record_thread.start()
send_thread.start()

# 스레드 종료 대기
record_thread.join()
send_thread.join()
