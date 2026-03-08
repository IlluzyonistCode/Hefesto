import subprocess
import os

from ui.colors import paint
from modules.minecraft.get_minecraft_server_data import GetMinecraftServerData
from core.config_manager import JsonManager
from utils.network import GetUtilities 
from utils.validation import CheckUtilities


def pinlogin_command(server, username, version, password_file, *args):
    

    try:
        if not os.path.exists(password_file):
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "invalidArguments", "invalidFile"]).replace("[0]", password_file)}')
            return
        
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "gettingDataFromServer"])}')
        server_data = GetMinecraftServerData.get_data(server, bot=False)

        if server_data is None:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "invalidArguments", "invalidServer"])}')
            return

        server = server_data['ip_port']
        ip, port = server.split(':')

        with open(password_file, 'r', encoding=CheckUtilities.check_file_encoding(password_file)) as f:
            passwords = f.readlines()

        if len(passwords) == 0:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "pinlogin", "emptyFile"])}')
            return

        if JsonManager.get(["minecraftServerOptions", "proxy"]):
            command = f'{JsonManager.get(["minecraftServerOptions", "nodeCommand"])} ./hefesto_files/scripts/pinlogin.js {ip} {port} {username} {version} {password_file} {len(GetUtilities.get_spaces())} {JsonManager.get(["minecraftServerOptions", "proxyFileForTheBot"])}'

        else:
            command = f'{JsonManager.get(["minecraftServerOptions", "nodeCommand"])} ./hefesto_files/scripts/pinlogin.js {ip} {port} {username} {version} {password_file} {len(GetUtilities.get_spaces())}'
        
        subprocess.run(command, shell=True)

    except KeyboardInterrupt:
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "ctrlC"])}')

