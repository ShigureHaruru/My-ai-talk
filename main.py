from flask import Flask, g, request, jsonify, render_template  # Flask Web框架相关
from flask_cors import CORS                                    # 跨域请求支持

import AI_tools
import openai
import json
import datetime
import requests
import threading


# 导入向量数据库函数
import tts
from tools_db import *

# 导入tts函数
from tts2 import tts_stream

# 导入key及相关设置
from key import *

# socketio
from flask_socketio import SocketIO, emit




# 修改网页文件路径
app = Flask(__name__ , template_folder="html")

# 初始化SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# 启用CORS(跨域资源共享)，允许前端应用从不同域访问API
CORS(app)


# 直接访问根目录时，渲染并返回主页
@app.route("/")
def index():
    return render_template('index.html')




@app.route("/api/llm",methods = ['POST'])
def api_llm():

        # 获取当前时间
        time = Get_time()

        # 获取请求中的参数(使用flask的request.json)
        data = request.json

        # 获取参数并赋值
        user_input = data.get("u_input","")
        

        # 保存记录逻辑
        if user_input.lower() in ["退出","保存"] :


            # 添加用户输入到消息列表中
            message.append({"role": "user", "content": "我先走开一会哦，很快回来"})

            # 传入相关记录,获取AI回复
            response = llm(time=time,message=message)
 

            
            print("正在存储对话记录...")
                
            with open("message.json" , "w" , encoding = "utf-8") as f:      # "w"覆盖模式

                # ensure_ascii=False  允许非ASCII码直接保存
                # json.dumps 转换为json格式
                f.write(json.dumps(message,ensure_ascii = False))

                print("对话记录已存储。")
                    
            

            # 返回ai的道别
            return jsonify({"response": response , "time":time}) , 200



       


        # 获取相关历史记录
        history = get_history(user_input)

        # 用户输入
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

                    message.append({"role": "assistant", "content": response})

                    # tts后台合成并播放
                    thread = threading.Thread(target=tts_stream , args=(response,))   # args传入参数
                    thread.daemon = True  # 设置为守护线程，主程序退出时自动结束
                    thread.start()
    


                    # 后台运行保存记录
                    def save_in_background():
                        try:

                            is_add = is_important2(user_input, response)

                            if is_add:

                                print("正在存储对话记录...")
                                add_history(user_input, response, str(time))
                                print("对话记录已存储。")

                        except Exception as e:

                            print(f"保存对话记录时出错: {e}")
    
                    # 启动后台线程
                    thread = threading.Thread(target=save_in_background)
                    thread.daemon = True  # 设置为守护线程，主程序退出时自动结束
                    thread.start()
    

                    # 直接返回结果给前端，不等待保存纪录
                    return jsonify({"response": response , "time":time}) , 200

                    # 未调用工具，跳出循环
                    break

                # 调用了工具
                else:
                    for i in AI_tool:

                        # 找到对应工具
                        if json.loads(response)["tool_name"] == i.__name__:

                            # 调用工具
                            rs = i(**iscall[1])


                    # 调用了工具，继续调用大模型
                    res = f"工具：已成功调用工具,返回结果如下：\n" + rs + "\n请根据返回结果，继续和主人自然的交流。如需要使用工具可再次调用。"
                    
                    # 返回结果给ai
                    message.append({"role": "user", "content": res})




        except Exception as e:

            print(f"调用失败：{e}")
            print("请稍后再试！")

            # 出错则移除最后一条用户输入，防止消息列表过长
            message.pop()

            return jsonify({"response": "抱歉，系统出现了一些问题，请稍后再试！" , "time":time}) , 200

          

# 存放所有工具函数
AI_tool=[

    AI_tools.AI_get_weather, # 获取天气

    AI_tools.AI_email_send,   # 发送邮件

    AI_tools.AI_add_things    # 添加代办

    ]


# 判断ai是否调用工具
def is_tool_call(response):

    # 尝试解析为JSON
    try:
        data = json.loads(response)


        # 保存调用参数
        d1 = data.get("parameters")

        return (True,d1)

                
    except:
        # 解析失败
        return (False,"")

    return (False,"")
        



# 获取当前时间
def Get_time():
    now = datetime.datetime.now()

    out = now.strftime("%Y-%m-%d %H:%M")



    return out


# 调用大模型
def llm(time,message):

    # 定义系统角色
    prompt = actor

    tool_txt = "你可以使用以下工具以完成用户的需求(一次仅可请求一个工具):\n"

    # 添加工具描述
    for i in AI_tool:

        # 添加工具描述文本 - 函数名 ： 函数说明
        tool_txt += f"- {i.__name__} ： {i.__doc__}\n"   # doc:函数的文档字符串（docstring）


    use_tool = """
    \n如果你需要使用工具，请按照以下json格式回复(不输出其他内容)：
    {"tool_call": true,"tool_name": "<工具函数名>","parameters": {"<参数1>": "<值1>","<参数2>": "<值2>"}}

    否则直接给出回答即可。
    
    """


    prompt = actor + tool_txt + use_tool


    message[0]["content"] = prompt



    # 调用推理接口
    response = client.chat.completions.create(
        model = llm_model,
        messages = message, # 传入对话消息列表
        temperature = 1.2, # 控制回答的随机性，值越高越随机
        stream = False  # 流式传输
    )



    return response.choices[0].message.content.strip()


    


# 初始化
client = openai.OpenAI(
        base_url = llm_url,
        api_key = key
    )







message = [
        {"role": "system", "content": actor },
        {"role": "user", "content": "你好啊，在干什么呢"}

    ]
        


# 检查当前时间是否有重要事件
def time_check():
    print("check is running")
    while True:
        
        # 获取当前时间
        now_time = Get_time()

        # 遍历时间事件表
        try:
            thing = AI_tools.time_list[str(now_time)]
            

        except Exception as e:
            pass

        # 如果有重要事件
        else:
            message.append({"role": "user", "content": f"系统提示:现在是{now_time}，你记得现在有待办事项：{thing}，请完成！"})
            
            response = llm(time=now_time,message=message)
            
            print(f"汐音:{response}\n")
            
            message.append({"role": "assistant", "content": response})

            # 添加回答发送到前端
            socketio.emit('server_message', {
            'message': response,
            'time': now_time,
            'type': 'notification'
        })

            thread = threading.Thread(target=tts_stream , args=(response,))   # args传入参数
            thread.daemon = True  # 设置为守护线程，主程序退出时自动结束
            thread.start()

            AI_tools.things_del(now_time)




        # 每60秒检查一次
        import time
        # 等待3秒
        time.sleep(10)





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

    
    # 检查是否提醒
    thread = threading.Thread(target=time_check)
    thread.daemon = True  # 设置为守护线程，主程序退出时自动结束
    thread.start()

    socketio.run(app, debug=True, port=10001)


    





    
    
