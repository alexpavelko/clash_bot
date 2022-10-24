# from aiogram import types
# from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
# from config.prefs import CLAN_TAG, CHAT_ID, MESSAGE_ID_TO_EDIT
# import telegram_chat
# import asyncio
# from aiogram.utils.exceptions import MessageNotModified
# import coc
#
# btn_get_warlog = InlineKeyboardButton(text="Статистика", callback_data="btn1")
# btn_get_attacker_info = InlineKeyboardButton(text="Атаки игроков", callback_data="btn2")
# warlog_markup = InlineKeyboardMarkup(row_width=2).add(btn_get_attacker_info)
# warlog_markup.add(btn_get_warlog)
#
#
# async def get_current_clan_war():  # get current war info
#     try:
#         return await coc_client.get_current_war(CLAN_TAG)
#     except coc.PrivateWarLog:
#         try:
#             msg = "Установите публичный варлог для клана в игре, чтобы видеть текущий расклад войны!"
#             await bot.edit_message_text(chat_id=CHAT_ID, text=msg,
#                                         message_id=MESSAGE_ID_TO_EDIT, reply_markup=warlog_markup)
#         except MessageNotModified:
#             pass
#
#
# async def get_tags_without_attacks():  # get player tags without attacks in war
#     attacks_count = 2
#     tags_without_attacks = []
#     clan_attackers = []
#     counts = {}
#     war = await coc_client.get_current_war(CLAN_TAG)
#     if war.is_cwl:
#         attacks_count = 1
#     for member in war.clan.members:
#         tag = member.tag
#         tags_without_attacks.append(tag)  # get all members list copy
#
#     for attack in war.attacks:
#         if not attack.attacker.is_opponent:
#             clan_attackers.append(attack.attacker.tag)  # get all players tags who made at list 1 attack
#
#     for n in clan_attackers:
#         counts[n] = counts.get(n, 0) + 1  # get amount of attacks for every player
#
#     for key, value in counts.items():
#         if value != attacks_count:
#             clan_attackers.remove(key)  # remove players from main list, who did < attacks_count attacks
#
#     for user in clan_attackers:
#         if user in tags_without_attacks:
#             tags_without_attacks.remove(user)  # get all players who must make attacks
#
#     return tags_without_attacks
#
#
# async def get_telegram_users_id_list_without_attacks():
#     users_id_to_notify = []
#     messages = await telethon_client.get_messages(CHAT_DB_ID, None)
#     for mes in messages:
#         if mes.message is not None:
#             id = mes.message[: mes.message.find("\n")]
#             tag = mes.message[mes.message.find("\n") + 1: mes.message.rfind("\n")]
#             for tag_without_attacks in await get_tags_without_attacks():
#                 if "#" + tag == tag_without_attacks:
#                     users_id_to_notify.append(int(id))
#     return users_id_to_notify
#
#
# async def get_war_time(war, flag):  # get string with hours and minutes to end of war
#     war_time = ""
#     if str(war.state) != "notInWar":
#         total_sec = war.end_time.seconds_until
#         if total_sec > 0:
#             hours = int(total_sec / 3600)
#             minutes = (int(total_sec / 60)) % 60
#             seconds = total_sec % 60
#             if flag is True:
#                 if hours == 6 and minutes == 0 and seconds == 0:
#                     war_time = f"До конца войны осталось {hours} часов! Успей провести атаку!"
#                     await telegram_chat.send_message_to_users_without_attacks(war_time)
#                 elif hours == 1 and minutes == 0 and seconds == 0:
#                     war_time = f"До конца войны остался всего {hours} час! Поторопись!!!"
#                     await telegram_chat.send_message_to_users_without_attacks(war_time)
#
#             else:
#                 war_time = f"До конца войны осталось {hours} часов {minutes} минут"
#         else:
#             war_time = "-1"
#     else:
#         msg = "Время запустить войну!"
#         await bot.edit_message_text(chat_id=CHAT_ID, text=msg,
#                                     message_id=MESSAGE_ID_TO_EDIT)
#         war_time = "-1"
#     return war_time
#
#
# @dp.callback_query_handler(text_contains='btn1')
# async def get_clan_war_statistics_callback(callback_query: types.CallbackQuery):
#     try:
#         msg = await get_clan_war_statistics()
#         await bot.send_message(CHAT_ID, f"{msg}")
#         await asyncio.sleep(5)
#     except coc.PrivateWarLog:
#         try:
#             msg = "Установите публичный варлог для клана в игре, чтобы видеть текущий расклад войны!"
#             await bot.edit_message_text(chat_id=CHAT_ID, text=msg,
#                                         message_id=MESSAGE_ID_TO_EDIT, reply_markup=warlog_markup)
#         except MessageNotModified:
#             pass
#
#
# @dp.callback_query_handler(text_contains="btn2")
# async def get_my_team_statistics_callback(callback_query: types.CallbackQuery):
#     try:
#         msg = await get_my_team_statistics()
#         await bot.send_message(CHAT_ID, msg)
#         await asyncio.sleep(5)
#     except coc.PrivateWarLog:
#         try:
#             msg = "Установите публичный варлог для клана в игре, чтобы видеть текущий расклад войны!"
#             await bot.edit_message_text(chat_id=CHAT_ID, text=msg,
#                                         message_id=MESSAGE_ID_TO_EDIT, reply_markup=warlog_markup)
#         except MessageNotModified:
#             pass
#
#
# async def get_clan_war_statistics():  # return string with count of teams attacks
#     war = await coc_client.get_current_war(CLAN_TAG)
#     if war.is_cwl:
#         team_max_attacks = war.team_size
#     else:
#         team_max_attacks = war.team_size * 2
#     opponents = ""
#     teammates = ""
#     i = 0
#     j = 0
#     for attack in war.attacks:
#         if attack.attacker.is_opponent:
#             i += 1
#             opponents += f"\n{i}. {attack.attacker.name}[{attack.attacker.map_position}] ->" \
#                          f" {attack.defender.name}[{attack.defender.map_position}] ({attack.stars}⭐)"
#         else:
#             j += 1
#             teammates += f"\n{j}. {attack.attacker.name}[{attack.attacker.map_position}] ->" \
#                          f" {attack.defender.name}[{attack.defender.map_position}] ({attack.stars}⭐) "
#     msg = f"\nКоманда:\n{teammates}\n\nПротивник:{opponents}\n\n" + \
#           f"Атак осталось у нашей команды — {team_max_attacks - j}\n" + \
#           f"Атак осталось у вражеской команды — {team_max_attacks - i}"
#     if len(opponents) == 0 or len(teammates) == 0:
#         msg = "Атаки не найдены."
#     return msg
#
#
# async def get_my_team_statistics():  # return string with count of my team attacks
#     war = await coc_client.get_current_war(CLAN_TAG)
#     if war.is_cwl:
#         team_max_attacks = war.team_size
#     else:
#         team_max_attacks = war.team_size * 2
#     msg = ""
#     list2 = []
#     for attack in war.clan.attacks:
#         if attack.attacker not in list2:
#             list2.append(attack.attacker)
#     counter = 0
#     for attacker in list2:
#         for attack in attacker.attacks:
#             if not attacker.is_opponent:
#                 counter += 1
#                 msg += f"[{attack.attacker.name}]\n"
#                 msg += f"атака №{counter} -> [{attack.defender.map_position}]{attack.defender.name}" \
#                        f"({attack.stars}⭐️,{attack.destruction}%)\n"
#
#     msg += "\nАтак осталось у нашей команды — " + str(team_max_attacks - counter)
#     if len(msg) == 0:
#         msg = "Атаки не найдены!"
#     return msg
#
#
# async def get_loosers(war):  # get string of players, who did not carry out attacks
#     loosers = ""
#     if war.state == "warEnded":
#         for member in war.clan.members:
#             if member.star_count == 0:
#                 loosers += member.name + "\n"
#     return loosers