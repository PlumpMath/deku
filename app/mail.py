# Module that handles emailing users.
# Emails sent on registration and if a password reset is needed.

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender = "dekudevs@gmail.com"
senderPassword = "flaskandbackbone"
templateDir = '/home/vagrant/Section-2-Team-6/app/mail_templates/'

def generateEmail(emailType, **kwargs):
    # Get templates from template directory.
    textTemplate = open(templateDir + emailType + ".txt", 'r')
    text = textTemplate.read().format(**kwargs)
    textTemplate.close()

    htmlTemplate = open(templateDir + emailType + ".html", 'r')
    html = htmlTemplate.read().format(**kwargs)
    htmlTemplate.close()

    return [text, html]

def sendEmail(address, subject, text, html):
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = address

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)
    
    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.ehlo()
    server.starttls() 
    server.login(sender, senderPassword)
    server.sendmail(sender, [address], msg.as_string())
    server.quit()

