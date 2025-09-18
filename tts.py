# tts(非流式合成版)

# 导入阿里模型库
from os import system
import dashscope

# 使用v2版本的tts    
from dashscope.audio.tts_v2 import VoiceEnrollmentService, SpeechSynthesizer

import time

from playsound import playsound

# 获取key
from key import ali_key 



# 创建语音注册服务实例
service = VoiceEnrollmentService()

# 调用create_voice方法复刻声音，并生成voice_id

dashscope.api_key = ali_key


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

# vioce_id_1 = cosyvoice-v2-v-b51f4f711649476dbbff40753fb5c03c


# 进行TTS合成
def tts(text):
    client = SpeechSynthesizer(
        model ="cosyvoice-v2",  # 使用v2模型
        voice = "cosyvoice-v2-v-b51f4f711649476dbbff40753fb5c03c",  # 使用复刻的音色ID
        speech_rate = 1.1 # 语速调整，1.0为正常语速
    )

    response = client.call(text=text)

    with open("output.mp3", "wb") as f:
        f.write(response)
        
    playsound("output.mp3")









    