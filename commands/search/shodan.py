import shodan
import requests
import json

from ui.colors import paint
from core.config_manager import JsonManager
from utils.network import GetUtilities
from modules.minecraft.show_minecraft_server import show_server
from modules.minecraft.get_minecraft_server_data import GetMinecraftServerData
from utils.log_manager import LogManager


def shodan_command(*data):
    
    
    server_list = []
    servers_found = 0

    if JsonManager.get(['shodanApiKey']) == '':
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "error"])}{GetUtilities.get_translated_text(["shodanInvalidApiKey"])}')
        return

    data = ' '.join(str(i) for i in data)

    data = data.split(' --- ')

    try:
        search = shodan.Shodan(JsonManager.get(['shodanApiKey']))
        all_data = ''

        for i in data:
            all_data = f'{all_data}{i} '
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "shodan", "scanning"])} &a{i}')
            servers = search.search(i)

            for server in servers['matches']:
                server_list.append(f'{str(server["ip_str"])}:{str(server["port"])}')

        if len(server_list) >= 1:
            server_list = list(set(server_list))
            message_found_ips = str(GetUtilities.get_translated_text(["commands", "shodan", "ipsFound"])).replace('[0]', str(len(server_list))).replace('[1]', all_data[:-1])
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{message_found_ips}')
            log_file = LogManager.create_log_file('shodan')

        else:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "shodan", "serversNotFound"])} &f&l(&a{all_data[:-1]}&f&l)')
            return

        for server in server_list:
            server_data = GetMinecraftServerData.get_data(server)

            if server_data is not None:
                show_server(server_data)
                log_data = list(server_data.values())
                LogManager.write_log(log_file, 'shodan', log_data)
                servers_found += 1

        if servers_found >= 1:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "serversFound"]).replace("[0]", str(servers_found))}')

        else:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "serversNotFound"])}')

    except (json.decoder.JSONDecodeError, requests.exceptions.JSONDecodeError, KeyboardInterrupt):
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "ctrlC"])}')

    except shodan.exception.APIError as e:
        if 'Invalid API key' in str(e):
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "error"])}{GetUtilities.get_translated_text(["shodanInvalidApiKey"])}')

        elif 'Access denied' in str(e):
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "error"])}{GetUtilities.get_translated_text(["shodanApiKeyNoAccess"])}')

        else:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "error"])}&f&lThe connection to the Shodan API could not be established.')

