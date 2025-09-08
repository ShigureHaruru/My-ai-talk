# AI工具函数模块


# 导入所需的库
import requests
import smtplib
from email.mime.text import MIMEText
from email.header import Header



# 导入类型提示
from typing import List, Dict, Callable, Any



# 创建装饰器
def tool(func:Callable) -> Callable:

    # 定义了一个名为 tool 的函数，它接受一个可调用对象（函数）作为参数，并返回一个可调用对象。

    # 添加istool属性，表示这是一个可用的工具函数
    func.is_tool = True
    
    return func






"""以下为ai的工具函数"""

@tool
def AI_get_weather(city1 : str, city2 : str) -> str:
    """获取指定城市的天气信息。参数： city1：省份名，city2：城市名"""

    response = requests.get(url=f"https://cn.apihz.cn/api/tianqi/tqyb.php?id=88888888&key=88888888&sheng={city1}&place={city2}")
    data = response.json()
    weather = data.get("weather1")

    return weather


@tool
def AI_email_send(send_list : List[str] , main_text : str , title : str) -> str:
    """发送邮件的工具函数。
    参数: 
    send_list : 收件人(这是一个列表，可以同时存储多个收件人)
    main_text : 邮件正文
    title : 邮件主题\n

    要求:
    邮件具体内容由你自主创作，但需要表明你的身份是我的助手，
    并且要表达对收件人的感谢之情。
    礼貌真诚且准确地传达主人想要表达的内容，
    格式要整洁，如果需要换行可在段落末尾加上'\n'。
    """

    
    mail_host = "smtp.qq.com"              

    mail_port = 465                        

    mail_user = "huachig@qq.com"           
    mail_pass = "vennakmfcbrmcjeh"         

    sender = mail_user                     

    receivers = send_list  

   
    message = MIMEText(main_text , 'plain', 'utf-8')

    message['Subject'] = Header(title , 'utf-8')
    
    message['From'] = 'huachig <huachig@qq.com>'  


    try:
        
        smtp_obj = smtplib.SMTP_SSL(mail_host, mail_port)
        
        smtp_obj.login(mail_user, mail_pass)
        
        smtp_obj.sendmail(sender, receivers, message.as_string())
        
        return "邮件发送成功"
        
        smtp_obj.quit()

    except smtplib.SMTPException as e:
        print(f"Error: 无法发送邮件。错误信息：{e}")
        return f"Error: 无法发送邮件。错误信息：{e}"


"""以上为ai的工具函数"""
