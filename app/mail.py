# Module that handles emailing users.
# Emails sent on registration and if a password reset is needed.

import smtplib
from email.mime.text import MIMEText

sender = "dekudevs@gmail.com"
senderPassword = "flaskandbackbone"

def registerEmail(address, firstName):
    message = "Hey, " + firstName + "! Welcome to Deku."
    msg = MIMEText(message)
    msg['Subject'] = "Welcome to Deku!"
    msg['From'] = sender
    msg['To'] = address
    
    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.ehlo()
    server.starttls() 
    server.login(sender, senderPassword)
    server.sendmail(sender, [address], msg.as_string())
    server.quit()

def resetPasswordEmail(address, firstName):
    message = "Hey, " + firstName + "! We're sending you this because you forgot your password.\n"
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
