import asyncio
from random import randint

from aiogram.utils.exceptions import MessageNotModified
from coc import WarRound

from clash_api import clash_player, clash_war, clash_clan
from clash_api.clash_clan import *
# from clash_api.clash_war import warlog_markup, get_loosers
# from config.prefs import CHAT_ID, MESSAGE_ID_TO_EDIT, CLAN_TAG, USER_BOT


# async def create_pinned_message(war):  # return string with war stars and time to end
#     if await clash_war.get_war_time(war, False) != "-1":
#         msg = f"{war.clan.name}: {war.clan.stars}⭐  ⚔️ {war.opponent.stars}⭐ {war.opponent.name}" \
#               f" \n{await clash_war.get_war_time(war, False)}"
#     else:
#         msg = f"Война завершена: {war.clan.name}: {war.clan.stars}⭐  ⚔️ {war.opponent.stars}⭐ {war.opponent.name}"
#     return msg
#
#
# async def edit_cw_info():  # if war is cw, sends info to pinned message
#     war = await clash_war.get_current_clan_war()
#
#     if war is not None:
#         while war.state != "warEnded":
#             await edit_pinned_message()
#             await asyncio.sleep(30)
#         await edit_war_finished_message(war)
#         await send_message_to_leader(war)
#     else:
#         msg = "Время запустить войну!"
#         await bot.edit_message_text(chat_id=CHAT_ID, text=msg,
#                                     message_id=MESSAGE_ID_TO_EDIT)
#
#
# async def edit_cwl_info():  # if war is cwl, sends info to pinned message
#     while True:
#         league_group = await coc_client.get_league_group(CLAN_TAG)  # get current cwl clans group
#         wars = league_group.get_wars(WarRound.current_war)  # get all cwl wars
#         print(wars)
#         war = await wars.__anext__()  # get current war
#         msg = await create_pinned_message(war)  # print info to the pinned telegram message
#         try:
#             await bot.edit_message_text(chat_id=CHAT_ID, text=msg,
#                                         message_id=MESSAGE_ID_TO_EDIT, reply_markup=warlog_markup)
#         except MessageNotModified:
#             pass
#         await asyncio.sleep(30)  # every 30 seconds
#     await edit_war_finished_message(war)  # if war is ended - notify results
#     await send_message_to_leader(war)  # and send nicknames, who made 0 attacks
#
#
# async def edit_pinned_message():  # send to pinned message of telegram info of war stars and time to end
#     war = await clash_war.get_current_clan_war()
#     msg = await create_pinned_message(war)
#     try:
#         await bot.edit_message_text(chat_id=CHAT_ID, text=msg,
#                                     message_id=MESSAGE_ID_TO_EDIT, reply_markup=warlog_markup)
#     except MessageNotModified:
#         pass
#
#
# async def edit_war_finished_message(war):  # edit telegram pinned message if war is ended
#     msg = f"Война завершена: {war.clan.name}: {war.clan.stars}⭐  ⚔️ {war.opponent.stars}⭐ {war.opponent.name}"
#     await bot.edit_message_text(chat_id=CHAT_ID, text=msg,
#                                 message_id=MESSAGE_ID_TO_EDIT, reply_markup=warlog_markup)
#
#
# # async def find_clan_leader_tg_id():  # get telegram id of clan leader
# #     leader_tag = await find_clan_leader_tag()
# #     result = "#"
# #     messages = await telethon_client.get_messages(CHAT_DB_ID, None)
# #     for mes in messages:
# #         if mes.message is not None:
# #             tag = mes.message[mes.message.find("\n") + 1: mes.message.rfind("\n")]
# #             id = mes.message[: mes.message.find("\n")]
# #             if "#" + tag == leader_tag:
# #                 result = id
# #     return result
#
#
# # async def send_message_to_leader(war):  # send message with players, who made 0 attacks
# #     clan_leader = await find_clan_leader_tg_id()
# #     mention = "[" + " глава клана" + "](tg://user?id=" + str(clan_leader) + ")"
# #     await bot.send_message(CHAT_ID, f"Уважаемый, {mention},"
# #                                     f" следующие игроки принесли 0 звезд, просьба их отшлепать:\n"
# #                                     f"{await get_loosers(war)}", parse_mode="Markdown")
#
#
# async def get_users_info():  # send to telegram list of users bot register state
#     msg = ""
#     wmsg = ""
#     all_tg_id = []
#     for chat_member in await telethon_client.get_participants(CHAT_ID):
#         if chat_member.bot is False and chat_member.first_name != USER_BOT:
#             all_tg_id.append(chat_member.id)
#     messages = await telethon_client.get_messages(CHAT_DB_ID, None)
#     for mes in messages:
#         if mes.message is not None:
#             id = mes.message[: mes.message.find("\n")]
#             tag = mes.message[mes.message.find("\n") + 1: mes.message.rfind("\n")]
#             player = await coc_client.get_player(tag)
#             from telethon.tl.types import PeerUser
#             tg_user = await telethon_client.get_entity(PeerUser(int(id)))
#             msg += tg_user.first_name + "зареган как " + player.name + "\n"
#             if id not in all_tg_id:
#                 wmsg += tg_user.first_name + " - не зареган!" + "\n"
#     if msg != "":
#         await bot.send_message(chat_id=CHAT_ID, text=msg+wmsg)
#
#
# async def send_message_to_users_without_attacks(war_time):  # send telegram private message that player must do attacks
#     war = await coc_client.get_current_war(CLAN_TAG)
#     users_id_list = await clash_war.get_telegram_users_id_list_without_attacks()
#     dialogs = await telethon_client.get_dialogs()
#     participants = await telethon_client.get_participants(CHAT_ID)
#     first_message = "Привет, это clash of clans бот. Если ты не против, я буду напоминать тебе про атаки на кв. Если " \
#                     "тебе это не надо - кинь меня в чс "
#     for user in participants:
#         if user.id in users_id_list:
#             messages = await telethon_client.get_messages(user)
#             if len(messages) == 0:
#                 await telethon_client.send_message(entity=user, message=first_message)
#             if war_time == "":
#                 war_time = "Прямо сейчас ты нужен на кв!" + await clash_war.get_war_time(war, False)
#             await telethon_client.send_message(entity=user, message=war_time)
#
#     if users_id_list != 0:
#         await bot.send_message(chat_id=CHAT_ID, text="Пользователи уведомлены в лс.")
#     else:
#         await bot.send_message(CHAT_ID, "Некого уведомлять, все атаки проведены.")
#
#
# async def notify_mafia():
#     msg = "Созываю мафиози!\n"
#     values = ['👨🏼', '👨🏼‍⚕️', '🤵🏻', '🕵🏼️‍♂️', '💃🏼', '😇', '😎', '🧑‍🏭', '👮‍♀️', '👲', '🤴', '🥷', '🦹‍♀️']
#     for participant in await telethon_client.get_participants(CHAT_ID):
#         if participant.first_name is not None and participant.bot is False and participant.first_name != USER_BOT:
#             rnd = randint(0, len(values) - 1)
#             msg += "[" + values[rnd] + "](tg://user?id=" + str(participant.id) + ")"
#     await bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode="Markdown")
#
#
# async def send_hero_statistics(user_id):
#     messages = await telethon_client.get_messages(CHAT_DB_ID, None)
#     authorized = False
#     tags = []
#     msg = ""
#     for mes in messages:
#         if mes.message is not None:
#             id = mes.message[: mes.message.find("\n")]
#             if str(id) == str(user_id):
#                 authorized = True
#                 tags.append(mes.message[mes.message.find("\n") + 1: mes.message.rfind("\n")])
#
#     if authorized is True:
#         for tag in tags:
#             player = await coc_client.get_player(tag)
#             result = await clash_player.get_percent_heroes(player)
#             msg += player.name + ": " + "Прокачка героев = " + str(int(result)) + "%" + "\n"
#     else:
#         msg = "Сперва зарегистрируйтесь!"
#     await bot.send_message(CHAT_ID, msg)
#
#
# async def pin_mafia_msg(event):
#     mafia_bot_id = 468253535
#     msg_id = event.message.to_dict()['id']
#     msg_text = event.message.to_dict()['message']
#     from_id = str(event.message.to_dict()["from_id"])
#     sender_id = (from_id.split(":")[-1]).replace('}', '').replace(' ', '')
#
#     if msg_text == "Ведётся набор в игру" and str(sender_id) == str(mafia_bot_id):
#         await telethon_client.pin_message(message=msg_id, notify=False, entity=CHAT_ID)
#
#
# async def notify_attacks(message):
#     id = message.from_user.id
#     user = await bot.get_chat_member(chat_id=CHAT_ID, user_id=id)
#     if user.status == "member":
#         await message.reply(text="Недостататочно прав на выполнение этой команды.")
#     else:
#         await send_message_to_users_without_attacks("")
#
#
# def send_leaders_table():
#     return None
#
#

