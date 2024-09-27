import socket
import pyaudio
import wave

# 서버의 IP 주소와 포트 번호
SERVER_IP = '192.168.1.194'
PORT = 12345

# 오디오 설정
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 22050  # 서버와 동일한 샘플레이트로 설정

# 소켓 설정 및 서버에 연결
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, PORT))
print(f'서버 {SERVER_IP}:{PORT}에 연결되었습니다.')

# 오디오 스트림 설정
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

# .wav 파일 설정
output_filename = "received_audio.wav"
wave_file = wave.open(output_filename, 'wb')
wave_file.setnchannels(CHANNELS)
wave_file.setsampwidth(audio.get_sample_size(FORMAT))
wave_file.setframerate(RATE)

try:
    while True:
        # 서버로부터 데이터 수신
        audio_data = client_socket.recv(CHUNK)

        # 데이터가 없으면 연결 종료
        if not audio_data:
            break

        # 수신한 데이터 오디오로 재생
        stream.write(audio_data)

        # 수신한 데이터를 .wav 파일에 저장
        wave_file.writeframes(audio_data)
except KeyboardInterrupt:
    print('클라이언트 연결 종료.')
finally:
    # 스트림 및 소켓 닫기
    stream.stop_stream()
    stream.close()
    audio.terminate()
    wave_file.close()
    client_socket.close()

print(f'녹음된 오디오가 {output_filename} 파일에 저장되었습니다.')
