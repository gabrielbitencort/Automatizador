import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# Configurações SMTP
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = 'gabrielbiten.henrique@gmail.com'
smtp_password = 'zsbr anlf uiab hvgh'

# Arquivo de lista de destinatários
arquivo_contatos = 'contacts2.txt'

# Assunto do e-mail
assunto = 'Testando imagem no email'

# Caminho para o arquivo HTML
corpo_html = 'message.html'

# Caminho para a imagem
imagem_path = 'Images/ottosistemas.png'

# Ler a lista de contatos do arquivo externo
with open("contacts2.txt", 'r') as arquivo:
    lista_de_contatos = [linha.split() for linha in arquivo]

# Loop através da lista de contatos e envio de e-mails
for destinatario in lista_de_contatos:
    mensagem = MIMEMultipart()
    mensagem['From'] = smtp_username
    mensagem['To'] = destinatario
    mensagem['Subject'] = assunto

    with open("message.html", 'r', encoding='utf-8') as arquivo_html:
        corpo_email = arquivo_html.read()

    corpo_email = MIMEText(corpo_email, 'html')
    mensagem.attach(corpo_email)

    with open("C:/Users/Win10/Documents/Automatizador/Images/ottosistemas.png", 'rb') as arquivo_imagem:
        imagem_anexa = MIMEImage(arquivo_imagem.read())
        imagem_anexa.add_header('Content-ID', '<imagem>')
        mensagem.attach(imagem_anexa)

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)
    server.send_message(mensagem)
    server.quit()
