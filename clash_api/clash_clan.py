import asyncio
import operator

from clash_api import clash_war
from clash_api.clash_player import mention_user
from config.prefs import CLAN_TAG, coc_client, ACADEMY_CLAN_TAG
from config.resources.constants import roles, war_result, shield_colors


async def get_shields():
    clan = await coc_client.get_clan(CLAN_TAG)
    players = []
    green_shields, number, current_th = 0, 1, 16
    result_message = "\nПосмотрите, кто готов к следующей войне.\n\n"
    for member in clan.members:
        player = await coc_client.get_player(member.tag)
        player_info = {
            "name": player.name,
            "town_hall": player.town_hall,
            "war_opted_in": player.war_opted_in,
        }
        players.append(player_info)
    players.sort(key=operator.itemgetter("war_opted_in", "town_hall"), reverse=True)
    for player in players:
        if current_th != player["town_hall"]:
            current_th = player["town_hall"]
            result_message += f"Тх{current_th}:\n"
        if player["war_opted_in"]:
            green_shields += 1
        result_message += f"[{shield_colors[player['war_opted_in']]}] {player['name']}\n"
        number += 1
    result_message += f"\nК войне готово {green_shields} игроков."
    return result_message


async def get_roles(clan):
    players = []
    result_string, current_role = "", "глава"
    number = 1
    for member in clan.members:
        player = await coc_client.get_player(member.tag)
        player_info = {
            "name": await mention_user(player.tag, player.name),
            "town_hall": player.town_hall,
            "role": roles[str(member.role).lower()]
        }
        players.append(player_info)
    players.sort(key=operator.itemgetter("town_hall"), reverse=True)
    players.sort(key=operator.itemgetter("role"))
    for player in players:
        if current_role != player["role"]:
            result_string += "\n"
            current_role = player["role"]
        result_string += f"{number}. {player['name']} ({player['town_hall']}тх), {player['role']}\n"
        number += 1
    return result_string


async def get_members():
    clan = await coc_client.get_clan(CLAN_TAG)
    academy_clan = await coc_client.get_clan(ACADEMY_CLAN_TAG)
    result_message = "Игроки Dark Elite\n\n"
    result_message += await get_roles(clan)
    result_message += "\n\nИгроки академа(D.Elite Academy)\n\n"
    result_message += await get_roles(academy_clan)
    return result_message


def get_hero_percent(player, player_sum_level=0, player_max_sum_level=0, player_min_sum_level=0):
    for hero in player.heroes:
        if hero.is_home_base:
            player_sum_level += hero.level
            player_max_sum_level += hero.get_max_level_for_townhall(player.town_hall)
            previous_th = 7 if player.town_hall < 7 else player.town_hall - 1
            try:
                player_min_sum_level += hero.get_max_level_for_townhall(previous_th)
            except Exception:
                pass
    percent = int(100 - ((player_max_sum_level - player_sum_level) * 100 / (
            player_max_sum_level - player_min_sum_level)))
    return percent


async def get_rating_list():
    clan = await coc_client.get_clan(CLAN_TAG)
    players_to_draw = []
    for member in clan.members:
        player = await coc_client.get_player(member.tag)
        hero_percent = get_hero_percent(player)
        players_to_draw.append({'name': player.name, 'town_hall': player.town_hall, 'hero_percent': hero_percent})
    return "Рейтинг игроков Dark Elite:\n\n" + get_progress_for_clan(players_to_draw)


def get_progress_for_clan(players):
    result_msg = ""
    current_th = -1
    players.sort(key=operator.itemgetter("town_hall", "hero_percent"), reverse=True)
    for player in players:
        if current_th is not player["town_hall"]:
            current_th = player["town_hall"]
            result_msg += f"Тх{current_th}:" + "\n"
        result_msg += get_progress_for_player(player)
    return result_msg


def get_progress_for_player(player, total=100):
    bar_len = 6
    result_msg = ""
    filled_len = int(round(bar_len * player["hero_percent"] / total))
    filled_len = 0 if filled_len < 0 else filled_len
    bar = '🟩' * filled_len + '🟥' * (bar_len - filled_len)
    result_msg += f"[{bar}] {int(player['hero_percent'])}% {player['name']}" + "\n"
    return result_msg


async def notify_attacks(total_sec, war):
    if total_sec == 3600:
        text_message = f"До конца войны остался 1 час! Проведи атаки!"
        await clash_war.send_message_to_users_without_attacks(text_message, war, 3600)
    elif total_sec == 3600 * 6:
        text_message = f"До конца войны осталось 6 часов, проведи атаки!"
        await clash_war.send_message_to_users_without_attacks(text_message, war, 3600 * 6)
    elif total_sec == 3600 * 12:
        text_message = f"Прошло 12 часов, проведи атаки в клешке!"
        await clash_war.send_message_to_users_without_attacks(text_message, war, 3600 * 12)
    elif total_sec == 3600 * 23 + 3540:
        text_message = f"Кв началось, время провести первую атаку!"
        await clash_war.send_message_to_users_without_attacks(text_message, war, 3600 * 23 + 59 * 60)


async def check_war_state():
    war = await coc_client.get_current_war(CLAN_TAG)
    if war is None:
        return "Война не запущена."

    total_sec = war.end_time.seconds_until

    while 0 < total_sec < 24 * 3600:
        total_sec = war.end_time.seconds_until
        await notify_attacks(total_sec, war)
        await asyncio.sleep(1)
    shields = await get_shields()
    return f"Война завершена. Результат: {war_result[war.status]}\n{shields}"



