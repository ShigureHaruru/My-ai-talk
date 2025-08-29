import os


# 导入阿里模型库
import dashscope
# 使用v2版本的tts    
from dashscope.audio.tts_v2 import VoiceEnrollmentService

# 创建语音注册服务实例
service = VoiceEnrollmentService()

# 调用create_voice方法复刻声音，并生成voice_id

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


create_voice()
    