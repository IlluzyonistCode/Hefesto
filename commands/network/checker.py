import os
import re

from ui.colors import paint
from modules.minecraft.get_minecraft_server_data import GetMinecraftServerData
from core.config_manager import JsonManager
from utils.network import GetUtilities
from utils.validation import CheckUtilities
from modules.minecraft.show_minecraft_server import show_server
from utils.log_manager import LogManager


def checker_command(file, *args):
    
    
    try:
        servers_found = 0
        log_file = LogManager.create_log_file('checker')

        if not os.path.exists(file):
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "invalidArguments", "invalidFile"]).replace("[0]", file)}')
            return
        
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "checker", "checking"])}')

        with open(file, encoding=CheckUtilities.check_file_encoding(file)) as f:
            for line in f:
                servers = re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\d{1,5}', line)

                for server in servers:
                    server_data = GetMinecraftServerData.get_data(server)
                            
                    if server_data is not None:
                        show_server(server_data)
                        servers_found += 1

                        if JsonManager.get('logs'):
                            log_data = list(server_data.values())
                            LogManager.write_log(log_file, 'scan', log_data)

        if servers_found == 0:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "checker", "noServersInTheFile"])}')

        else:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "checker", "foundServers"]).replace("[0]", str(servers_found))}')

    except KeyboardInterrupt:
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "ctrlC"])}')

