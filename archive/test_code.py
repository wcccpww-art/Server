from telethon import TelegramClient
import asyncio

api_id = '22968934'
api_hash = 'f6ced4df37e7dd07237d8ecf40cfa424'
session_file = 'session.session'

async def main():
    phone = input("Enter phone number: ")
    client = TelegramClient(session_file, api_id, api_hash)
    try:
        await client.connect()
        result = await client.send_code_request(phone)
        print("Code sent! Phone code hash:", result.phone_code_hash)
        code = input("Enter the code: ")
        await client.sign_in(phone, code)
        print("Session created successfully!")
    except Exception as e:
        print("Error:", e)
    finally:
        await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())