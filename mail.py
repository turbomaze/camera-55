import os
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

def send_email(user, pwd, recipient, subject, body, img_file_name):
    img_data = open(img_file_name, 'rb').read()
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = user
    msg['To'] = recipient

    text = MIMEText(body)
    msg.attach(text)
    image = MIMEImage(img_data, name=os.path.basename(img_file_name))
    msg.attach(image)

    try:
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(user, pwd)
        s.sendmail(msg['From'], msg['To'], msg.as_string())
        s.quit()
        print 'Successfully sent mail at %s' % str(time.time())
    except Exception as e:
        print e
