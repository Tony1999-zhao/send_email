import smtplib
import csv
import os #打开系统路径
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


end_str = '@qq.com'
from_addr = input('请输入发送人qq号：')+ end_str #用户名
password = input('请输入授权码：') #授权码
smtp_server = 'smtp.qq.com'  #邮箱服务器地址
content = input('请输入你要发送的内容：')#发送内容
subject = input('请输入邮箱标题：')
add_image = input("是否添加图片？按任意键继续不添加，按y添加图片")
if add_image == 'y':
    img_file = open('./d4.png','rb').read()
    msg_img = MIMEImage(img_file)
    msg_img.add_header('Content-Disposition','attachment', filename = "image.jpg")
    msg_img.add_header('Content-ID', '<0>')

add_att = input("是否添加附件？按任意键继续不添加，按y添加附件")#添加附件
 #构造附件1，传送当前目录下  文件
att1 = MIMEText(open('./to_addrs.csv','rb').read(),'base64','utf-8') # rb以二进制方式读取
# att1["Content-Type"] = 'application/octet-stream'
# filename为附件名称，可以任意写，写什么名字，邮件中显示什么名字
att1["Content-Disposition"] = 'attachment; filename = "to_addrs.csv" '
 #将附件添加到MIMEMultipart中

to_addrs = [] #对方邮箱账号
while True:
    qq_num = input('请输入你要发送的联系人qq号：')
    to_addrs.append([qq_num+end_str])
    qustion = input('是否继续添加？按n退出，任意键继续输入')
    if qustion == 'n':
        break


# 这边要存储多维数组才能方便后面的csv的调用，否则会报错；
#使用csv来存储发送的人
with open("./to_addrs.csv","w",newline="") as f :
    writer = csv.writer(f)
    for row in to_addrs:
        writer.writerow(row)

# 打开文件
with open("./to_addrs.csv","r",newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        to_addrs = row[0]
        ## 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码


        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = from_addr
        msg['TO'] = to_addrs
        msg.attach(MIMEText(content,'plain','utf8'))
        msg.attach(msg_img) #传输图片内容
        msg.attach(att1)
        server = smtplib.SMTP_SSL(host=smtp_server) # 实例化一个SMTP的对象,python3.7中更新了配置需要在这里加上服务器地址
        server.connect(smtp_server,465) #连接到邮箱的服务器地址，以及端口
        server.set_debuglevel(1) #debug抓取错误
        server.login(from_addr, password)#登录邮箱
        try:
            server.sendmail(from_addr,to_addrs, msg.as_string())#发送消息

            print("发送成功！")
        except:
            print("发送失败,邮箱是%s"%(to_addrs))
server.quit()#退出STMP;




