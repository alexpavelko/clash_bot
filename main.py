import coc
from aiogram import types
from aiogram.utils import executor
from clash_api.clash_clan import *
from clash_api.events import register_markup
from config.prefs import CHAT_ID, CLAN_TAG, coc_client, dp, bot
import services
from db import DL


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await services.start(message)


@dp.message_handler(commands=['delete'])
async def delete_user(message: types.Message):
    await services.delete_user(message)


@dp.message_handler()
async def answer_menu(message: types.Message):
    if message.chat.id == -1001158139685:
        await message.reply("Бот находиться на тестировании🛠. Просьба не беспокоить его лишний раз :3")
        return -1
    if message.text == "📝":
        await message.reply("Кто ты в игре?", reply_markup=await register_markup())
    elif message.text == "👨‍💼":
        await services.get_members(message)
    elif message.text == "👑":
        await services.get_rating(message)


@coc_client.event
@coc.ClanEvents.member_join(tags=[CLAN_TAG])
async def on_clan_member_join(member, clan):
    await bot.send_message(CHAT_ID, f" {member.name} вступил в клан")
    player = await coc_client.get_player(member.tag)
    percent = get_hero_percent(player)
    await bot.send_message(CHAT_ID, f"Прокачка героев игрока для его тх({player.town_hall}) = {int(percent)}%")


@coc_client.event
@coc.ClanEvents.member_leave(tags=[CLAN_TAG])
async def on_clan_member_leave(member, clan):
    await bot.send_message(CHAT_ID, f"{member.name} покинул клан")


if __name__ == '__main__':
    executor.start_polling(dp)



