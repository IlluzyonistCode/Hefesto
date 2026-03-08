import subprocess
import time

from ui.colors import paint
from modules.minecraft.get_minecraft_server_data import GetMinecraftServerData
from core.config_manager import JsonManager
from utils.network import GetUtilities
from utils.validation import CheckUtilities


def kickall_command(server, version, loop, *args):
    

    try:
        if not CheckUtilities.check_loop_argument(loop):
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "invalidArguments", "invalidLoopArgument"])}')
            return
        
        loop = GetUtilities.get_loop_argument(loop)
        
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "gettingDataFromServer"])}')
        server_data = GetMinecraftServerData.get_data(server, bot=False)

        if server_data is None:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "invalidArguments", "invalidServer"])}')
            return
        
        if server_data['platform_type'] != 'Java':
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "errorBedrockServer"])}')
            return
        
        players = []

        server = server_data['ip_port']
        ip, port = server.split(':')

        if server_data['default_player_list'] is not None and len(server_data['default_player_list']) >= 1:
            for player in server_data['default_player_list']:
                if type(player) == dict:
                    if player['name'] != 'Anonymous Player':
                        players.append(player['name'])
                else:
                    paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "kickall", "noPlayers"])}')
                    return
        else:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "kickall", "noPlayers"])}')
            return
        
        if len(players) == 0:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "kickall", "noPlayers"])}')
            return

        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "kickall", "startingTheAttack"])}')
        
        if loop:
            while loop:
                time.sleep(1)
                
                for player in players:
                    if JsonManager.get(["minecraftServerOptions", "proxy"]):
                        command = f'{JsonManager.get(["minecraftServerOptions", "nodeCommand"])} ./hefesto_files/scripts/kick.js {ip} {port} {player} {version} {len(GetUtilities.get_spaces())} {JsonManager.get(["minecraftServerOptions", "proxyFileForTheBot"])}'

                    else:
                        command = f'{JsonManager.get(["minecraftServerOptions", "nodeCommand"])} ./hefesto_files/scripts/kick.js {ip} {port} {player} {version} {len(GetUtilities.get_spaces())}'
                    
                    subprocess.run(command, shell=True)

        if not loop:
            for player in players:
                if JsonManager.get(["minecraftServerOptions", "proxy"]):
                    command = f'{JsonManager.get(["minecraftServerOptions", "nodeCommand"])} ./hefesto_files/scripts/kick.js {ip} {port} {player} {version} {len(GetUtilities.get_spaces())} {JsonManager.get(["minecraftServerOptions", "proxyFileForTheBot"])}'

                else:
                    command = f'{JsonManager.get(["minecraftServerOptions", "nodeCommand"])} ./hefesto_files/scripts/kick.js {ip} {port} {player} {version} {len(GetUtilities.get_spaces())}'
                
                subprocess.run(command, shell=True)

    except KeyboardInterrupt:
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "ctrlC"])}')

