try:
    import smtplib, ssl
    import requests
    import json
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.header import Header
except Exception as e:
    print("[!] ERROR on importing module:\n",e)
    exit(0)

#   readHTML("https://grader.ga/static/functions/verify/email.html")
def readHTML(url:str):
    req = requests.get(url)
    if (req.status_code != 200):
        return -1
    req.encoding = req.apparent_encoding
    return req.text

"""Expected Parameters
    sender(str) -> sender information, need to specify in pattern : name;email;password
    receiver(str) -> receiver information, only email.
    subject(str) -> title of the email.
    mail(str) -> source to be email template. If you have any variable to replace, be sure that it's in "{{variable}}" format
    variable(str) -> any variable that being to replace from email template. Can't be empty but can send empty json ("{}").
"""
#   sendEmail("PondJa;p0ndja.dev@gmail.com;fbP>ZM4kZVPM","pondja2545@gmail.com","Test Email Jaaaa","https://grader.ga/static/functions/verify/email.html","""{"name":"Palapon!"}""")
def sendEmail(sender:str,receiver:str,subject:str,mail:str,variable:str):
    
    sender = sender.split(';')
    if (len(sender) != 3):
        return 0
    sender_name = sender[0]
    sender_email = sender[1]
    sender_password = sender[2]


    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = str(Header(f'{sender_name} <{sender_email}>'))
    message["To"] = receiver

    content_html = readHTML(mail)
    var = json.loads(variable)
    for v in var:
        content_html = content_html.replace("{{"+v+"}}",var[v])
    content = MIMEText(content_html, "html")

    message.attach(content)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        try:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver, message.as_string())
            server.quit()
            return 1
        except Exception as e:
            print(e)
            return -9