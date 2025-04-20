from telethon import TelegramClient, events
from telethon.tl.functions.messages import SendReactionRequest
from telethon.tl.types import ReactionEmoji
import asyncio
import os

# Bot sozlamalari (TOKEN, EMOJI)
bots = [
    {"name": "bot1", "7327051070:AAGxDXW1ozkgIp__ha6sm9ZMzHn-3QS_Jno": os.getenv("BOT_TOKEN_1"), "emoji": "❤️"},
    {"name": "bot2", "7753185283:AAFbgzOUwYRvaRHQPMX-auvPrMoeQlxQuF4": os.getenv("BOT_TOKEN_2"), "emoji": "💔"},
    {"name": "bot3", "7504024097:AAGItfdmjblZgTeAzHBg6j5G-M63o0i5F4s": os.getenv("BOT_TOKEN_3"), "emoji": "💯"},
    {"name": "bot4", "7717874523:AAGa_ZXd2jawu8WbQWjSPwhmsl6Hly7h25Y": os.getenv("BOT_TOKEN_4"), "emoji": "💋"},
    {"name": "bot5", "7724748741:AAG7ic1bmj6AGDznL2KflL9r2MB9eerUMJE": os.getenv("BOT_TOKEN_5"), "emoji": "❤‍🔥"},
    # Qo‘shimcha botlar kerak bo‘lsa shu yerga qo‘sh
]

# API ID va HASH
api_id = int(os.getenv("28782604"))
api_hash = os.getenv("e5a1c0ee714544244e25b2a9d3e06e69")
channel = os.getenv("rasulovshokh")  # Masalan: @my_channel

clients = []

# Har bir botni boshlash
for bot in bots:
    client = TelegramClient(bot["name"], api_id, api_hash).start(bot_token=bot["token"])
    clients.append((client, bot["emoji"]))

# Botlar eventga tayyor
async def main():
    @clients[0][0].on(events.NewMessage(chats=channel))
    async def handler(event):
        await asyncio.sleep(60)  # Postdan keyin 1 daqiqa kutadi
        for client, emoji in clients:
            try:
                await client(SendReactionRequest(
                    peer=event.chat_id,
                    msg_id=event.id,
                    reaction=[ReactionEmoji(emoticon=emoji)]
                ))
                print(f"{emoji} bosildi")
                await asyncio.sleep(2)  # Antiban uchun delay
            except Exception as e:
                print(f"Xatolik: {e}")

    await asyncio.gather(*[client.run_until_disconnected() for client, _ in clients])

# Ishga tushirish
asyncio.run(main())
