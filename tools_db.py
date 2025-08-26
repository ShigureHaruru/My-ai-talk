import chromadb

from chromadb.config import Settings

# 导入向量文本嵌入模型
from sentence_transformers import SentenceTransformer


embed_model = SentenceTransformer('./GanymedeNil/text2vec-large-chinese') # 中文模型


# 初始化ChromaDB向量数据库客户端
client = client = chromadb.PersistentClient(path="./db")


# 创建或获取一个名为"AI_talk_history"的集合
# 该集合用于存储AI与对话的历史记录
collection = client.get_or_create_collection(name = "AI_talk_history")



# 将对话记录添加到向量数据库中
def add_history(user_input,ai_output,time):
    
    # 将用户输入和AI回答合并以及当前时间合并为一个字符串
    history_text = f"时间:{time},用户输入:{user_input},AI回答:{ai_output}"

    # 将文本转换为向量表示
    # tolist()将NumPy数组转换为Python原生列表
    embed_text = embed_model.encode(history_text).tolist()


    print(embed_text)
    print(embed_model)


add_history("你好","你好呀","2024-10-10 10:10:10")
