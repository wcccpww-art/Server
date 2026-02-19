from telethon import TelegramClient
import asyncio

api_id = '22968934'
api_hash = 'f6ced4df37e7dd07237d8ecf40cfa424'
session_file = 'session.session'

async def main():
    client = TelegramClient(session_file, api_id, api_hash)
    await client.start()
    print("Session created successfully!")
    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())