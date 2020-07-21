import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText 


subject = "Here's your attached images" 
body = "Please find your attached images below" 
sender_email = "firstgarage2020@gmail.com"  # Enter your address
receiver_email = "shubhamkumarpro1@gmail.com"  # Enter receiver address
password = input("Type your password and press enter: ")
smtp_server = "smtp.gmail.com"


#Create a multipart message
message = MIMEMultipart()
message['From']  = sender_email
message['To'] = receiver_email
message['subject'] = subject


message.attach(MIMEText(body, "plain"))

filename = "imageOne.jpg"

with open(filename, "rb") as attachment:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())


encoders.encode_base64(part)

part.add_header(
        "Content-Disposition", 
        f"attachment; filename = {filename}",
)


message.attach(part)
text = message.as_string()

port = 465

print("Trying to create ssl context \n")

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    print("server login complete")
    server.sendmail(sender_email, receiver_email, message)
    print("Mail sent successfully \n")
