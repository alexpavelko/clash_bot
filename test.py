import asyncio
import operator

import coc
from aiogram.utils import executor

from config.prefs import CHAT_ID, telethon_client

CLAN_TAG = "#RYLQCJ2J"
war_result = {"tie": " ничья",
              "won": "победа!",
              "lost": "поражение",
              "winning": "побеждаем",
              "tied": "ничья",
              "losing": "поражение",
              "inWar": "определить не удалось",
              "warEnded": "определить не удалось"}
roles = {
    "leader": "глава",
    "co-leader": "соруководитель",
    "elder": "старейшина",
    "member": "участник",
}

separator_line = "------------------------------------------------------------------\n"


async def get_roles():
    coc_client = coc.Client()
    try:
        await coc_client.login('pavelkobond@gmail.com', 'Sanya_007')
    except coc.InvalidCredentials as error:
        exit(error)
    clan = await coc_client.get_clan(CLAN_TAG)
    players = []
    result_string = ""
    number = 1
    for member in clan.members:
        player = await coc_client.get_player(member.tag)
        player_info = {
            "name": member.name,
            "town_hall": player.town_hall,
            "role": roles[str(member.role).lower()]
        }
        players.append(player_info)
    players.sort(key=operator.itemgetter("role", "town_hall"))
    current_role = "глава"
    for player in players:
        if current_role != player["role"]:
            result_string += separator_line
            current_role = player["role"]
        result_string += f"{number}. {player['name']} ({player['town_hall']}тх), {player['role']}\n"
        number += 1
    print(result_string)
    await coc_client.close()


async def get_shields():
    coc_client = coc.Client()
    try:
        await coc_client.login('pavelkobond@gmail.com', 'Sanya_007')
    except coc.InvalidCredentials as error:
        exit(error)
    clan = await coc_client.get_clan(CLAN_TAG)
    list = []
    for member in clan.members:
        player = await coc_client.get_player(member.tag)
        player_info = {
            "name": player.name,
            "town_hall": player.town_hall,
            "war_opted_in": player.war_opted_in,
        }
        list.append(player_info)
    sorted_players = sorted(list, key=operator.itemgetter("war_opted_in", "town_hall"), reverse=True)
    number = 1
    for p in sorted_players:
        shield_color = "✅" if p["war_opted_in"] else "🟥"
        town_hall = f"{p[str('town_hall')]}. " if p[str('town_hall')] < 10 else f"{p[str('town_hall')]}."
        print(f"{' ' if number < 10 else ''}{number}. Тх{town_hall} Щит[{shield_color}] {p['name']}")
        number += 1

    await coc_client.close()


def get_hero_percent(player, player_sum_level_of_heroes, player_max_sum_level, player_min_sum_level):

    for hero in player.heroes:
        if hero.is_home_base:
            player_sum_level_of_heroes += hero.level
            hero.get_max_level_for_townhall()
            player_max_sum_level += hero.get_max_level_for_townhall(player.town_hall)
            previous_th = 7 if player.town_hall < 7 else player.town_hall - 1
            try:
                player_min_sum_level += hero.get_max_level_for_townhall(previous_th)
            except Exception:
                pass
    percent = int(100 - ((player_max_sum_level - player_sum_level_of_heroes) * 100 / (
            player_max_sum_level - player_min_sum_level)))
    return percent


async def get_rating_list():
    
    coc_client = coc.Client()
    try:
        await coc_client.login('pavelkobond@gmail.com', 'Sanya_007')
    except coc.InvalidCredentials as error:
        exit(error)
    CLAN_TAG = "#RYLQCJ2J"
    clan = await coc_client.get_clan(CLAN_TAG)
    players_to_draw = []
    for member in clan.members:
        player = await coc_client.get_player(member.tag)
        hero_percent = get_hero_percent(player, 0, 0, 0)
        players_to_draw.append({'name': player.name, 'town_hall': player.town_hall, 'hero_percent': hero_percent})
    get_progress_for_clan(players_to_draw)

    await coc_client.close()


def get_progress_for_clan(players):
    result_msg = ""
    current_th = -1
    players.sort(key=operator.itemgetter("town_hall", "hero_percent"), reverse=True)
    for player in players:
        if current_th is not player["town_hall"]:
            current_th = player["town_hall"]
            result_msg += f"Тх{current_th}:" + "\n"
        result_msg += get_progress_for_player(player)
    print(result_msg)


def get_progress_for_player(player, total=100):
    bar_len = 6
    result_msg = ""
    filled_len = int(round(bar_len * player["hero_percent"] / total))
    filled_len = 0 if filled_len < 0 else filled_len
    percents = 100 * player["hero_percent"] / total
    bar = '🟩' * filled_len + '🟥' * (bar_len - filled_len)
    result_msg += f"[{bar}] {int(percents)}% {player['name']}" + "\n"
    return result_msg


def notify_attacks(message):
    pass


async def get_war_scores(war):
    result_msg = ""
    if war.clan.tag == CLAN_TAG:
        scores_string = f"{war.clan.name}:{war.clan.stars}⭐ ⚔ {war.opponent.stars}⭐ {war.opponent.name}"
    else:
        scores_string = f"{war.opponent.name}{war.opponent.stars}⭐ ⚔ {war.clan.stars}⭐ {war.clan.name}"
    result_msg += scores_string
    total_sec = war.end_time.seconds_until
    if total_sec > 0:
        hours = int(total_sec / 3600)
        minutes = (int(total_sec / 60)) % 60
        time_string = f"{minutes} минут\n" if hours == 0 else f"{hours} часов {minutes} минут\n"
        result_msg += f"\nДо конца кв осталось {time_string}\n"
        if total_sec == 3600 or total_sec == 3600 * 2 or total_sec == 3600 * 6:
            message = f"Привет, проведи атаки в клешке, до конца войны осталось {time_string}"
            notify_attacks(message)
    print(result_msg)
    return result_msg


async def check_war_state():
    coc_client = coc.Client()
    try:
        await coc_client.login('pavelkobond@gmail.com', 'Sanya_007')
    except coc.InvalidCredentials as error:
        exit(error)
    war = await coc_client.get_current_war(CLAN_TAG)
    if war is None:
        return "Война не запущена."
    while war.end_time:
        await get_war_scores(war)
        await asyncio.sleep(31)
    print(f"Война завершена. Результат: {war_result[war.state]}")
    await get_shields()
    await coc_client.close()


if __name__ == "__main__":
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(get_shields())

        # executor.start_polling(dp)

    except KeyboardInterrupt:
        pass
