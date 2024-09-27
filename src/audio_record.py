import pyaudio
import wave

# audio_device_list 에서 확인한 DEVICE_ID로 변경
MIC_DEVICE_ID = 3

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
SAMPLE_SIZE = 2  # FORMAT의 바이트 수

def record(record_seconds):
    p = pyaudio.PyAudio()
    stream = p.open(input_device_index=MIC_DEVICE_ID,
                    format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    print("Start to record the audio.")
    frames = []

    for i in range(0, int(RATE / CHUNK * record_seconds)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Recording is finished.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    return frames


# 녹음 데이터를 WAV 파일로 저장하기
def save_wav(target, frames):
    wf = wave.open(target, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(SAMPLE_SIZE)
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))

    if isinstance(target, str):
        wf.close()

if __name__ == '__main__':
    RECORD_SECONDS = 5
    frames = record(RECORD_SECONDS)

    WAVE_OUTPUT_FILENAME = "output.wav"
    save_wav(WAVE_OUTPUT_FILENAME, frames)