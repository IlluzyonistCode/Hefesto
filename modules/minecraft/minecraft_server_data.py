import httpx
import hashlib
import uuid
import dns
import asyncio
import subprocess
import re

from json import JSONDecodeError

from modules.minecraft.status.status_response import JavaStatusResponse, BedrockStatusResponse
from core.config_manager import JsonManager
from modules.minecraft.ping_as_java_and_bedrock_in_one_time import status
from utils.network import GetUtilities


class JavaServerData:
    def __init__(self, platform_type, ip_port, motd, version, protocol, connected_players, max_player_limit, player_list, default_player_list, favicon, mod_type, mod_list, latency, bot_response):
        self.platform_type = platform_type
        self.ip_port = ip_port
        self.motd = motd
        self.version = version
        self.protocol = protocol
        self.connected_players = connected_players
        self.max_player_limit = max_player_limit
        self.player_list = player_list
        self.default_player_list = default_player_list
        self.favicon = favicon
        self.mod_type = mod_type
        self.mod_list = mod_list
        self.latency = latency
        self.bot_response = bot_response


class BedrockServerData:
    def __init__(self, platform_type, ip_port, motd, version, protocol, brand, connected_players, max_player_limit, map, gamemode, latency, bot_response):
        self.platform_type = platform_type
        self.ip_port = ip_port
        self.motd = motd
        self.version = version
        self.protocol = protocol
        self.brand = brand
        self.connected_players = connected_players
        self.max_player_limit = max_player_limit
        self.map = map
        self.gamemode = gamemode
        self.latency = latency
        self.bot_response = bot_response


class MinecraftServerData:
    @staticmethod
    async def get_server_data(server, bot, clean_data):
        

        if ':' not in server:
            ip_address = await MinecraftServerData.get_minecraft_ip_address(server)
            port = await MinecraftServerData.get_minecraft_server_port(server)

            if port is not None:
                server = f'{ip_address}:{port}'
            else:
                server = ip_address

        response = await status(server)

        if response is None:
            return None
        
        if isinstance(response, JavaStatusResponse):
            server = server if ':' in server else f'{server}:25565'

            if bot:
                if JsonManager.get(['minecraftServerOptions', 'checkServerLoginWithABot']):
                    bot_response = await MinecraftServerData.get_bot_response(server, response.version.protocol)

                else:
                    bot_response = None

            else:
                bot_response = None

            if type(response.description) != str:
                response.description = response.description.raw

            if clean_data:
                motd = await MinecraftServerData.__clean_data(response.description)
                version = await MinecraftServerData.__clean_data(response.version.name)
                bot_response = await MinecraftServerData.__clean_data(bot_response)

            else:
                motd = response.description
                version = response.version.name

            return JavaServerData(
                'Java',
                server,
                motd,
                version,
                response.version.protocol,
                response.players.online,
                response.players.max,
                await MinecraftServerData.get_clean_list_player_names(response.players.sample),
                response.players.sample,
                response.favicon,
                response.raw.get('modinfo', {}).get('type'),
                response.raw.get('modinfo', {}).get('modList', []),
                response.latency,
                bot_response
            )
        
        elif isinstance(response, BedrockStatusResponse):
            server = server if ':' in server else f'{server}:19132'

            
            
            bot_response = '&cNot compatible with Bedrock'

            if type(response.motd) != str:
                response.motd = response.motd.raw

            if clean_data:
                motd = await MinecraftServerData.__clean_data(response.motd)
                bot_response = await MinecraftServerData.__clean_data(bot_response)

            else:
                motd = response.motd
            
            return BedrockServerData(
                'Bedrock',
                server,
                motd,
                response.version.version,
                response.version.protocol,
                response.version.brand,
                response.players_online,
                response.players_max,
                response.map,
                response.gamemode,
                response.latency,
                bot_response
            )
        
        else:
            return None
        
    @staticmethod
    async def get_minecraft_server_port(server):
        
        
        hostname = f'_minecraft._tcp.{server}'

        try:
            answers = dns.resolver.resolve(hostname, 'SRV')
            
            server = answers[0].target
            port = answers[0].port

            return port

        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers, dns.exception.Timeout):
            return None
        
    @staticmethod
    async def get_minecraft_ip_address(server):
        
        
        ip_addresses = await MinecraftServerData.get_dns_records(server, 'A')
        
        if ip_addresses is not None and len(ip_addresses) >= 1:
            return ip_addresses[0]
        
    @staticmethod
    async def get_clean_list_player_names(player_list):
        

        if player_list is not None:
            texts_with_spaces = 0

            for player in player_list:
                if ' ' in player.name:
                    texts_with_spaces += 1

            if texts_with_spaces >= 3:
                players = str([f'{player.name}' for player in player_list])
                players = players.replace('[', '').replace(']', '').replace("'", '').replace(
                    "&f&l(&500000000-0000-0000-0000-000000000000&f&l), ", '').replace(
                    "&f&l(&500000000-0000-0000-0000-000000000000&f&l)", '').replace(', ', ' ')

            else:
                players = str([f'&f&l{player.name} &f&l({await MinecraftServerData.get_uuid_color(player.name, player.id)}{player.id}&f&l)' for player in player_list])
                players = players.replace('[', '').replace(']', '').replace("'", '').replace(
                    "&f&l(&500000000-0000-0000-0000-000000000000&f&l), ", '').replace(
                    "&f&l(&500000000-0000-0000-0000-000000000000&f&l)", '')

            re.findall(
                r'[0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z]'
                r'[0-9a-z][0-9a-z][0-9a-z][0-9a-z]'
                r'[0-9a-z][0-9a-z][0-9a-z][0-9a-z]'
                r'[0-9a-z][0-9a-z][0-9a-z][0-9a-z]'
                r'[0-9a-z][0-9a-z][0-9a-z][0-9a-z]'
                r'[0-9a-z][0-9a-z][0-9a-z][0-9a-z]'
                r'[0-9a-z][0-9a-z][0-9a-z][0-9a-z]'
                r'[0-9a-z][0-9a-z][0-9a-z][0-9a-z]'
                r'[0-9a-z][0-9a-z][0-9a-z][0-9a-z]',
                players
            )

            return players

        return None
    
    @staticmethod
    async def get_player_uuid(username):
        

        api = 'https://api.mojang.com/users/profiles/minecraft/'

        try:
            async with httpx.AsyncClient() as session:
                async with session.get(f'{api}{username}') as response:
                    response_json = await response.json()

                    online_uuid = response_json['id']
                    online_uuid = f'{online_uuid[0:8]}-{online_uuid[8:12]}-{online_uuid[12:16]}-{online_uuid[16:20]}-{online_uuid[20:32]}'

                    offline_uuid = str(uuid.UUID(bytes=hashlib.md5(bytes(f'OfflinePlayer:{username}', 'utf-8')).digest()[:16], version=3))

                    return online_uuid, offline_uuid

        except (JSONDecodeError, KeyError):
            offline_uuid = str(uuid.UUID(bytes=hashlib.md5(bytes(f'OfflinePlayer:{username}', 'utf-8')).digest()[:16], version=3))
            return None, offline_uuid

        
    @staticmethod
    async def get_uuid_color(username, uuid):
        

        online_uuid, offline_uuid = await MinecraftServerData.get_player_uuid(username)

        if uuid == online_uuid:
            return '&a'
            
        elif uuid == offline_uuid:
            return '&7'
            
        else:
            return '&5'
        
    @staticmethod
    async def get_bot_response(ip_port, protocol):
        

        try:
            ip, port = ip_port.split(':')

        except ValueError:
            return 'Error'

        if JsonManager.get(["minecraftServerOptions", "proxy"]):
            command = f'node assets/scripts/checker.js {ip} {port} {protocol} {len(GetUtilities.get_spaces())} {JsonManager.get(["minecraftServerOptions", "proxyFileForTheBot"])}'

        else:
            command = f'node assets/scripts/checker.js {ip} {port} {protocol} {len(GetUtilities.get_spaces())}'

        proxy_file = None

        if proxy_file is not None:
            command += f' {proxy_file}'

        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()
            
        if stderr:
            error_message = stderr.decode('utf-8')

            if 'Error: Cannot find module' in error_message:
                return 'Error (Missing NodeJS modules!)'
            
            elif 'not found' in error_message or '"node"' in error_message:
                return 'Error (NodeJS is not installed)'
            
            else:
                return 'Error'
            
        else:
            output = stdout.decode('utf-8').replace('\n', '')
            output = re.sub(' +', ' ', output)
            output = MinecraftServerData.improve_bot_response(output)
            return output
        
    def get_bot_response_sync(ip_port, protocol):
        

        try:
            ip, port = ip_port.split(':')

        except ValueError:
            return 'Error'

        if JsonManager.get(["minecraftServerOptions", "proxy"]):
            command = f'node assets/scripts/checker.js {ip} {port} {protocol} {len(GetUtilities.get_spaces())} {JsonManager.get(["minecraftServerOptions", "proxyFileForTheBot"])}'

        else:
            command = f'node assets/scripts/checker.js {ip} {port} {protocol} {len(GetUtilities.get_spaces())}'

        proxy_file = None

        if proxy_file is not None:
            command += f' {proxy_file}'

        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        stdout, stderr = process.communicate()

        if stderr:
            error_message = stderr.decode('utf-8')

            if 'Error: Cannot find module' in error_message:
                return 'Error (Missing NodeJS modules!)'
            
            elif 'not found' in error_message or '"node"' in error_message:
                return 'Error (NodeJS is not installed)'
            
            else:
                return 'Error'

        else:
            output = stdout.decode('utf-8').replace('\n', '')
            output = re.sub(' +', ' ', output)
            output = MinecraftServerData.improve_bot_response(output)
            return output
        
    @staticmethod
    async def get_dns_records(hostname, record_type='All'):
        

        try:
            records_list = []
            
            records = dns.resolver.resolve(hostname, record_type)

            for record in records:
                records_list.append(record.to_text())

            return records_list

        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers, dns.exception.Timeout):
            return None
        
    @staticmethod
    def improve_bot_response(bot_response):
        

        messages = {
            'http//Minecraft.netMinecraft.net': 'http//Minecraft.net',
            'multiplayer.disconnect.invalid_public_key_signature': '§cInvalid signature for profile public key',
            'multiplayer.disconnect.banned_ip.reasonwith': '§cYou are IP banned for the following reason',
            'multiplayer.disconnect.banned.reasonwith': '§cYou are banned for the following reason',
            'multiplayer.disconnect.incompatiblewith': '§cIncompatible versions',
            'multiplayer.disconnect.unverified_username': '§6Premium Server',
            'multiplayer.disconnect.not_whitelisted': '§bWhitelist',
            'multiplayer.disconnect.incompatible': '§cVersion Incompatible',
            'This server has mods that require FML/Forge to be installed on the client. Contact your server admin for more details.': '§dForge Server',
            'This server has mods that require Forge to be installed on the client. Contact your server admin for more details.': '§dForge Server',
            'If you wish to use IP forwarding, please enable it in your BungeeCord config as well!': '§cVulnerable to Bungee Exploit',
            'Unable to authenticate - no data was forwarded by the proxy.': '&cBungeeguard',
            'You are not whitelisted on this server!': '§bWhitelist',
            'You have to join through the proxy.': '&cIPWhitelist',
            'Not authenticated with Minecraft.net': '§6Premium Server',
            'disconnect.genericReasonwith': '§c',
        }

        for message, replacement in messages.items():
            bot_response = bot_response.replace(message, replacement)
        
        return bot_response

    @staticmethod
    async def __clean_data(data):
        

        if data is not None:
            data = str(data).replace('\n', '')

            data = re.sub(' +', ' ', data)
            return data
        
        return None
