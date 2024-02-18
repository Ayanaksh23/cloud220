import ssl
import smtplib
from email.message import EmailMessage


def sendfinalmail(mostiour, temperature, humidity, tim2):
    email_sender = "ayan.sakib.sp0@gmail.com"
    email_password = "hsflopunfqhdudsn"
    email_recipient = "cybercontect@skiff.com"

    subject = "Project AgriFlow Sensor Data."
    body = f"{humidity}\n{temperature}\n{mostiour}\n \nThe Time is: {tim2}"

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_recipient
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_recipient, em.as_string())
        print("Mail sent successfully")


def sendmail_cyber24(mostiour, temperature, humidity, tim2, tim3, rain,pressure_value):
    smtp_server = 'sapphire.premium.hostns.io'
    smtp_port = 465
    smtp_username = 'agriflow@cyber24bd.com'
    smtp_password = '^&~%7!4,YpPv'

    sender_email = 'agriflow@cyber24bd.com'
    receiver_email = 'cybercontect@skiff.com'
    subject = 'Project AgriFlow Without Gmail Sensor Data.'

    body = f"Humidity : {humidity}\nTemperature: {temperature}\nMoisture : {mostiour}\n Pressure: {pressure_value}\nRain: {rain} \nThe Date is: {tim2}\nThe Time is : {tim3}"

    em2 = EmailMessage()
    em2['From'] = sender_email
    em2['To'] = receiver_email
    em2['Subject'] = subject
    em2.set_content(body)

    context = ssl.create_default_context()

    print("Connecting to SMTP server...")
    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as smtp2:
        print("Logging in...")
        smtp2.login(smtp_username, smtp_password)
        print("Sending email...")
        smtp2.sendmail(sender_email, receiver_email, em2.as_string())
        print("Mail sent successfully")
