import os
import time

from phonenumbers import PhoneNumber
from telethon import TelegramClient
from telethon.tl.functions.messages import AddChatUserRequest
from telethon.tl.types import InputPhoneContact
from telethon.tl.functions.contacts import ImportContactsRequest
from telethon import functions, types
import asyncio
import phonenumbers
from queue import Queue
import threading

lock = threading.Lock()
global q
q = Queue()

phone_number = '+84706201293'
api_id = 14537933

api_hash = 'ee3a2dc9e9bfd679d9f0b8d6b6600904'


async def main():
    sessions = os.listdir('sessions')
    print(sessions)
    async with TelegramClient(sessions[2], api_id, api_hash) as client:
        await client.start()
        print(client.is_connected())
        numberOk = 0
        with open('phones.txt') as f:
            phones = f.readlines()
            for phone in phones:
                time.sleep(5)
                if await check_phone(client, convert_phone_number(phone)):
                    print(phone)
                    numberOk += 1
    print(numberOk)


async def check_phone(client, phone):
    try:
        contact = InputPhoneContact(client_id=0, phone=phone, first_name=phone, last_name="")
        result = await client(ImportContactsRequest([contact]))
        return len(result.users) > 0
    except Exception as e:
        print(e)


def convert_phone_number(number):
    phone_number_format = phonenumbers.parse(number, "VN")
    phone = phonenumbers.format_number(phone_number_format, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    return phone


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
