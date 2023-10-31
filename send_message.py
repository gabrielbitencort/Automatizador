# Import necessary packages
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# from email.mime.image import MIMEImage

# SMTP Server configs and credential
smtp_server = 'smtp.gmail.com'
smtp_port = 587
username = 'gabrielbiten.henrique@gmail.com'
password = 'zsbr anlf uiab hvgh'

# Ler a lista de contatos do arquivo externo
with open("Contacts/contacts2.txt", 'r') as archive:
    contacts_list = [line.split() for line in archive]

try:
    for recipients in contacts_list:
        # Create MIMEMultipart object for email
        msg = MIMEMultipart("alternative")
        msg['From'] = username
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = 'Teste Automatizador de Emails'

        # Attach html_file to email body
        with open('message.html', 'r', encoding='utf-8') as html_file:
            email_body = MIMEText(html_file.read(), 'html', 'utf-8')
        msg.attach(email_body)

        # Initialize SMTP connection
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(username, password)

        # Send email for recipients
        server.sendmail(username, recipients, msg.as_string())
        server.quit()
        print("Email enviado.")
except Exception as e:
    print(f"Erro ao enviar email: {str(e)}")