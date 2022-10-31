import smtplib
import ssl
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart  # New line
from email.mime.application import MIMEApplication

from email.mime.base import MIMEBase  # New line
from email import encoders  # New line
from . import views
from WebGuard import settings


def gmailfornewtrusted(sitename, request):
    subject = "Web Guard's update on " + sitename
    # User configuration
    sender_email = settings.EMAIL_HOST_USER
    sender_name = 'Web Guard'
    # password = input('Please, type your password:n')
    password = settings.EMAIL_HOST_PASSWORD
    EMAIL_HOST = settings.EMAIL_HOST

    path = views.GetCodeDirectory(request)

    with open(path + "emailalert.txt") as file:
        file_data = file.readlines()
        file.close()
    # print(file_data)
    b = []
    for i in file_data:
        a = i.split("\n")[0]
        b.append(a)
    print(b)

    for receiver_emails in b:
        # print(receiver_emails)
        receiver_emails = [receiver_emails]  # ["ehsan.ncsael@mcs.edu.pk"]
        receiver_names = [""]

        # Email body
        email_body1 = "A new copy of your Website " + sitename + " is saved by webguard."
        # email_html = open('/home/jzm/Desktop/OfficeWorkFromH/FullProject/UI/app/home/email.html')
        # email_body = email_html.read()

        # filename = 'cat.gif'
        for receiver_email, receiver_name in zip(receiver_emails, receiver_names):
            print("Sending the email...")
            # Configurating user's info
            msg = MIMEMultipart()
            msg['To'] = formataddr((receiver_name, receiver_email))
            msg['From'] = formataddr((sender_name, sender_email))
            msg['Subject'] = subject

            # path_to_pdf = "/home/jzm/Desktop/OfficeWorkFromH/FullProject/UI/Report.pdf"
            # with open(path_to_pdf, "rb") as f:
            #     # attach = email.mime.application.MIMEApplication(f.read(),_subtype="pdf")
            #     file = MIMEApplication(f.read(), _subtype="pdf")

            email_body = """<html> <head></head> <body><div style= 
            "margin:0;padding:0;color:red;font-weight:1000;font-weight:700;font-size:20px"><p> 
            ATTENTION 
            </p></div></body></html> """

            msg.attach(MIMEText(email_body, 'html'))
            msg.attach(MIMEText(email_body1, 'plain'))

            # msg.attach(file)

            try:
                # Creating a SMTP session | use 587 with TLS, 465 SSL and 25
                server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
                # Encrypts the email
                context = ssl.create_default_context()
                server.starttls(context=context)
                # We log in into our Google account
                server.login(sender_email, password)
                # Sending email from sender, to receiver with the email body
                server.sendmail(sender_email, receiver_email, msg.as_string())
                print('Email sent!')
            except Exception as e:
                print(f'Oh no! Something bad happened!n{e}')
                break
            finally:
                print('Closing the server...')
                server.quit()


def gmail(sitename, pdfname, request):
    subject = "Website " + sitename + " excedded the thresh hold its look like that yourr website has been changed is it you? if its you then press yess " \
                                      "Otherwise no."
    subject = "Web Guard's Report on " + sitename
    # User configuration
    sender_email = 'eagleak169@gmail.com'
    sender_name = 'Web Guard'
    # password = input('Please, type your password:n')
    # password = 'Qwerty@123#'

    sender_email = "web@lynx-infosec.com"
    password = "]{)ZDe=%I*c4"

    path = views.GetCodeDirectory(request)

    with open(path + "emailalert.txt") as file:
        file_data = file.readlines()
        file.close()
    # print(file_data)
    b = []
    for i in file_data:
        a = i.split("\n")[0]
        b.append(a)
    print(b)

    for receiver_emails in b:
        # print(receiver_emails)
        receiver_emails = [receiver_emails]  # ["ehsan.ncsael@mcs.edu.pk"]
        receiver_names = ["Ehsan"]

        # Email body
        email_body1 = "Website " + sitename + " has been defaced."
        # email_html = open('/home/jzm/Desktop/OfficeWorkFromH/FullProject/UI/app/home/email.html')
        # email_body = email_html.read()

        # filename = 'cat.gif'
        for receiver_email, receiver_name in zip(receiver_emails, receiver_names):
            print("Sending the email...")
            # Configurating user's info
            msg = MIMEMultipart()
            msg['To'] = formataddr((receiver_name, receiver_email))
            msg['From'] = formataddr((sender_name, sender_email))
            msg['Subject'] = subject

            # path_to_pdf = "/home/jzm/Desktop/OfficeWorkFromH/FullProject/UI/Report.pdf"
            # with open(path_to_pdf, "rb") as f:
            #     # attach = email.mime.application.MIMEApplication(f.read(),_subtype="pdf")
            #     file = MIMEApplication(f.read(), _subtype="pdf")

            email_body = """<html> <head></head> <body><div style= 
            "margin:0;padding:0;color:red;font-weight:1000;font-weight:700;font-size:20px"><p> 
            WARNING 
            </p></div></body></html> """

            # pdfname = path + sitename +' Report.pdf'

            # open the file in bynary
            binary_pdf = open(pdfname, 'rb')

            payload = MIMEBase('application', 'octate-stream', Name="Report.pdf")
            # payload = MIMEBase('application', 'pdf', Name=pdfname)
            payload.set_payload((binary_pdf).read())

            # enconding the binary into base64
            encoders.encode_base64(payload)

            # add header with pdf name
            payload.add_header('Content-Decomposition', 'attachment', filename="Report.pdf")

            msg.attach(MIMEText(email_body, 'html'))
            msg.attach(MIMEText(email_body1, 'plain'))

            msg.attach(payload)

            # msg.attach(file)

            try:
                # Creating a SMTP session | use 587 with TLS, 465 SSL and 25
                context = ssl.create_default_context()
                server = smtplib.SMTP_SSL('mail.lynx-infosec.com', 465, context=context)

                # server = smtplib.SMTP('smtp.gmail.com', 587)
                # Encrypts the email
                # context = ssl.create_default_context()
                # server.starttls(context=context)
                # We log in into our Google account
                server.login(sender_email, password)
                # Sending email from sender, to receiver with the email body
                server.sendmail(sender_email, receiver_email, msg.as_string())
                print('Email sent!')
            except Exception as e:
                print(f'Oh no! Something bad happened!n{e}')
                break
            finally:
                print('Closing the server...')
                server.quit()

# gmail("ncsael.mcs.nust.edu.pk")
# gmailfornewtrusted("ncsael.mcs.nust.edu.pk")
