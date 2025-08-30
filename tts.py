from email.mime import base
import os
from sqlite3 import connect
from turtle import update


# 导入阿里模型库
import dashscope

# 使用v2版本的tts    
from dashscope.audio.tts_v2 import VoiceEnrollmentService, SpeechSynthesizer

# 用于解码TTS服务返回的base64编码的音频数据
import base64

# 提供线程同步机制，确保主线程等待合成完成
import threading

import time

# TTS实时合成相关的核心类
from dashscope.audio.qwen_tts_realtime import QwenTtsRealtime, QwenTtsRealtimeCallback, AudioFormat




# 创建语音注册服务实例
service = VoiceEnrollmentService()

# 调用create_voice方法复刻声音，并生成voice_id

dashscope.api_key = "sk-83ea3498d37a491da1959c34fbd647fd"


# 复刻声音，返回voice_id   
def create_voice(file_url,voice_name):
    

    # 开始创建音色
    new_id = service.create_voice(

        # 使用v2模型
        target_model = "cosyvoice-v2",

        # 音色名称
        prefix = voice_name,

        # 音色文件url
        url = file_url
        
    )

    return new_id

# vioce_id_1 = cosyvoice-v2-v1-d9643e6da37e4ad195a6519fde12e066


# 进行TTS合成
def tts(text):
    client = SpeechSynthesizer(
        model ="cosyvoice-v2",  # 使用v2模型
        voice = "cosyvoice-v2-v1-d9643e6da37e4ad195a6519fde12e066",  # 使用复刻的音色ID
    )

    response = client.call("hello")

    with open("output.wav", "wb") as f:
        f.write(response)




print(create_voice(file_url="https://raw.githubusercontent.com/ShigureHaruru/My-ai-talk/refs/heads/main/voice.mp3?token=GHSAT0AAAAAADIXJJS564U5I56KWCZF5O2S2FTITYA",voice_name="v"))

    