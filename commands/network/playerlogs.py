import datetime
import time
import re

from utils.log_manager import LogManager
from core.config_manager import JsonManager
from ui.colors import paint
from ui.mccolor.mc_remove import mcremove
from utils.network import GetUtilities
from modules.minecraft.get_minecraft_server_data import GetMinecraftServerData


def playerlogs_command(server):
    

    old_players = []
    regex = r'\((.*?)\)'

    try:
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "gettingDataFromServer"])}')
        server_data = GetMinecraftServerData.get_data(server, bot=False)

        if server_data is None:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "invalidArguments", "invalidServer"])}')
            return
        
        if server_data['platform_type'] != 'Java':
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "errorBedrockServer"])}')
            return

        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "listening", "waitingForPlayers"])}')
        
        if JsonManager.get('logs'):
            log_file = LogManager.create_log_file('playerlogs')
            LogManager.write_log(log_file, 'playerlogs', f'Target: {server}\n')

    except KeyboardInterrupt:
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "ctrlC"])}')
        return

    while True:
        try:
            server_data = GetMinecraftServerData.get_data(server, bot=False)
            players = []

            if server_data is not None:
                if server_data['platform_type'] == 'Bedrock':
                    continue

                if server_data['default_player_list'] is not None:
                    for player in server_data['default_player_list']:
                        if type(player) is dict:
                            username = player['name']
                            uuid = player.get('uuid', player.get('id', None))

                            if username != '':
                                player_found = f'{username} ({uuid})'
                                players.append(player_found)

                else:
                    continue

                removed_players = set(old_players) - set(players)
                added_players = set(players) - set(old_players)
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                for player in removed_players:
                    user = player.split(' (')[0]
                    uuid = re.search(regex, player).group(1)
                    data = f'{user} &f&l({GetUtilities.get_uuid_color(user, uuid)}{uuid}&f&l'
                    log_data = f'\n🔴 {current_time} {data}'
                    paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "playerlogs", "disconnectedUser"]).replace("[0]", current_time).replace("[1]", data)}')

                    if JsonManager.get('logs'):
                        LogManager.write_log(log_file, 'playerlogs', mcremove(log_data))

                for player in added_players:
                    user = player.split(" (")[0]
                    uuid = re.search(regex, player).group(1)
                    data = f'{user} &f&l({GetUtilities.get_uuid_color(user, uuid)}{uuid}&f&l)'
                    log_data = f'\n🟢 {current_time} {data}'
                    paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "playerlogs", "connectedUser"]).replace("[0]", current_time).replace("[1]", data)}')
                    players.append(player)

                    if JsonManager.get('logs'):
                        LogManager.write_log(log_file, 'playerlogs', mcremove(log_data))

                old_players = players
                time.sleep(1)

            else:
                time.sleep(5)

        except (KeyboardInterrupt):
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "ctrlC"])}')
            return

