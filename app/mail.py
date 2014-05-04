# Module that handles emailing users.
# Emails sent on registration and if a password reset is needed.

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re

sender = "dekudevs@gmail.com"
senderPassword = "flaskandbackbone"
templateDir = '/home/vagrant/Section-2-Team-6/app/mail_templates/'

def registerEmail(address, firstName):
    # Get templates from template directory.
    textTemplate = open(templateDir + "registration.txt", 'r')
    text = parseMessage(textTemplate.read(), firstName = firstName)
    textTemplate.close()

    htmlTemplate = open(templateDir + "registration.html", 'r')
    html = parseMessage(htmlTemplate.read(), firstName = firstName)
    htmlTemplate.close()

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Welcome to Deku!"
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

def resetPasswordEmail(address, firstName, tempPassword):
    message = "Hey, " + firstName + "! We're sending you this because you forgot your password.\n"
    message += "Please use " + tempPassword + " to log in and add a new password immediately."
    msg = MIMEText(message)
    msg['Subject'] = "Forgot your password?"
    msg['From'] = sender
    msg['To'] = address

    server = smtplib.SMTP(host="smtp.gmail.com", port=587)
    server.ehlo()
    server.starttls()
    server.login(sender, senderPassword)
    server.sendmail(sender, [address], msg.as_string())
    server.quit()

def parseMessage(template, **kwargs):
    for key in kwargs:
        template = re.sub('\{(%s)\}' % key, kwargs[key], template)
    return template
        
