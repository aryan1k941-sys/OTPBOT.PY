"""
Telegram Number Checker Bot
Install:  pip install telethon
Setup:
  1. https://my.telegram.org -> API development tools -> api_id & api_hash lo
  2. https://t.me/BotFather se bot token lo
  3. Neeche 4 values bhar do, phir: python tg_checker_bot.py
"""
import re
import asyncio
from telethon import TelegramClient, events
from telethon.tl.functions.contacts import ImportContactsRequest, DeleteContactsRequest
from telethon.tl.types import InputPhoneContact

API_ID = 39776296              # my.telegram.org se
API_HASH = "39750d30671418c6fd01a96b6296ee82"   # my.telegram.org se
BOT_TOKEN = "8584121938:AAFrsbNREiJosuLVEXvvClJwGUticuCyhUQ" # BotFather se

# user account (lookup ke liye) + bot (chat ke liye)
user = TelegramClient("checker_user", API_ID, API_HASH)
bot = TelegramClient("checker_bot", API_ID, API_HASH)


async def check_number(phone: str) -> str:
    contact = InputPhoneContact(client_id=0, phone=phone, first_name="chk", last_name="")
    result = await user(ImportContactsRequest([contact]))
    if result.users:
        u = result.users[0]
        await user(DeleteContactsRequest(id=[u.id]))  # contact list saaf
        name = f"{u.first_name or ''} {u.last_name or ''}".strip()
        uname = f"@{u.username}" if u.username else "no username"
        return f"✅ REGISTERED\nName: {name or '-'}\nUsername: {uname}\nID: {u.id}"
    return "❌ NOT REGISTERED (fresh number ya privacy se hidden)"


@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    await event.reply("Number bhejo country code ke saath.\nExample: +919876543210\nEk saath kai numbers bhi bhej sakte ho (har line me ek).")


@bot.on(events.NewMessage)
async def handler(event):
    if event.raw_text.startswith("/"):
        return
    numbers = re.findall(r"\+?\d{8,15}", event.raw_text)
    if not numbers:
        await event.reply("Sahi number bhejo, jaise +919876543210")
        return
    for n in numbers[:20]:  # limit, warna flood-ban ho sakta hai
        n = n if n.startswith("+") else "+" + n
        try:
            res = await check_number(n)
        except Exception as e:
            res = f"⚠️ Error: {e}"
        await event.reply(f"📞 {n}\n{res}")
        await asyncio.sleep(3)  # delay zaroori hai


async def main():
    await user.start()                     # pehli baar phone + OTP maangega
    await bot.start(bot_token=BOT_TOKEN)
    print("Bot chal raha hai...")
    await bot.run_until_disconnected()

asyncio.run(main())
