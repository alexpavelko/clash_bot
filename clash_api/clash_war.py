from config.prefs import coc_client, CLAN_TAG, telethon_client
from config.resources.constants import hello_message
from db import DL


async def send_message_to_users_without_attacks(text_message):  # send to telegram private message that player must do attacks
    users_id_list = set(await get_telegram_users_id_list_without_attacks())
    for user_id in users_id_list:
        user = await telethon_client.get_entity(int(user_id))
        messages = await telethon_client.get_messages(user)
        if len(messages) == 0:
        #     print(f"tg_user:{user.username if user.username is not None else user.first_name}: {hello_message}")
        # print(f"tg_user:{user.username if user.username is not None else user.first_name}: {text_message}")
            await telethon_client.send_message(entity=user, message=hello_message)
        await telethon_client.send_message(entity=user, message=text_message)


async def get_tags_without_attacks():  # get player tags without attacks in war
    tags_without_attacks = []
    war = await coc_client.get_current_war(CLAN_TAG)
    attacks_count = war.attacks_per_member
    for member in war.clan.members:
        tags_without_attacks.append(member.tag)  # get all members list copy

    for attack in war.clan.attacks:
        member_attacks_count = len(attack.attacker.attacks)
        if member_attacks_count < attacks_count:
            tags_without_attacks.append(attack.attacker.tag)
    return tags_without_attacks


async def get_telegram_users_id_list_without_attacks():
    users_id_to_notify = []
    for tag_without_attacks in await get_tags_without_attacks():
        if DL.exists_by_clash_tag(tag_without_attacks):
            db_user = DL.get_by_clash_tag(tag_without_attacks).fetchall()
            if db_user[0][2] == tag_without_attacks:
                users_id_to_notify.append(db_user[0][1])
    return users_id_to_notify

