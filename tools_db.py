
# 导入向量数据库
import chromadb

from chromadb.config import Settings

# 导入文本转换向量函数
from text_embedding import embedding 




# 初始化ChromaDB向量数据库客户端
# 自动保存版
# 保存到当前目录下的db文件夹中
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



def get_history(query,n_results = 5):

    # 将查询文本转换为向量表示
    query_embedding = embedding(query)

    # 从数据库中检索与查询向量最相似的记录
    results = collection.query(

    # 查询向量
    query_embeddings = [query_embedding],

    # 返回最相似的记录数(默认5条)
    n_results = n_results

    )
    
    # 判断是否有搜索结果
    if len(results['documents'][0]) == 0:
        return None
        print("没有找到相关的历史记录。")

    else:

        # 返回搜索结果的文本内容
        response = results['documents'][0]
        print("找到相关的历史记录:",len(response))
        



def is_important(user_input,ai_output):

    # 用户输入包含以下关键词则视为重要
    important_keywords = [
        "喜欢", "讨厌", "过敏", "生日", 
        "纪念日", "梦想", "希望", "想要", "害怕", 
        "地址", "号码", "答应", "保证"]

    # 检查用户输入中是否包含任何重要关键词
    for keyword in important_keywords:
        if keyword in user_input:
            return True


    # 包含以下关键词则视为重要
    commitment_words = ["下次", "以后", "明天", "周末", "给你做", "帮你", "记下了", "记住了"]

    # 检查AI回答和用户说话中是否包含任何重要关键词
    for word in commitment_words:
        if word in ai_output or word in user_input:
            return True
        
        
    
    # 默认不重要   
    return False


        # 检查AI回答中是否包含任何重要关键词
        
    

