from config.prefs import coc_client, CLAN_TAG, telethon_client, bot, CHAT_ID
from config.resources.constants import hello_message
from db import DL


async def create_war_state_message(war, hours):
    if hours == 24:
        result_msg = "Кв началось, самое время провести первую атаку!"
    else:
        result_msg = f"\nДо конца кв осталось {hours} часов\n"
        if war.clan.tag == CLAN_TAG:
            scores_string = f"Счет: {war.clan.name}:{war.clan.stars}⭐ ⚔ {war.opponent.stars}⭐ {war.opponent.name}"
        else:
            scores_string = f"Счет: {war.opponent.name}{war.opponent.stars}⭐ ⚔ {war.clan.stars}⭐ {war.clan.name}"
        result_msg += scores_string + "\nПользователи уведомлены."
    return result_msg


async def send_message_to_users_without_attacks(text_message, war, hours):
    users_id_list = set(await get_telegram_users_id_list_without_attacks())
    for user_id in users_id_list:
        user = await telethon_client.get_entity(int(user_id))
        messages = await telethon_client.get_messages(user)
        if len(messages) == 0:
            await telethon_client.send_message(entity=user, message=hello_message)
        await telethon_client.send_message(entity=user, message=text_message)
        if len(users_id_list) > 0:
            result_msg = await create_war_state_message(war, hours)
            try:
                await bot.send_message(chat_id=CHAT_ID, text=result_msg)
            except Exception:
                pass


async def get_tags_without_attacks():
    tags_without_attacks = []
    war = await coc_client.get_current_war(CLAN_TAG)
    attacks_count = war.attacks_per_member
    for member in war.clan.members:
        if len(member.attacks) < attacks_count:
            tags_without_attacks.append(member.tag)
    return tags_without_attacks


async def get_telegram_users_id_list_without_attacks():
    users_id_to_notify = []
    for tag_without_attacks in await get_tags_without_attacks():
        if DL.exists_by_clash_tag(tag_without_attacks):
            db_user = DL.get_by_clash_tag(tag_without_attacks).fetchall()
            if db_user[0][2] == tag_without_attacks:
                users_id_to_notify.append(db_user[0][1])
    return users_id_to_notify

