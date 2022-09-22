from time import sleep
from typing import Optional
from pyaudio import PyAudio, paInt16
from pydub import AudioSegment
import numpy as np
from numpy import fft
from math import sqrt
from threading import Thread
from audioop import rms

p = PyAudio()

def perform_fft(chunk: bytes):
    np_chunk = np.frombuffer(chunk, dtype=np.int16)
    fft_complex = fft.rfft(np_chunk, norm="ortho", n=1024)
    fft_complex /= len(fft_complex)
    fft_values = list(sqrt(v.imag * v.imag + v.real * v.real) for v in fft_complex)
    return fft_values

class AudioThread(Thread):
    audio: AudioSegment
    byte_offset: int
    chunk_size: int

    def __init__(self, audio: AudioSegment, chunk_size: int):
        super().__init__()
        self.audio = audio
        self.byte_offset = 0
        self.chunk_size = chunk_size
        self.playing = True
        self._terminate = False

        self.oustream = p.open(
            format = p.get_format_from_width(self.audio.sample_width), # type: ignore
            channels = self.audio.channels, # type: ignore
            rate = self.audio.frame_rate, # type: ignore
            output = True # type: ignore
        )

    def get_chunk(self):
        return self.audio.raw_data[self.byte_offset:self.byte_offset + self.chunk_size] # type: ignore

    def run(self):
        while not self._terminate:
            if self.playing:
                chunk = self.get_chunk()
                self.oustream.write(chunk)
                self.byte_offset += self.chunk_size

    def stop(self):
        self.playing = False
        self.byte_offset = 0

    def pause(self):
        self.playing = False

    def resume(self):
        self.playing = True

    def terminate(self):
        self._terminate = True

    def __del__(self):
        self.terminate()
        self.oustream.stop_stream()
        self.oustream.close()

class AudioFile:
    thread: AudioThread
    data: AudioSegment

    def __init__(self, filename: str, chunk_size: int = 1024):
        audio_segment: AudioSegment = AudioSegment.from_file(filename) # type: ignore
        self.data = audio_segment
        self.thread = AudioThread(audio_segment, chunk_size)

    def get_chunk(self) -> bytes:
        return self.thread.get_chunk()

    def get_fft(self):
        return perform_fft(self.thread.get_chunk())

    def get_rms(self):
        chunk = self.thread.get_chunk()
        width: int = self.data.sample_width # type: ignore
        return rms(chunk, width)

    def play(self):
        self.thread.start()

    def stop(self):
        if self.thread.is_alive():
            self.thread.stop()

    def resume(self):
        if self.thread.is_alive():
            self.thread.resume()

    def pause(self):
        if self.thread.is_alive():
            self.thread.pause()

    def terminate(self):
        if self.thread.is_alive():
            self.thread.terminate()

    def __del__(self):
        self.terminate()

def smooth_fft_values(fft_values, new_fft_values, smoothing):
    if len(fft_values) != len(new_fft_values):
        for i in range(len(fft_values)):
            fft_values[i] = new_fft_values[i]
        for i in range(len(fft_values), len(new_fft_values)):
            fft_values.append(new_fft_values[i])

        return

    for i in range(len(fft_values)):
        fft_values[i] *= smoothing
        fft_values[i] += (new_fft_values[i] - fft_values[i]) * (1-smoothing)

class MicThread(Thread):
    current_chunk: bytes
    chunk_size: int
    chunk_rate: int

    def __init__(self, mic_info, chunks_per_second: int):
        super().__init__()
        self.chunks_per_second = chunks_per_second
        self._terminate = False
        self.current_chunk = b''

        self.chunk_rate = int(mic_info["defaultSampleRate"])
        self.chunk_size = int((1/chunks_per_second) * self.chunk_rate)
        self.micstream = p.open(
            format = paInt16,
            channels = 1,
            rate = self.chunk_rate,
            frames_per_buffer = self.chunk_size,
            input = True
        )

    def get_chunk(self):
        return self.current_chunk

    def run(self):
        while not self._terminate:
            self.current_chunk = self.micstream.read(self.chunk_size)

    def terminate(self):
        self._terminate = True

    def __del__(self):
        self.terminate()
        self.micstream.stop_stream()
        self.micstream.close()

class AudioMic:
    thread: MicThread

    def __init__(self, mic_index: Optional[int] = None, chunks_per_second: int = 30):
        mic_info = None
        if mic_index != None:
            mic_info = p.get_device_info_by_index(mic_index)
        else:
            mic_info = p.get_default_input_device_info()

        self.thread = MicThread(mic_info, chunks_per_second)
        self.thread.start()

    def get_chunk(self):
        return self.thread.get_chunk()

    def get_fft(self):
        return perform_fft(self.thread.get_chunk())

    def get_rms(self):
        chunk = self.thread.get_chunk()
        return rms(chunk, 2)

    def terminate(self):
        if self.thread.is_alive():
            self.thread.terminate()

    def __del__(self):
        self.terminate()

def list_input_devices() -> list[tuple[int, str]]:
    devices = []
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if info["maxInputChannels"] > 0: # type: ignore
            devices.append((i, info["name"]))
    return devices

# def get_mic_chunk_size(p: PyAudio, chunks_per_second: int = 60):
#     device_info = p.get_default_input_device_info()
#     assert device_info
#
#     rate = int(device_info["defaultSampleRate"])
#     return int((1/chunks_per_second) * rate)
#
# def open_mic_stream(p: PyAudio, samplerate: int, chunk_size: int = 60) -> Stream:
#     return p.open(
#         format = paInt16,
#         channels = 1,
#         rate = samplerate,
#         frames_per_buffer = chunk_size,
#         input = True
#     )
#
# def open_out_stream(p: PyAudio, sound: AudioSegment) -> Stream:
#     return p.open(
#         format = p.get_format_from_width(sound.sample_width),
#         channels = sound.channels,
#         rate = sound.frame_rate,
#         frames_per_buffer = sound.frame_width,
#         output = True
#     )
