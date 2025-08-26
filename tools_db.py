
# 导入向量数据库
import chromadb

from chromadb.config import Settings

# 导入文本转换向量函数
from text_embedding import embedding 




# 初始化ChromaDB向量数据库客户端
# 自动保存版
client = chromadb.PersistentClient(path="./db")


# 创建或获取一个名为"AI_talk_history"的集合
# 该集合用于存储AI与对话的历史记录
collection = client.get_or_create_collection(name = "AI_talk_history")



# 将对话记录添加到向量数据库中
def add_history(user_input,ai_output,time):
    
    # 将用户输入和AI回答合并以及当前时间合并为一个字符串
    history_text = f"时间:{time},用户输入:{user_input},AI回答:{ai_output}"


    # 调用函数将文本转换为向量表示
    embed_text = embedding(history_text)


    # 存储对话记录到数据库
    collection.add(

        # 原始文本
        documents = history_text,

        # 转换后的向量
        embeddings = embed_text,

        # 唯一标识符(使用当前时间)
        ids = time
    )

    

