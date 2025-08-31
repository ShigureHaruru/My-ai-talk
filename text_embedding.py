# 文本转向量模块

import openai

import json





# 文本转换向量函数
def embedding(text):
    client = openai.OpenAI(

        # 阿里百炼服务的base_url 
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  

        # api key
        api_key = "sk-83ea3498d37a491da1959c34fbd647fd"
    )

    # 调用文本转向量模型
    response = client.embeddings.create(
        
        # 使用文本模型v4
        model = "text-embedding-v4",

        # 要转换的文本
        input = text,

        # 向量维度
        dimensions=1024,

        # 返回浮点数据
        encoding_format="float"

    )

    # 返回embedding值(浮点数列表)
    return response.data[0].embedding



