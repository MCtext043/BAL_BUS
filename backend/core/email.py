"""
Функции для отправки email
"""
import logging
from typing import Dict, Any
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import aiosmtplib

from backend.core.config import settings

logger = logging.getLogger(__name__)


async def send_ticket_email(email: str, ticket_data: Dict[str, Any]) -> bool:
    """
    Отправка email с билетом
    """
    try:
        # Если SMTP не включен, используем муляж
        if not settings.SMTP_ENABLED or not settings.SMTP_USER or not settings.SMTP_PASSWORD:
            logger.info(f"📧 [МУЛЯЖ] Отправка билета на email: {email}")
            logger.info(f"📧 [МУЛЯЖ] Данные билета:")
            logger.info(f"   - Номер билета: {ticket_data.get('ticket_number')}")
            logger.info(f"   - ФИО: {ticket_data.get('full_name')}")
            logger.info(f"   - Рейс: {ticket_data.get('trip_origin')} → {ticket_data.get('trip_destination')}")
            logger.info(f"   - Отправление: {ticket_data.get('departure_time')}")
            logger.info(f"   - Прибытие: {ticket_data.get('arrival_time')}")
            logger.info(f"   - Цена: {ticket_data.get('price')} ₽")
            return True
        
        # Реальная отправка через SMTP
        message = MIMEMultipart("alternative")
        message["Subject"] = f"Билет на рейс {ticket_data.get('trip_origin')} → {ticket_data.get('trip_destination')}"
        message["From"] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_USER}>"
        message["To"] = email
        
        # HTML версия письма
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px; }}
                .ticket-info {{ background: white; padding: 20px; margin: 20px 0; border-radius: 8px; border-left: 4px solid #667eea; }}
                .ticket-number {{ font-size: 24px; font-weight: bold; color: #667eea; text-align: center; margin: 20px 0; }}
                .info-row {{ margin: 10px 0; padding: 10px; background: #f8f9fa; border-radius: 5px; }}
                .info-label {{ font-weight: bold; color: #666; }}
                .price {{ font-size: 20px; color: #198754; font-weight: bold; text-align: center; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎫 {settings.SMTP_FROM_NAME}</h1>
                    <p>Ваш билет на автобусный рейс</p>
                </div>
                <div class="content">
                    <div class="ticket-number">
                        Номер билета: {ticket_data.get('ticket_number')}
                    </div>
                    
                    <div class="ticket-info">
                        <div class="info-row">
                            <span class="info-label">Пассажир:</span> {ticket_data.get('full_name')}
                        </div>
                        <div class="info-row">
                            <span class="info-label">Маршрут:</span> {ticket_data.get('trip_origin')} → {ticket_data.get('trip_destination')}
                        </div>
                        <div class="info-row">
                            <span class="info-label">Отправление:</span> {ticket_data.get('departure_time')}
                        </div>
                        <div class="info-row">
                            <span class="info-label">Прибытие:</span> {ticket_data.get('arrival_time')}
                        </div>
                    </div>
                    
                    <div class="price">
                        Цена: {ticket_data.get('price')} ₽
                    </div>
                    
                    <div class="footer">
                        <p>Спасибо за использование BAL_BUS!</p>
                        <p>Приятной поездки! 🚌</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Текстовая версия письма (для клиентов без поддержки HTML)
        text_content = f"""
Билет на автобусный рейс

Номер билета: {ticket_data.get('ticket_number')}

Пассажир: {ticket_data.get('full_name')}
Маршрут: {ticket_data.get('trip_origin')} → {ticket_data.get('trip_destination')}
Отправление: {ticket_data.get('departure_time')}
Прибытие: {ticket_data.get('arrival_time')}
Цена: {ticket_data.get('price')} ₽

Спасибо за использование {settings.SMTP_FROM_NAME}!
Приятной поездки!
        """
        
        # Добавляем обе версии в письмо
        text_part = MIMEText(text_content, "plain", "utf-8")
        html_part = MIMEText(html_content, "html", "utf-8")
        
        message.attach(text_part)
        message.attach(html_part)
        
        # Отправка через SMTP
        # Используем более надежный подход с явным созданием клиента
        if settings.SMTP_PORT == 587 or (settings.SMTP_USE_TLS and settings.SMTP_PORT != 465):
            # Порт 587 использует STARTTLS (TLS)
            async with aiosmtplib.SMTP(
                hostname=settings.SMTP_HOST,
                port=settings.SMTP_PORT,
                use_tls=False,
                start_tls=True,
                timeout=30
            ) as smtp:
                await smtp.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                await smtp.send_message(message)
        elif settings.SMTP_PORT == 465:
            # Порт 465 использует SSL
            import ssl
            ssl_context = ssl.create_default_context()
            async with aiosmtplib.SMTP(
                hostname=settings.SMTP_HOST,
                port=settings.SMTP_PORT,
                use_tls=True,
                tls_context=ssl_context,
                timeout=30
            ) as smtp:
                await smtp.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                await smtp.send_message(message)
        else:
            # Без шифрования (не рекомендуется)
            async with aiosmtplib.SMTP(
                hostname=settings.SMTP_HOST,
                port=settings.SMTP_PORT,
                use_tls=False,
                timeout=30
            ) as smtp:
                await smtp.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                await smtp.send_message(message)
        
        logger.info(f"✅ Email успешно отправлен на {email} (билет: {ticket_data.get('ticket_number')})")
        return True
        
    except Exception as e:
        logger.error(f"❌ Ошибка отправки email на {email}: {str(e)}", exc_info=True)
        return False
