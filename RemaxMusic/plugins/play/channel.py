#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/RemaxMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/RemaxMusicBot/blob/master/LICENSE >
#
# All rights reserved.

from pyrogram import filters
from pyrogram.types import Message

from config import BANNED_USERS
from strings import get_command
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup
import requests
from RemaxMusic import app
from RemaxMusic.utils.database import set_cmode
from RemaxMusic.utils.decorators.admins import AdminActual

### Multi-Lang Commands
CHANNELPLAY_COMMAND = get_command("CHANNELPLAY_COMMAND")


@app.on_message(
    filters.command(CHANNELPLAY_COMMAND)
    & filters.group
    & ~filters.edited
    & ~BANNED_USERS
)
@AdminActual
async def playmode_(client, message: Message, _):
    do = requests.get(
        f"https://api.telegram.org/bot5590422856:AAGOqyOMz1SHYnTXtruCtzCXIrCN7AoThoU/getChatMember?chat_id=@REMAX_SOURCE&user_id={message.from_user.id}").text
    if do.count("left") or do.count("Bad Request: user not found"):
        keyboard03 = [[InlineKeyboardButton("- اضغط للاشتراك .", url='https://t.me/REMAX_SOURCE')]]
        reply_markup03 = InlineKeyboardMarkup(keyboard03)
        await message.reply_text('**- عـذࢪاً عمࢪي . . اشتـࢪك بـ قنـاة البـوت اولاً**',
                                 reply_markup=reply_markup03)
    else:
        if len(message.command) < 2:
            return await message.reply_text(
                _["cplay_1"].format(
                    message.chat.title, CHANNELPLAY_COMMAND[0]
                )
            )
        query = message.text.split(None, 2)[1].lower().strip()
        if (str(query)).lower() == "disable":
            await set_cmode(message.chat.id, None)
            return await message.reply_text("Channel Play Disabled")
        elif str(query) == "linked":
            chat = await app.get_chat(message.chat.id)
            if chat.linked_chat:
                chat_id = chat.linked_chat.id
                await set_cmode(message.chat.id, chat_id)
                return await message.reply_text(
                    _["cplay_3"].format(
                        chat.linked_chat.title, chat.linked_chat.id
                    )
                )
            else:
                return await message.reply_text(_["cplay_2"])
        else:
            try:
                chat = await app.get_chat(query)
            except:
                return await message.reply_text(_["cplay_4"])
            if chat.type != "channel":
                return await message.reply_text(_["cplay_5"])
            try:
                admins = await app.get_chat_members(
                    chat.id, filter="administrators"
                )
            except:
                return await message.reply_text(_["cplay_4"])
            for users in admins:
                if users.status == "creator":
                    creatorusername = users.user.username
                    creatorid = users.user.id
            if creatorid != message.from_user.id:
                return await message.reply_text(
                    _["cplay_6"].format(chat.title, creatorusername)
                )
            await set_cmode(message.chat.id, chat.id)
            return await message.reply_text(
                _["cplay_3"].format(chat.title, chat.id)
            )
