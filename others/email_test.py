from email.mime.text import MIMEText
msg = 'hello, send by yyf...miss zxj day:'
# 输入Email地址和口令:
from_addr = "alex.yyf1992@gmail.com"
password = "youyangfan"
# 输入收件人地址:
to_addr = '460193360@qq.com'
# 输入SMTP服务器地址:
smtp_server = 'smtp.gmail.com'

import smtplib
server = smtplib.SMTP(smtp_server, 587) # SMTP协议默认端口是25
server.set_debuglevel(1)
server.ehlo()
server.starttls()
server.login(from_addr, password)
for n in range(1,11):
    server.sendmail(from_addr, [to_addr], MIMEText(msg+str(n), 'plain', 'utf-8').as_string())
# server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()
print('1111'+str(1))