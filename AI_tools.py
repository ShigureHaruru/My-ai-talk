# AI工具函数模块


# 导入所需的库
import requests
import smtplib
from email.mime.text import MIMEText
from email.header import Header

from key import *



# 导入类型提示
from typing import List, Dict, Callable, Any

# 时间事件表
time_list = {
    
}


"""以下为ai的工具函数"""
def AI_get_weather(city1 : str, city2 : str) -> str:
    """获取指定城市的天气信息。参数： city1：省份名，city2：城市名"""

    try:
        response = requests.get(url=f"https://cn.apihz.cn/api/tianqi/tqyb.php?id=88888888&key=88888888&sheng={city1}&place={city2}")
        data = response.json()
        weather = data.get("weather1")
        return weather

    except:
        return "调用功能当前不可用"
    

    



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

    mail_user = user           
    mail_pass = pass_id        

    sender = mail_user                     

    receivers = send_list  

   
    message = MIMEText(main_text , 'plain', 'utf-8')

    message['Subject'] = Header(title , 'utf-8')
    
    message['From'] = ename 


    try:
        
        smtp_obj = smtplib.SMTP_SSL(mail_host, mail_port)
        
        smtp_obj.login(mail_user, mail_pass)
        
        smtp_obj.sendmail(sender, receivers, message.as_string())
        
        return "邮件发送成功"
        
        smtp_obj.quit()

    except smtplib.SMTPException as e:
        print(f"Error: 无法发送邮件。错误信息：{e}")
        return f"Error: 无法发送邮件。错误信息：{e}"



def AI_add_things(time : str ,things : str ) -> str:
    """添加待办事项的函数
    参数：
    time: 待办事项的时间（例:2025-10-05 18:19）
    things: 待办事项的内容（例:提醒用户上班、帮用户发送邮件给xxx，内容：xxx）
    """
    time_list[time] = things

    print(f"已添加待办事项：{time} - {things}")

    return f"已添加待办事项：{time} - {things}"


"""以上为ai的工具函数"""


def things_del(time):
    del time_list[str(time)]