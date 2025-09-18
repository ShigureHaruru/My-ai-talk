from AI_tools import *
import openai
import json
import datetime
import requests


# 导入向量数据库函数
from AI_talk import tts
from tools_db import add_history , get_history , is_important

# 导入tts函数
from tts2 import tts_stream

# 导入key及相关设置
from key import ds_key , actor2 , voiceid







# 存放所有工具函数
AI_tools=[

    AI_get_weather, # 获取天气

    AI_email_send   # 发送邮件

    ]


# 判断ai是否调用工具
def is_tool_call(response):

    # 判断开头结尾是否为{}
    if response.strip().startswith('{') and response.strip().endswith('}'):

        # 尝试解析为JSON
        try:
            data = json.loads(response)

            # 检查是否呼叫工具
            if data["tool_call"]:

                # 保存调用参数
                d1 = data.get("parameters")

                return (True,d1)

                
        except:
            # 解析失败
            return (False,"")

    return (False,"")
        



# 获取当前时间
def Get_time():
    time = datetime.datetime.now()

    return time


# 调用大模型
def llm(time,message):

    # 定义系统角色
    prompt = actor2

    tool_txt = "你可以使用以下工具以完成用户的需求(一次仅可请求一个工具):\n"

    # 添加工具描述
    for i in AI_tools:

        # 添加工具描述文本 - 函数名 ： 函数说明
        tool_txt += f"- {i.__name__} ： {i.__doc__}\n"   # doc:函数的文档字符串（docstring）


    use_tool = """
    \n如果你需要使用工具，请按照以下json格式回复(不输出其他内容)：
    {"tool_call": "true","tool_name": "<工具函数名>","parameters": {"<参数1>": "<值1>","<参数2>": "<值2>"}}

    否则直接给出回答即可。
    注意：json格式需要使用双引号\n
    """


    prompt = actor2 + tool_txt + use_tool

    message[0]["content"] = prompt



    # 调用推理接口
    response = client.chat.completions.create(
        model = "deepseek-chat",
        messages = message, # 传入对话消息列表
        temperature = 1.3, # 控制回答的随机性，值越高越随机
        stream = False  # 流式传输
    )



    return response.choices[0].message.content.strip()


    


# 初始化
client = openai.OpenAI(
        base_url = "https://api.deepseek.com/v1",
        api_key = ds_key
    )







message = [
        {"role": "system", "content": actor2 },
        {"role": "user", "content": "你好啊，在干什么呢"}

    ]
        


# 主程序
if __name__ == "__main__":


    
    # 获取时间
    time = Get_time()

    # 欢迎界面
    print("欢迎使用AI聊天系统！")
    print("会话启动时间:",time)
    print("输入'退出'以结束对话。")
    print("===========================")


    try:

        # 尝试读取历史记录文件
        with open("message.json" , "r" , encoding = "utf-8") as f:
            
            # 读取文件内容
            history_data = f.read()


            # 判断文件内容是否为空
            if  history_data.strip() != "":
                
                # 解析JSON数据
                history_messages = json.loads(history_data)

                # 将历史记录替换到消息列表中
                message = history_messages

                print("已加载历史对话记录。")


            else:

                print("没有找到历史对话记录文件，开始新的对话。")


                # 激活初始对话
                response = llm(time=time,message=message)

                


                # 添加回答到消息列表中
                message.append({"role": "assistant", "content": response})


    except:
           print("没有找到历史对话记录文件，开始新的对话。")


           # 激活初始对话
           response = llm(time=time,message=message)

           


           # 添加回答到消息列表中
           message.append({"role": "assistant", "content": response})


    
    while True:
        user_input = input("你:")


        # 退出逻辑
        if user_input.lower() == "退出":

            # 添加用户输入到消息列表中
            message.append({"role": "user", "content": "我先走开一会哦，很快回来"})

            # 传入相关记录,获取AI回复
            llm(time=time,message=message)

            # 询问是否保存记录
            a = input("是否保存本次对话以便下次继续？(Y/N)：")
            
            if a.lower() == "y":
                print("正在存储对话记录...")
                
                with open("message.json" , "w" , encoding = "utf-8") as f:      # "w"覆盖模式

                    # ensure_ascii=False  允许非ASCII码直接保存
                    # json.dumps 转换为json格式
                    f.write(json.dumps(message,ensure_ascii = False))

                    print("对话记录已存储。")
                    
            
            elif a.lower() == "n":
                with open("message.json" , "w" , encoding = "utf-8") as f:
                    pass  # 清空文件内容


            else:
                print("输入有误，默认保存记录。")

                with open("message.json" , "w" , encoding = "utf-8") as f:      # "w"覆盖模式

                    # ensure_ascii=False  允许非ASCII码直接保存
                    # json.dumps 转换为json格式
                    f.write(json.dumps(message,ensure_ascii = False))

                    print("对话记录已存储。")

            break

        time = Get_time()


        # 获取相关历史记录
        history = get_history(user_input)


        user_input_all = f"""
        以下是你和主人过去的对话历史记录:

        {history}

        以上是你和主人过去的对话历史记录，请根据以上这些背景和当前对话，继续和主人自然的交流。

        注意：
        - 1.你仅可进行纯口语输出：只说你讲的话，绝对不要描述动作、神态、表情或环境！！！
        - 2.只有"用户输入:"后面的内容是主人刚刚说的话，请不要把历史记录当做主人的话。


        时间:{time}

        用户输入:{user_input}

        """
        

        # 添加用户输入到消息列表中
        message.append({"role": "user", "content": user_input_all})



        # 控制消息列表长度，防止过长
        if len(message) > 40:
            # 移除最早的一轮对话
            message.remove(message[1]) 
            message.remove(message[1])

        try:

            while True:
                # 传入相关记录,获取AI回复
                response = llm(time=time,message=message)

                # 判断是否调用工具
                iscall = is_tool_call(response)

                
                # 判断是否调用工具
                if (iscall[1] == ""):
                    print(f"汐音:{response}\n")

                    # 未调用工具，跳出循环
                    break

                # 调用了工具
                else:
                    for i in AI_tools:

                        # 找到对应工具
                        if json.loads(response)["tool_name"] == i.__name__:

                            # 调用工具
                            rs = i(**iscall[1])


                    # 调用了工具，继续调用大模型
                    res = f"工具：已成功调用工具,返回结果如下：\n" + rs + "\n请根据返回结果，继续和主人自然的交流。如需要使用工具可再次调用。"
                    
                    # 返回结果给ai
                    message.append({"role": "user", "content": res})




            # 添加回答到消息列表中
            message.append({"role": "assistant", "content": response})

            # 判断记录是否需要存储
            is_add = is_important(user_input,response)

            # 存储对话记录
            if (is_add):

                print("正在存储对话记录...")

                # 转化时间为字符串
                add_history(user_input,response,str(time))

                print("对话记录已存储。")

        except Exception as e:
            print(f"调用失败：{e}")
            print("请稍后再试！")

            # 出错则移除最后一条用户输入，防止消息列表过长
            message.pop()

            # 继续
            continue


        



        


