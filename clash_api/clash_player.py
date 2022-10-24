from db import DL


async def mention_user(player_tag, player_name):
    user = DL.get_by_clash_tag(player_tag).fetchall()
    if len(user) != 0:
        user_id = user[0][1]
        result = f"[{player_name}](tg://user?id={user_id})"
        return result
    else:
        return player_name


