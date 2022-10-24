import asyncio
import operator

from clash_api.clash_player import mention_user
from config.resources.constants import roles, war_result, shield_colors
from config.prefs import CLAN_TAG, coc_client


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


async def get_roles():
    clan = await coc_client.get_clan(CLAN_TAG)
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
    war = await coc_client.get_current_war(CLAN_TAG)
    if war is None:
        return "Война не запущена."
    while war.end_time:
        await get_war_scores(war)
        await asyncio.sleep(31)
    print(f"Война завершена. Результат: {war_result[war.state]}")
    await get_shields()
    await coc_client.close()
