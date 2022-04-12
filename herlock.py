import re
import os
from asyncio import gather, get_event_loop, sleep

from aiohttp import ClientSession
from pyrogram import Client, filters, idle
from Python_ARQ import ARQ

is_config = os.path.exists("config.py")

if is_config:
    from config import *
else:
    from sample_config import *

luna = Client(
    ":memory:",
    bot_token=bot_token,
    api_id=6,
    api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e",
)

bot_id = int(bot_token.split(":")[0])
arq = None


async def herlockQuery(query: str, user_id: int):
    query = (
        query
        if LANGUAGE == "tr"
        else (await arq.translate(query, "tr")).result.translatedText
    )
    resp = (await arq.herlock(query, user_id)).result
    return (
        resp
        if LANGUAGE == "tr"
        else (
            await arq.translate(resp, LANGUAGE)
        ).result.translatedText
    )


async def type_and_send(message):
    chat_id = message.chat.id
    user_id = message.from_user.id if message.from_user else 0
    query = message.text.strip()
    await message._client.send_chat_action(chat_id, "typing")
    response, _ = await gather(herlockQuery(query, user_id), sleep(2))
    await message.reply_text(response)
    await message._client.send_chat_action(chat_id, "cancel")


@herlock.on_message(filters.command("repo") & ~filters.edited)
async def repo(_, message):
    await message.reply_text(
        "[GitHub](https://instagram.com/developer.rat)"
        + " | [Grub](t.me/isyancilarvip)",
        disable_web_page_preview=True,
    )


@herlock.on_message(filters.command("help") & ~filters.edited)
async def start(_, message):
    await herlock.send_chat_action(message.chat.id, "typing")
    await sleep(2)
    await message.reply_text("Noldu Yardıma mı ihtiyacın var ü")


@herlock.on_message(filters.command("start") & ~filters.edited)
async def start(_, message):
    await herlock.send_chat_action(message.chat.id, "typing")
    await sleep(2)
    await message.reply_text("**Merhaba** [Dostum](tg://settings) Ben @SakirBey1 Tarafından Oluşturulan ChatBotum \n/komuts")


@herlock.on_message(filters.command("komuts") & ~filters.edited)
async def start(_, message):
    await herlock.send_chat_action(message.chat.id, "typing")
    await sleep(2)
    await message.reply_text("**HerusChatBot Komuts Bölümü**\n=> /repo \n=> /help \n=>/developer \n => /herus")


@herlock.on_message(filters.command("developer") & ~filters.edited)
async def start(_, message):
    await herlock.send_chat_action(message.chat.id, "typing")
    await sleep(2)
    await message.reply_text("Sahibim Ve Geliştiricim @SakirBey1 ;)\n✨")


@herlock.on_message(filters.command("herus") & ~filters.edited)
async def start(_, message):
    await herlock.send_chat_action(message.chat.id, "typing")
    await sleep(2)
    await message.reply_text("**Merhaba Ben Herus** \n@SakirBey1 Tarafından Günden Güne Geliştirilen Ve En Eğlenceli Bir ChatBotum Sizde Bota Eklenmesi İstediğiniz Özellikleri Sahibime Yazarak İlete Bilirsiniz Ayrıca Sahibim Benden Başka Bi Sürü Grub Botları Geliştiriyor @SakirBey2 Kanalına Bir Göz Atın Derim ;) \nSakirBey")


@herlock.on_message(
    ~filters.private
    & filters.text
    & ~filters.command("help")
    & ~filters.edited,
    group=69,
)
async def chat(_, message):
    if message.reply_to_message:
        if not message.reply_to_message.from_user:
            return
        from_user_id = message.reply_to_message.from_user.id
        if from_user_id != bot_id:
            return
    else:
        match = re.search(
            "[.|\n]{0,}herlock[.|\n]{0,}",
            message.text.strip(),
            flags=re.IGNORECASE,
        )
        if not match:
            return
    await type_and_send(message)


@herlock.on_message(
    filters.private & ~filters.command("help") & ~filters.edited
)
async def chatpm(_, message):
    if not message.text:
        return
    await type_and_send(message)


async def main():
    global arq
    session = ClientSession()
    arq = ARQ(ARQ_API_BASE_URL, ARQ_API_KEY, session)

    await herlock.start()
    print(
        """
-------------------
| Herlock Başladı |
-------------------
"""
    )
    await idle()


loop = get_event_loop()
loop.run_until_complete(main())
