import requests
import time
import re

from core.config_manager import JsonManager
from modules.network.api import convert_server_data
from modules.minecraft.minecraft_server_data import JavaServerData, BedrockServerData, MinecraftServerData
from utils.validation import CheckUtilities
from utils.network import GetUtilities


class GetMinecraftServerData:
    @staticmethod
    def get_data(server, bot=True, clean_data=True):
        

        time.sleep(0.5)

        try:
            if JsonManager.get('api') == 'localhost':
                return GetMinecraftServerData.sort_dictionary(GetMinecraftServerData.get_data_via_local_API(server, bot, clean_data))

            elif JsonManager.get('api') == 'mcsrvstat.us':
                return GetMinecraftServerData.sort_dictionary(convert_server_data(GetMinecraftServerData.get_data_via_mcsrvstatus(server, bot, clean_data)))

            elif JsonManager.get('api') == 'mcstatus.io':
                return GetMinecraftServerData.sort_dictionary(convert_server_data(GetMinecraftServerData.get_data_via_mcstatusio(server, bot, clean_data)))

            else:
                return 'API_ERROR'
                
        except KeyboardInterrupt:
            return None
        
    @staticmethod
    def get_data_via_local_API(server, bot, clean_data):
        

        try:
            local_api_port = JsonManager.get('local_api_port')

            response = requests.get(f'http://127.0.0.1:{local_api_port}/api/minecraft_server_data',
                            params={'server_address': server, 'bot': bot, 'clean_data': clean_data})
                
            if response.status_code == 200:
                response = response.json()
                return response
            
            else:
                return None

        except KeyboardInterrupt:
            return None

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout,
                requests.exceptions.TooManyRedirects, requests.exceptions.RequestException,
                ConnectionError) as e:

            settings = JsonManager.load_json('./config/config.json')
            settings['api'] = 'mcsrvstat.us'
            JsonManager.save_json(settings, './config/config.json')
            return None

    @staticmethod
    def get_data_via_mcsrvstatus(server, bot, clean_data):
        

        try:
            response = requests.get(f'https://api.mcsrvstat.us/3/{server}')

            if response.status_code == 200 and response.json()['online']:
                r_json = response.json()

                motd = f'{r_json["motd"]["raw"][0]}\n{r_json["motd"]["raw"][1]}' if len(r_json["motd"]["raw"]) >= 2 else f'{r_json["motd"]["raw"][0]}'
                version = f'{r_json["version"]}'
                
                if clean_data:
                    motd = GetMinecraftServerData.clean_data(motd)
                    version =  GetMinecraftServerData.clean_data(version)

                if bot:
                    return JavaServerData(
                        'Java',
                        f'{r_json["ip"]}:{r_json["port"]}',
                        motd,
                        version,
                        r_json["protocol"]["version"] if 'protocol' in r_json else '47',
                        r_json["players"]["online"] if 'players' in r_json else '0',
                        r_json["players"]["max"] if 'players' in r_json else '0',
                        GetUtilities.get_clean_list_player_names(r_json["players"]["list"]) if "list" in r_json["players"] else None,
                        r_json["players"]["list"] if "list" in r_json["players"] else r_json["info"]["raw"] if "info" in r_json else None,
                        {r_json["icon"]} if 'icon' in r_json else None,
                        None,
                        [],
                        None,
                        MinecraftServerData.get_bot_response_sync(f'{r_json["ip"]}:{r_json["port"]}', f'{r_json["protocol"]["version"] if "protocol" in r_json else "47"} ')
                    )
                
                else:
                    return JavaServerData(
                        'Java',
                        f'{r_json["ip"]}:{r_json["port"]}',
                        motd,
                        version,
                        r_json["protocol"]["version"] if 'protocol' in r_json else '47',
                        r_json["players"]["online"] if 'players' in r_json else '0',
                        r_json["players"]["max"] if 'players' in r_json else '0',
                        GetUtilities.get_clean_list_player_names(r_json["players"]["list"]) if "list" in r_json["players"] else None,
                        r_json["players"]["list"] if "list" in r_json["players"] else r_json["info"]["raw"] if "info" in r_json else None,
                        {r_json["icon"]} if 'icon' in r_json else None,
                        None,
                        [],
                        None,
                        None
                    )
            
            else:
                response = requests.get(f'https://api.mcsrvstat.us/bedrock/3/{server}')

                if response.status_code == 200 and response.json()['online']:
                    r_json = response.json()
                    motd = f'{r_json["motd"]["raw"][0]} {r_json["motd"]["raw"][1]}' if len(r_json["motd"]["raw"]) >= 2 else f'{r_json["motd"]["raw"][0]}'
                    version = f'{r_json["version"]}'

                    if clean_data:
                        motd = GetMinecraftServerData.clean_data(motd)
                        version = GetMinecraftServerData.clean_data(version)

                    return BedrockServerData(
                        'Bedrock',
                        f'{r_json["ip"]}:{r_json["port"]}',
                        motd,
                        version,
                        r_json["protocol"]["version"],
                        r_json['software'] if 'software' in r_json else None,
                        r_json["players"]["online"],
                        r_json["players"]["max"],
                        r_json['map']['raw'] if 'map' in r_json else None,
                        r_json['gamemode'] if 'gamemode' in r_json else None,
                        None,
                        None,
                    )

        except KeyboardInterrupt:
            return None

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout,
                requests.exceptions.TooManyRedirects, requests.exceptions.RequestException,
                ConnectionError) as e:
            
            settings = JsonManager.load_json('./config/config.json')
            settings['api'] = 'mcstatus.io'
            JsonManager.save_json(settings, './config/config.json')
            return None
        

    @staticmethod
    def get_data_via_mcstatusio(server, bot, clean_data):
        

        try:
            response = requests.get(f'https://api.mcstatus.io/v2/status/java/{server}')

            if response.status_code == 200 and response.json()['online']:
                r_json = response.json()
                
                motd = r_json['motd']['raw']
                version = r_json["version"]['name_raw']
                
                if clean_data:
                    motd = GetMinecraftServerData.clean_data(motd)
                    version =  GetMinecraftServerData.clean_data(version)

                if bot:
                    return JavaServerData(
                        'Java',
                        f'{r_json["ip_address"]}:{r_json["port"]}',
                        motd,
                        version,
                        r_json["version"]["protocol"] if 'version' in r_json else '47',
                        r_json["players"]["online"] if 'players' in r_json else '0',
                        r_json["players"]["max"] if 'players' in r_json else '0',
                        GetUtilities.get_clean_list_player_names(r_json["players"]["list"]) if "list" in r_json["players"] else None,
                        r_json["players"]["list"] if "list" in r_json["players"] else r_json["info"]["raw"] if "info" in r_json else None,
                        {r_json["icon"]} if 'icon' in r_json else None,
                        None,
                        [],
                        None,
                        MinecraftServerData.get_bot_response_sync(f'{r_json["ip_address"]}:{r_json["port"]}', f'{r_json["version"]["protocol"] if "version" in r_json else "47"} ')
                    )
                
                else:
                    return JavaServerData(
                        'Java',
                        f'{r_json["ip_address"]}:{r_json["port"]}',
                        motd,
                        version,
                        r_json["version"]["protocol"] if 'version' in r_json else '47',
                        r_json["players"]["online"] if 'players' in r_json else '0',
                        r_json["players"]["max"] if 'players' in r_json else '0',
                        GetUtilities.get_clean_list_player_names(r_json["players"]["list"]) if "list" in r_json["players"] else None,
                        r_json["players"]["list"] if "list" in r_json["players"] else r_json["info"]["raw"] if "info" in r_json else None,
                        {r_json["icon"]} if 'icon' in r_json else None,
                        None,
                        [],
                        None,
                        None
                    )
            
            else:
                response = requests.get(f'https://api.mcstatus.io/v2/status/bedrock/{server}')

                if response.status_code == 200 and response.json()['online']:
                    r_json = response.json()
                
                    motd = r_json['motd']['raw']
                    version = r_json["version"]['name']

                    if clean_data:
                        motd = GetMinecraftServerData.clean_data(motd)
                        version = GetMinecraftServerData.clean_data(version)

                    return BedrockServerData(
                        'Bedrock',
                        f'{r_json["ip_address"]}:{r_json["port"]}',
                        motd,
                        version,
                        r_json["version"]["protocol"] if 'version' in r_json else '47',
                        r_json['software'] if 'software' in r_json else None,
                        r_json["players"]["online"],
                        r_json["players"]["max"],
                        r_json['map']['raw'] if 'map' in r_json else None,
                        r_json['gamemode'] if 'gamemode' in r_json else None,
                        None,
                        None,
                    )

        except KeyboardInterrupt:
            return None

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout,
                requests.exceptions.TooManyRedirects, requests.exceptions.RequestException,
                ConnectionError) as e:
            
            settings = JsonManager.load_json('./config/config.json')
            settings['api'] = 'mcsrvstat.us'
            JsonManager.save_json(settings, './config/config.json')
            return None
        
    @staticmethod
    def sort_dictionary(response):
        if response is not None:
            if response['platform_type'] == 'Java':
                key_order = ['platform_type', 'ip_port', 'motd', 'version', 'protocol', 'connected_players', 'max_player_limit', 'player_list', 'default_player_list', 'favicon', 'mod_type', 'mod_list', 'latency', 'bot_response']

            else:
                key_order = ['platform_type', 'ip_port', 'motd', 'version', 'protocol', 'brand', 'connected_players', 'max_player_limit', 'map', 'gamemode', 'latency', 'bot_response']

            return {key: response[key] for key in key_order}
        
        else:
            return None


    @staticmethod
    def clean_data(data):
        

        if type(data) != str:
            data = data.raw

        data = str(data).replace('\n', '')

        data = re.sub(' +', ' ', data)

        data = re.sub(r'§#[0-9A-Fa-f]{6}', '', data)
        
        return data
