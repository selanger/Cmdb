import smtplib
from email.mime.text import MIMEText

subject = "好好学习"  ### 邮件主题
content = "这是一个好好学习的邮件"
sender = "str_wjp@163.com"
recver = "str_wjp@126.com,674948919@qq.com"

password = "123456a"  ## 邮箱授权密码，不是邮箱的登陆密码

## 构建邮件内容
message = MIMEText(content, "plain", "utf-8")
#     内容
#     内容类型
#     编码格式

message["Subject"] = subject
message["From"] = sender
message["To"] = recver


## 发送邮件
smtp = smtplib.SMTP_SSL("smtp.163.com",465)
smtp.login(sender,password)
smtp.sendmail(sender,recver.split(","),message.as_string())
    #发送人
    #接收人 需要是一个列表 []
    #发送邮件 as_string是一种类似json的封装方式，目的是为了在协议上传输邮件内容
smtp.close()
