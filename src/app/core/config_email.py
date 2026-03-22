from fastapi_mail import ConnectionConfig, FastMail

from app.core.config import settings

# se configura los datos necesarios para trabajar con fastapi_mail
mail_config = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=587,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER="src/app/template",
)


# se configura el objeto para permitir el uso de los métodos de envío de correo
mail = FastMail(config=mail_config)
