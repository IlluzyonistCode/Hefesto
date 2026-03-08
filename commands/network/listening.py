import time

from utils.log_manager import LogManager
from core.config_manager import JsonManager
from ui.colors import paint
from utils.network import GetUtilities
from modules.minecraft.get_minecraft_server_data import GetMinecraftServerData


def listening_command(server, *args):
    

    captured_players = []
    found = False
    t = ''

    try:
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "gettingDataFromServer"])}')
        server_data = GetMinecraftServerData.get_data(server, bot=False)

        if server_data is None:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "invalidArguments", "invalidServer"])}')
            return
        
        if server_data['platform_type'] != 'Java':
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "errorBedrockServer"])}')
            return

        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "listening", "waitingForPlayers"])}\n')
        
        if JsonManager.get('logs'):
            log_file = LogManager.create_log_file('listening')
            LogManager.write_log(log_file, 'listening', f'Target: {server}\n')

    except KeyboardInterrupt:
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "ctrlC"])}')
        return

    while True:
        try:
            server_data = GetMinecraftServerData.get_data(server, bot=False)

            if server_data is not None:
                if server_data['platform_type'] == 'Bedrock':
                    continue

                if server_data['default_player_list'] is not None:
                    for player in server_data['default_player_list']:
                        if type(player) is dict:
                            username = player['name']
                            uuid = player.get('uuid', player.get('id', None))

                            if uuid is None:
                                continue

                            if not found:
                                paint(f'{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "listening", "foundPlayers"])}\n')
                                t = '\n'
                                found = True

                            if f'{username} ({uuid})' not in captured_players:
                                captured_players.append(f'{username} ({uuid})')
                                log_data = f'{username} ({uuid})'

                                if JsonManager.get('logs'):
                                    LogManager.write_log(log_file, 'listening', log_data)
                                
                                paint(f'{GetUtilities.get_spaces()}&f&l{username} ({GetUtilities.get_uuid_color(username, uuid)}{uuid}&f&l)')

            else:
                time.sleep(30)

            time.sleep(1)

        except KeyboardInterrupt:
            paint(f'{t}{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "ctrlC"])}')
            break

