import asyncio
import logging
import os
import sys
from dotenv import load_dotenv
from urllib.parse import urlparse

from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram.exceptions import TelegramAPIError

from aiohttp import web
from routes.transactions import fin_router

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')  # Должен быть полным URL, включая https://
WEBHOOK_PATH = "/webhook"  # Путь для обработки вебхуков

# Определение порта - используем PORT из окружения или 8080 по умолчанию
PORT = int(os.getenv('PORT', 8080))

# Проверка и валидация URL
def validate_webhook_url(url):
    if not url:
        return False
    
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        return False
    
    return True

# Проверка наличия обязательных переменных окружения
if not BOT_TOKEN:
    logger.error("BOT_TOKEN не найден в переменных окружения!")
    exit(1)

if not validate_webhook_url(WEBHOOK_URL):
    logger.error(f"Невалидный WEBHOOK_URL: {WEBHOOK_URL}. URL должен быть полным (https://example.com)")
    exit(1)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Регистрация роутеров
dp.include_router(fin_router)

# Создание приложения
app = web.Application()

# Обработчик для корневого маршрута
async def handle_root(request):
    """Обработчик для корневого маршрута - предотвращает 404 ошибки"""
    return web.Response(text="Бот работает. Маршрут webhook доступен.", status=200)

# Обработчик для проверки состояния сервиса
async def handle_health(request):
    """Обработчик для проверки состояния сервиса"""
    return web.json_response({"status": "ok", "message": "Service is running"})

# Настройка вебхука
async def on_startup(app):
    """Выполняется при запуске приложения"""
    webhook_url = f"{WEBHOOK_URL.rstrip('/')}{WEBHOOK_PATH}"
    logger.info(f"Устанавливаем вебхук: {webhook_url}")
    
    try:
        await bot.delete_webhook()  # Сначала удаляем старый вебхук
        await bot.set_webhook(url=webhook_url)
        logger.info("Вебхук успешно установлен")
    except TelegramAPIError as e:
        logger.error(f"Ошибка установки вебхука: {e}")

# Запуск ping-задачи для предотвращения "засыпания"
async def keep_alive():
    """Задача для предотвращения "засыпания" сервиса на бесплатных планах"""
    while True:
        logger.debug("Поддержание активности сервиса...")
        await asyncio.sleep(300)  # Пинг каждые 5 минут

# Отмена вебхука при выключении
async def on_shutdown(app):
    """Выполняется при остановке приложения"""
    logger.info("Удаляем вебхук")
    try:
        await bot.delete_webhook()
        logger.info("Вебхук удален")
    except TelegramAPIError as e:
        logger.error(f"Ошибка удаления вебхука: {e}")
    
    # Закрываем сессии
    await bot.session.close()

# Регистрация хуков запуска и остановки
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

# Настройка обработчика вебхуков
webhook_handler = SimpleRequestHandler(
    dispatcher=dp,
    bot=bot,
)

# Добавление маршрутов
app.router.add_get('/', handle_root)
app.router.add_get('/health', handle_health)

# Настройка маршрутов для вебхука
webhook_handler.register(app, path=WEBHOOK_PATH)

# Настройка интеграции с aiogram
setup_application(app, dp, bot=bot)

if __name__ == '__main__':
    # Запуск задачи для поддержания активности
    asyncio.ensure_future(keep_alive())
    
    logger.info(f"Запуск приложения на порту {PORT}")
    logger.info(f"Webhook URL: {WEBHOOK_URL}")
    
    # Запуск веб-сервера
    web.run_app(app, host="0.0.0.0", port=PORT)