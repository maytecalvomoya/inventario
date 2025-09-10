import os
import django
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


# Establece la configuración del proyecto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'P_inventario.settings')
django.setup()

load_dotenv()  # busca el archivo .env en el directorio actual

#SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

message = Mail(
    from_email='mayte.calvo.moya@gmail.com',
    to_emails='mayte.calvo.moya@gmail.com',
    subject='Correo de prueba desde PythonAnywhere',
    plain_text_content='¡Hola Mayte! Este es un correo enviado con SendGrid sin dominio propio.'
)

try:
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print(f"Correo enviado. Status code: {response.status_code}")
except Exception as e:
    print(f"Error al enviar el correo: {e}")

