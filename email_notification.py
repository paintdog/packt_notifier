#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://codingworld.io/project/e-mails-versenden-mit-python

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from settings import settings


""" Warning!

If you use web.de like me, you must first
allow the use of smtp and imap in the settings.

Otherwise you will receive an error message:

smtplib.SMTPAuthenticationError()

"""

def email_notification(settings, subject, text):
    msg            = MIMEMultipart()
    msg['From']    = settings["senderEmail"]
    msg['To']      = settings["empfangsEmail"]
    msg['Subject'] = subject

    emailText      = text
    msg.attach(MIMEText(emailText, 'html'))

    server = smtplib.SMTP(settings["smtp_server"], settings["smtp_server_port"])
    server.starttls()
    server.login(settings["senderEmail"], settings["senderPasswort"])
    text = msg.as_string()
    server.sendmail(settings["senderEmail"], settings["empfangsEmail"], text)
    server.quit()


if __name__ == "__main__":

    email_notification(settings,
                       "This is my subject",
                       "<b>Here comes my text!</b><br><ul><li>List 1</li><li>List 2</li></ul><p>Greetings</p>")
    
