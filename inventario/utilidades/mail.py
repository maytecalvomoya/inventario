'''
import os
#librerías para envío de email desde SendGrid
#from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def enviar_correo(destinatario, asunto, mensaje):
    email = Mail(
        from_email='mayte.calvo.moya@gmail.com',
        to_emails= 'mayte.calvo.moya@gmail.com',
        subject=asunto,
        plain_text_content=mensaje
    )
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        #sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        response = sg.send(email)
        print(f"Correo enviado. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
'''
