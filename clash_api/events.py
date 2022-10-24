from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config.prefs import CHAT_ID, CLAN_TAG, coc_client, bot, dp
from db import DL


async def register_markup():
    player_markup = InlineKeyboardMarkup(row_width=2)
    clan = await coc_client.get_clan(CLAN_TAG)
    DL.create_table()
    for member in clan.members:
        if not DL.exists_by_clash_tag(member.tag):
            player_markup.insert(InlineKeyboardButton(text=f"{member.name}({member.tag})",
                                                      callback_data=f"user{member.tag}"))
    player_markup.add(InlineKeyboardButton(text="Отмена❌", callback_data="btn_del"))
    return player_markup


@dp.callback_query_handler(text_contains='user')
async def register_by_tag(callback_query: types.CallbackQuery):
    message_to_remove_id = callback_query.message.message_id
    await bot.delete_message(CHAT_ID, message_to_remove_id)
    tag = callback_query.data[callback_query.data.find("user") + 4:]
    player = await coc_client.get_player(tag)
    nickname = player.name
    tg_id = callback_query.from_user.id
    user_first_name = callback_query.from_user.first_name
    if DL.insert(tg_id, tag):
        await bot.send_message(CHAT_ID, user_first_name + ' зарегистрировался как ' + nickname)
    else:
        await bot.send_message(CHAT_ID, f"{nickname} уже зарегестрирован!")


@dp.callback_query_handler(text_contains="btn_del")
async def remove_msg_by_id(callback_query: types.CallbackQuery):
    id_to_remove = callback_query.message.message_id
    await bot.delete_message(callback_query.message.chat.id, id_to_remove)


