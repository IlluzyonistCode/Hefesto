import random
import re
import requests

from ui.colors import paint
from utils.network import GetUtilities
from core.config_manager import JsonManager
from utils.log_manager import LogManager
from modules.minecraft.show_minecraft_server import show_server
from modules.minecraft.get_minecraft_server_data import GetMinecraftServerData


def websearch_command(tag, *args):
    

    servers = []
    servers_found = 0

    log_file = LogManager.create_log_file('websearch')

    urls = {
        'https=".*?"><span>(.*?)</span>',
        'https="icon ip"></span>(.*?)</p>',
        'https)</strong></button>',
    }

    headers_list = GetUtilities.get_headers()
    cookies = {'cookie_name': 'cookie_value'}

    invalid_words = ['playing now', 'Copy IP', '#']

    paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "websearch", "searching"]).replace("[0]", tag)}')

    try:
        for url in urls.items():
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "websearch", "webSearch"]).replace("[0]", url[0])}')

            for num in range(1, 500):
                page = url[0]

                if page == 'https://minecraft-mp.com':
                    page = f'{page}/type/{tag.lower()}'
                    page = f'{page}/{num}/'

                elif page == 'https://servers-minecraft.net':
                    page = f'{page}/minecraft-{tag.lower()}-servers'
                    page = f'{page}/pg.{num}'

                elif page == 'https://minecraftservers.org':
                    page = f'{page}/search/{tag}'
                    page = f'{page}/{num}'

                try:
                    headers = headers_list[random.randint(0, len(headers_list) - 1)]
                    text = requests.get(page, headers=headers, cookies=cookies, timeout=5).text

                except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
                    break

                if 'https://minecraft-mp.com/' in page:
                    if '<h1>Minecraft Servers By Types</h1>' in text:
                        break

                    if not ', page' in text and num > 1:
                        break

                if 'https://minecraftservers.org' in page:
                    if '<p>Found 0 servers</p>' in text:
                        break

                    if '<title>404 Page Not Found | Minecraft Servers' in text:
                        break

                if 'https://servers-minecraft.net' in page:
                    if '<span>No Servers</span>' in text:
                        break

                server_list = re.findall(url[1], text)

                for server in server_list:
                    if server not in servers:
                        for word in invalid_words:
                            if word in server:
                                break

                        else:
                            servers.append(server)

                continue

        if not servers:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "websearch", "serversNotFound"])}')
            return

        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "websearch", "checkingServers"]).replace("[0]", str(len(servers)))}')

        for server in servers:
            server_data = GetMinecraftServerData.get_data(server)

            if server_data is not None:
                show_server(server_data)
                servers_found += 1

                if JsonManager.get('logs'):
                    log_data = list(server_data.values())
                    LogManager.write_log(log_file, 'websearch', log_data)
        
        if servers_found >= 1:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "serversFound"]).replace("[0]", str(servers_found))}')

        else:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "serversNotFound"])}')
                    
    except KeyboardInterrupt:
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "ctrlC"])}')

