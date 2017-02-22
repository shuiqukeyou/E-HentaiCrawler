import smtplib
from email.mime.text import MIMEText

# 过年那几天我摸鱼时用的一个函数，调用的是QQ邮箱的SMTP服务，发送到一个我新注册的邮箱中，以提示我程序断了。
# 事实上只在API部分用过
def remind(text):
    _user = "邮箱"
    _pwd  = "密码"
    _to   = "目标邮箱"

    msg = MIMEText(text)
    msg["Subject"] = "EH程序出现错误"
    msg["From"]    = _user
    msg["To"]      = _to

    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(_user, _pwd)
        s.sendmail(_user, _to, msg.as_string())
        s.quit()
        print ("Success!")
    except smtplib.SMTPException as e:
        print ("Falied,%s"%e)