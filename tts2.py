# tts(流式合成版)

import os
import dashscope
import pyaudio
import threading
from dashscope.audio.tts_v2 import SpeechSynthesizer, ResultCallback, AudioFormat

# 确保已设置你的 API Key
dashscope.api_key = "sk-83ea3498d37a491da1959c34fbd647fd"  # 建议改为从环境变量读取

class TTSStreamCallback(ResultCallback):
    """处理流式音频数据的回调类"""
    def __init__(self):
        super().__init__()
        self.audio_queue = []  # 用于存储音频数据块的队列
        self.completion_event = threading.Event()
        self._player = pyaudio.PyAudio()
        # 根据你选择的音频格式打开输出流，CosyVoice-v2 流式通常使用 PCM
        self._audio_stream = self._player.open(
            format=self._player.get_format_from_width(2),  # 16bit PCM
            channels=1,  # 单声道
            rate=22050,   # 采样率，需与 AudioFormat 匹配，例如 22050 Hz
            output=True
        )

    def on_open(self):
        """连接建立时调用"""
        pass

    def on_data(self, data: bytes):
        """收到音频数据时调用"""

        # 将收到的音频数据立即播放
        self._audio_stream.write(data)

        # 也可存入队列供其他地方使用
        self.audio_queue.append(data)

    def on_complete(self):
        """合成完成时调用"""
        self.completion_event.set()

    def on_error(self, error_msg: str):
        """发生错误时调用"""
        print(f"\nTTS合成发生错误: {error_msg}")
        self.completion_event.set()

    def on_close(self):
        """连接关闭时调用"""
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self._player.terminate()

    def wait_until_completion(self):
        """等待合成完成"""
        self.completion_event.wait()

def tts_stream(text, voice_id):
    """
    使用流式合成并播放语音
    """
    # 初始化回调处理器
    callback = TTSStreamCallback()
    
    # 初始化合成客户端，指定音频格式用于流式
    client = SpeechSynthesizer(
        model="cosyvoice-v2",
        voice=voice_id,
        callback=callback,  # 设置回调
        format=AudioFormat.PCM_22050HZ_MONO_16BIT,  # 流式调用需指定格式
        speech_rate = 1.2 # 语速调整，1.0为正常语速
    )
    
    # 开始流式合成
    client.streaming_call(text)  # 对于长文本，可考虑分多次 streaming_call

    # 如果需要结束流式输入，调用 client.streaming_complete()

    client.streaming_complete()
    
    # 等待合成播放完成
    callback.wait_until_completion()

