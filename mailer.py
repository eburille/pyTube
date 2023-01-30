import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import imaplib
import email
from email.header import decode_header
import os
from email import encoders
from email.mime.base import MIMEBase

senha = "******"
endereco_email = "**********"

def send_message(mensagem, assunto, e_mail):

    port = 587  # For SSL
    password = senha

    # Create a secure SSL context
    context = ssl.create_default_context()
    sender = endereco_email
    receiver = e_mail
    smtp_server = "smtp.outlook.com"

    txt = mensagem

    message = MIMEMultipart("alternative")
    message["Subject"] = assunto
    message["From"] = sender
    message["To"] = receiver
    
    message.attach(MIMEText(txt, 'plain'))
    
    context = ssl.create_default_context()
    
    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() # Can be omitted
        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        server.login(sender, password)
        # TODO: Send email here
        server.sendmail(sender, receiver, message.as_bytes())
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit() 

def numero_de_emails():
    # account credentials
    username = endereco_email
    password = senha
    # use your email provider's IMAP server, you can look for your provider's IMAP server on Google
    # or check this page: https://www.systoolsgroup.com/imap/
    # for office 365, it's this:
    imap_server = "imap-mail.outlook.com"

    # create an IMAP4 class with SSL 
    imap = imaplib.IMAP4_SSL(imap_server)
    # authenticate
    imap.login(username, password)

    status, messages = imap.select("INBOX")
    # number of top emails to fetch
    # total number of emails
    n_messages = int(messages[0])
    return  n_messages

def get_last_message():
    username = endereco_email
    password = senha
    # use your email provider's IMAP server, you can look for your provider's IMAP server on Google
    # or check this page: https://www.systoolsgroup.com/imap/
    # for office 365, it's this:
    imap_server = "imap-mail.outlook.com"

    def clean(text):
    # clean text for creating a folder
        return "".join(c if c.isalnum() else "_" for c in text)

    # create an IMAP4 class with SSL 
    imap = imaplib.IMAP4_SSL(imap_server)
    # authenticate
    imap.login(username, password)

    status, messages = imap.select("INBOX")
    # number of top emails to fetch
    N = 1
    # total number of emails
    messages = messages[0].split(b' ')

    for i in messages:
        # fetch the email message by ID
        res, msg = imap.fetch(i, "(RFC822)")

        for response in msg:
            if isinstance(response, tuple):
                # parse a bytes email into a message object
                msg = email.message_from_bytes(response[1])
                # decode the email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    # if it's a bytes, decode to str
                    subject = subject.decode(encoding)
                # decode email sender
                From, encoding = decode_header(msg.get("From"))[0]
                if isinstance(From, bytes):
                    From = From.decode(encoding)
                # if the email message is multipart
                if msg.is_multipart():

                    # iterate over email parts
                    for part in msg.walk():
                        # extract content type of email
                        content_type = part.get_content_type()

                        content_disposition = str(part.get("Content-Disposition"))

                        try:
                            # get the email body
                            body = part.get_payload(decode=True).decode()

                        except:
                            pass
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            body = part.get_payload(decode=True).decode('latin1')
                            imap.store(i, "+FLAGS", "\\Deleted")
                            imap.expunge()
                            imap.close()
                            imap.logout()
                            return From, body
                            # print text/plain emails and skip attachments

def send_video(nome_video, e_mail):

    port = 587  # For SSL
    password = senha

    # Create a secure SSL context
    context = ssl.create_default_context()
    sender = endereco_email
    receiver = e_mail
    smtp_server = "smtp.outlook.com"

  

    message = MIMEMultipart("alternative")
    message["Subject"] = "Video baixado"
    message["From"] = sender
    message["To"] = receiver

    video_file = MIMEBase('application', "octet-stream",)

    # Importing video file
    video_file.set_payload(open(nome_video, "rb").read())

    # Encoding video for attaching to the email
    encoders.encode_base64(video_file)

    # creating EmailMessage object

    
    message.attach(MIMEText("video enviado", 'plain'))
    message.attach(video_file)
    context = ssl.create_default_context()
    
    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() # Can be omitted
        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        server.login(sender, password)
        # TODO: Send email here
        server.sendmail(sender, receiver, message.as_bytes())
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit() 

                        
