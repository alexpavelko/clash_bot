import ast
import re

import coc
from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils import executor
from clash_api.clash_clan import *
from clash_api.events import register_markup
from config.resources.constants import kb_menu, panic_message
from config.prefs import CHAT_ID, CLAN_TAG, coc_client, dp, bot, telethon_client
from db import DL


# @client.on(NewMessage(chats=('Dark Elite', CHAT_ID)))
# async def pin_mafia_msg(event):
#     await telegram_chat.pin_mafia_msg(event)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.chat.id != CHAT_ID:
        await message.reply(text="Этот бот предназначен только одного чата. Вы не можете его использовать.",
                            reply_markup=ReplyKeyboardRemove())
    else:
        await message.reply(text="Выбери действие", reply_markup=kb_menu)


@dp.message_handler()
async def answer_menu(message: types.Message):
    is_registered = DL.exists_by_tg_id(message.from_user.id)
    if message.text == "📝":
        await message.reply("Кто ты в игре?", reply_markup=await register_markup())
    elif message.text == "👨‍💼":
        if is_registered:
            message_id = (await message.reply(text="Загрузка...")).message_id
            message_text = await get_roles()
            await bot.edit_message_text(chat_id=CHAT_ID, text=message_text, message_id=message_id,
                                        parse_mode="Markdown")
        else:
            await message.reply(text=panic_message)
    elif message.text == "👑":
        if is_registered:
            message_id = (await message.reply(text="Загрузка...")).message_id
            message_text = await get_rating_list()
            await bot.edit_message_text(chat_id=CHAT_ID, text=message_text, message_id=message_id)
        else:
            await message.reply(text=panic_message)
    elif message.text == "⚔":
        if is_registered:
            message_id = (await message.reply(text="Загрузка...")).message_id
            message_text = await get_shields()
            await bot.edit_message_text(chat_id=CHAT_ID, text=message_text, message_id=message_id)
        else:
            await message.reply(text=panic_message)


@coc_client.event
@coc.ClanEvents.member_join(tags=[CLAN_TAG])
async def on_clan_member_join(member, clan):
    await bot.send_message(CHAT_ID, f" {member.name} вступил в клан")
    player = await coc_client.get_player(member.tag)
    result = get_hero_percent(player)
    await bot.send_message(CHAT_ID, f"Прокачка героев игрока для его тх({player.town_hall}) = {int(result)}%")


@coc_client.event
@coc.ClanEvents.member_leave(tags=[CLAN_TAG])
async def on_clan_member_leave(member, clan):
    await bot.send_message(CHAT_ID, f"{member.name} покинул клан")


if __name__ == '__main__':
    executor.start_polling(dp)
