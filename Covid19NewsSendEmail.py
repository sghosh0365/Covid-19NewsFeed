import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import datetime

def send_email():
    li = [{'name': "Test", 'email': "test@email.com", 'location':'Test'}]  ## Specify the list of user name, email and the local news location of the recipients as a list of dicts
    currentTime = datetime.datetime.now()
    currentTime.hour
    if currentTime.hour < 12:
        greeting = 'Good morning!'
    elif 12 <= currentTime.hour < 18:
        greeting = 'Good afternoon!'
    else:
        greeting = 'Good evening!'
    for dest in li:
        fromaddr = "test@email.com" ## Sender address
        location = dest['location']
        # instance of MIMEMultipart
        msg = MIMEMultipart()

        # storing the senders email address
        msg['From'] = 'Covid-19 News'

        # storing the subject
        msg['Subject'] = "Daily COVID-19 newsletter from Snehasis"

        # string to store the body of the mail
        # body = f"Hello {reader}, \n\n{greeting}\nAttached is your daily newsletter. Happy reading!\nStay healthy and safe :)\n\nRegards,\nSG"

        # attach the body with the msg instance
        # msg.attach(MIMEText(body, 'plain'))

        # open the file to be sent
        filename = "COVID-19NewsLetter.pdf"
        attachment = open(f"C:\\Users\\TSG\\PycharmProjects\\NewsFeed\\venv\\COVID-19NewsLetter_{location}.pdf", "rb") ## Specify the path of the pdf

        # instance of MIMEBase and named as p
        p = MIMEBase('application', 'octet-stream')

        # To change the payload into encoded form
        p.set_payload((attachment).read())

        # encode into base64
        encoders.encode_base64(p)

        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

        # attach the instance 'p' to instance 'msg'
        msg.attach(p)

        # sending the mail

        # storing the receivers email address
        reader = dest['name']
        to_email = dest['email']
        msg['To'] = to_email
        body = f"Hello {reader}, \n\n{greeting}\nAttached is your daily newsletter. Happy reading!\nStay healthy and safe :)\n\nRegards,\nSG"
        msg.attach(MIMEText(body, 'plain'))
        text = msg.as_string()
        # creates SMTP session
        s = smtplib.SMTP('smtp.gmail.com', 587)
        # start TLS for security
        s.starttls()
        # s.starttls()
        s.login("Test", "<password>") ## Provide login credentials of the sender email
        s.sendmail(fromaddr, to_email, text)
        s.quit()
    print('Completed execution of Covid-19NewsSendEmail.py')
