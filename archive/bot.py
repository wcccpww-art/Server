from telethon import TelegramClient, events
import asyncio
import os

BOT_TOKEN = '7538739924:AAF01dsSM-Ti0k4qksAdAvcd7yTZepqcHns'
DOWNLOAD_DIR = 'downloads'

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

client = TelegramClient('bot_session', api_id='22968934', api_hash='f6ced4df37e7dd07237d8ecf40cfa424').start(bot_token=BOT_TOKEN)

@client.on(events.NewMessage)
async def handler(event):
    if event.message.file:
        filename = event.message.file.name or f"file_{event.message.id}"
        path = os.path.join(DOWNLOAD_DIR, filename)
        await event.message.download_media(path)
        await event.reply(f"Файл скачан: {filename}")
        
        # Если это ZIP, импортировать
        if filename.endswith('.zip'):
            import subprocess
            result = subprocess.run(['tg-archive', '--import-zip', path], capture_output=True, text=True)
            if result.returncode == 0:
                await event.reply("Данные импортированы в архив.")
                # Пересобрать сайт
                subprocess.run(['tg-archive', '--build'], capture_output=True)
            else:
                await event.reply("Ошибка импорта.")
        
        # Удалить файл после обработки
        os.remove(path)
        await event.reply(f"Файл {filename} удален после обработки.")

print("Бот запущен. Отправьте файлы в чат с ботом.")
client.run_until_disconnected()