import subprocess
import time
import os

from ui.colors import paint
from modules.minecraft.get_minecraft_server_data import GetMinecraftServerData
from core.config_manager import JsonManager
from utils.network import GetUtilities 
from utils.validation import CheckUtilities


def sendcmd_command(server, username, version, command_file, loop, *args):
    

    try:
        if not os.path.exists(command_file):
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "invalidArguments", "invalidFile"]).replace("[0]", command_file)}')
            return
        
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

        server = server_data['ip_port']
        ip, port = server.split(':')

        with open(command_file, 'r', encoding=CheckUtilities.check_file_encoding(command_file)) as f:
            commands = f.readlines()

        if len(commands) == 0:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "sendcmd", "emptyFile"])}')
            return
        
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "sendcmd", "startingTheAttack"])}')
        
        if JsonManager.get(["minecraftServerOptions", "proxy"]):
            command = f'{JsonManager.get(["minecraftServerOptions", "nodeCommand"])} ./hefesto_files/scripts/sendcmd.js {ip} {port} {username} {version} {command_file} {len(GetUtilities.get_spaces())} {JsonManager.get(["minecraftServerOptions", "proxyFileForTheBot"])}'

        else:
            command = f'{JsonManager.get(["minecraftServerOptions", "nodeCommand"])} ./hefesto_files/scripts/sendcmd.js {ip} {port} {username} {version} {command_file} {len(GetUtilities.get_spaces())}'
        
        while loop:
            time.sleep(4)
            subprocess.run(command, shell=True)

        if not loop:
            subprocess.run(command, shell=True)

    except KeyboardInterrupt:
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "ctrlC"])}')

