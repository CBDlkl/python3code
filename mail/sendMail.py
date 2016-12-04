import smtplib
from email.mime.text import MIMEText
from email.header import Header

mailto_list = ['likeli@jsj.com.cn']  # 收件人(列表)
mail_host = "smtp.163.com"
mail_user = "18672959719"
mail_pass = "lkl5282784"
mail_postfix = "163.com"


def send_mail(to_list, sub, content):
    me = "hello" + "<" + mail_user + "@" + mail_postfix + ">"
    msg = MIMEText(content, _subtype='plain')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)  # 将收件人列表以‘；’分隔
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)  # 连接服务器
        server.login(mail_user, mail_pass)  # 登录操作
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception as e:
        print(str(e))
        return False


for i in range(1):  # 发送1封，上面的列表是几个人，这个就填几
    if send_mail(mailto_list, "电话", "电话是XXX"):  # 邮件主题和邮件内容
        # 这是最好写点中文，如果随便写，可能会被网易当做垃圾邮件退信
        print("done!")
    else:
        print("failed!")
