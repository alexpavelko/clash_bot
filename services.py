import aiogram.types
from aiogram import types
from aiogram.types import ReplyKeyboardRemove

from clash_api import clash_clan
from clash_api.clash_clan import check_war_state
from config.prefs import CHAT_ID, telethon_client, bot, coc_client
from config.resources.constants import panic_message, kb_menu
from db import DL


async def has_permissions(tg_id, role):
    if DL.exists_by_tg_id(tg_id):
        users = DL.get_by_tg_id(tg_id).fetchall()
        for user in users:
            tag = user[2]
            player = await coc_client.get_player(tag)
            if player.role.name.lower() == role:
                return True
    return False


async def delete_user(message: aiogram.types.Message):
    if message.chat.id != CHAT_ID:
        await message.reply(text="Этот бот предназначен только одного чата. Вы не можете его использовать.",
                            reply_markup=ReplyKeyboardRemove())
    else:
        has_permission = await has_permissions(message.from_user.id, "co_leader") or await has_permissions(
            message.from_user.id, "leader")
        if has_permission:
            tg_id = await parse_tg_id(message)
            if not DL.exists_by_tg_id(tg_id):
                message_text = f"В базе данных отсутствует информация про данного пользователя.\n"
                await message.reply(text=message_text, parse_mode="Markdown")
            else:
                DL.delete(tg_id).fetchall()
                user = await telethon_client.get_entity(int(tg_id))
                mention = f"[@{user.first_name if user.first_name != '' else user.username}](tg://user?id={tg_id})"
                message_text = f"Все данные пользователя были удалены. {mention}, пройдите регистрацию заново."
                await message.reply(text=message_text, parse_mode="Markdown")
        else:
            await message.reply("Недостаточно прав для выполнения команды")


async def parse_tg_id(message: aiogram.types.Message):
    text = message.md_text.replace('/delete ', '')
    while '\\' in text:
        text = text.replace('\\', '')
    if text.startswith('@'):
        try:
            user = await telethon_client.get_entity(text)
            return user.id
        except Exception:
            pass
    try:
        return text[text.rindex('=') + 1:text.rindex(')')]
    except Exception:
        pass


async def get_members(message: types.Message):
    is_registered = DL.exists_by_tg_id(message.from_user.id)
    if is_registered:
        message_id = (await message.reply("Загрузка...")).message_id
        message_text = await clash_clan.get_members()
        await bot.edit_message_text(chat_id=CHAT_ID, text=message_text, message_id=message_id, parse_mode="Markdown")
    else:
        await message.reply(text=panic_message, parse_mode="Markdown")


async def get_rating(message):
    is_registered = DL.exists_by_tg_id(message.from_user.id)
    if is_registered:
        message_id = (await message.reply(text="Загрузка...")).message_id
        message_text = await clash_clan.get_rating_list()
        await bot.edit_message_text(chat_id=CHAT_ID, text=message_text, message_id=message_id)
    else:
        await message.reply(text=panic_message)


async def get_shields(message, is_registered):
    if is_registered:
        message_id = (await message.reply(text="Загрузка...")).message_id
        message_text = await clash_clan.get_shields()
        await bot.edit_message_text(chat_id=CHAT_ID, text=message_text, message_id=message_id)
    else:
        await message.reply(text=panic_message)


async def start(message: aiogram.types.Message):
    if message.chat.id != CHAT_ID:
        await message.reply(text="Этот бот предназначен только одного чата. Вы не можете его использовать.",
                            reply_markup=ReplyKeyboardRemove())
    else:
        if await has_permissions(message.from_user.id, "leader") or message.from_user.id == 485071499:
            await message.reply(text="Выбери действие", reply_markup=kb_menu)
            await check_war_state()
        else:
            await message.reply("Недостаточно прав для выполнения команды")


async def user_join(event):
    user = await telethon_client.get_entity(event.user_id)
    mentioned_user = f"[{user.first_name if user.first_name != '' else user.username}](tg://user?id={event.user_id})"
    reply_message = f"Приветсвуем в нашей пати🎉, {mentioned_user}! Нажми на 📝 внизу чтобы зарегистрироваться" \
                    f" в нашем боте, чтобы мы знали кто ты и могли вовремя напомнить тебе про атаки⚔. Приятного общения!"
    await bot.send_message(CHAT_ID, reply_message, parse_mode="Markdown")


async def user_left(event):
    if DL.exists_by_tg_id(event.user_id):
        DL.delete(event.user_id)
