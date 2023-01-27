import os
import asyncio
from presets import Presets
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from library.support import users_info
from library.sql import add_user, query_msg


if bool(os.environ.get("ENV", False)):
    from sample_config import Config
else:
    from config import Config

# ------------------------------- View Subscribers --------------------------------- #
@Client.on_message(filters.private & filters.command('stats'))
async def stats_count(bot, m: Message):
    id = m.from_user.id
    if id not in Config.AUTH_USERS:
        return
    msg = await m.reply_text(Presets.WAIT_MSG)
    messages = await users_info(bot)
    active = messages[0]
    blocked = messages[1]

    await msg.edit(Presets.USERS_LIST.format(active, blocked))


# ------------------------ Send messages to subs ----------------------------- #
@Client.on_message(filters.private & filters.command('broadcast'))
async def broadcast_text(bot, m: Message):
    id = m.from_user.id
    if id not in Config.AUTH_USERS:
        return
    if (" " not in m.text) and ("broadcast" in m.text) and (m.reply_to_message is not None):
        query = await query_msg()
        for row in query:
            chat_id = int(row[0])
            try:
                await bot.copy_message(
                    chat_id=chat_id,
                    from_chat_id=m.chat.id,
                    message_id=m.reply_to_message.message_id,
                    caption=m.reply_to_message.caption,
                    reply_markup=m.reply_to_message.reply_markup
                )
    try:
        await query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(btn)
        )
            except FloodWait as e:
                await asyncio.sleep(e.x)
            except Exception:
                pass
    else:
        msg = await m.reply_text(Presets.REPLY_ERROR, m.message_id)
        await asyncio.sleep(8)

