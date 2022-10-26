from db import DL


async def mention_user(player_tag, player_name):
    player_name = remove_symbols(player_name)
    if DL.exists_by_clash_tag(player_tag):
        user = DL.get_by_clash_tag(player_tag).fetchall()
        user_id = user[0][1]
        result = f"[{player_name}](tg://user?id={user_id})"
        return result
    else:
        return player_name


def remove_symbols(str):
    for char in str:
        if not char.isalnum():
            str = str.replace(char, '')
    return str


