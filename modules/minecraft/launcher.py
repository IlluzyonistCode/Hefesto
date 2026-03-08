import subprocess
import datetime
import time

from modules.minecraft.fakeproxy import FakeProxy
from ui.colors import paint
from core.config_manager import JsonManager
from utils.files import FileUtilities
from utils.network import GetUtilities
from utils.validation import CheckUtilities
from modules.minecraft.get_minecraft_server_data import GetMinecraftServerData
from utils.log_manager import LogManager


class ProxyLauncher:
    @staticmethod
    def start_proxy(proxy_type, address, velocity_mode=None):
        

        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file = ''
        
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["proxyMessages", "configuring"])}')
        time.sleep(0.5)
        
        server_data = GetMinecraftServerData.get_data(address, bot=False, clean_data=False)

        if server_data is None:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "invalidArguments", "invalidServer"])}')
            return None
        
        if JsonManager.get(["proxyConfig", "convertDomainToIP"]):
            address = server_data['ip_port']

        proxy_config_path = f'./assets/proxy/settings/{proxy_type}.config'

        with open(proxy_config_path, 'r', encoding='utf8') as f:
            proxy_config = f.read()

        proxy_config, proxy_port = ProxyLauncher.replace_proxy_variables(proxy_type, proxy_config, address, velocity_mode)

        if proxy_type in ['velocity', 'fakeproxy']:
            if JsonManager.get('logs'):
                log_file = LogManager.create_log_file(proxy_type)

                if proxy_type == 'velocity':
                    LogManager.write_log(log_file, 'fakeproxy', f'{current_time} Target: {address}\n')

                else:
                    LogManager.write_log(log_file, 'fakeproxy', f'{current_time} Target: {address} (Forwading mode: {velocity_mode})\n')

            FileUtilities.write_file(f'./assets/proxy/jar/{proxy_type}/velocity.toml', proxy_config, 'w+', True)

            if proxy_type == 'fakeproxy':
                if FakeProxy.setup(address) is False:
                    return None

            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["proxyMessages", "starting"])}')

            subprocess.Popen(f'cd ./assets/proxy/jar/{proxy_type} && {JsonManager.get(["proxyConfig", "velocityCommand"])}', stdout=subprocess.PIPE, shell=True)

        else:
            if JsonManager.get('logs'):
                log_file = LogManager.create_log_file('waterfall')
                LogManager.write_log(log_file, 'waterfall', f'{current_time} Target: {address}\n')

            FileUtilities.write_file(f'./assets/proxy/jar/{proxy_type}/config.yml', proxy_config, 'w+', True)

            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["proxyMessages", "starting"])}')

            subprocess.Popen(f'cd ./assets/proxy/jar/{proxy_type} && {JsonManager.get(["proxyConfig", "waterfallCommand"])}', stdout=subprocess.PIPE, shell=True)
        
        time.sleep(5)

        if not CheckUtilities.check_local_port(int(proxy_port)):
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["proxyMessages", "proxyServerNotStartup"])}')
            return
        
        if proxy_type == 'fakeproxy':
            if GetUtilities.get_ip_ngrok() is not None:
                paint(f"""\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["proxyMessages", "proxyServerStarted"]).replace("[0]", f"127.0.0.1:{proxy_port} &f&l(&d{GetUtilities.get_ip_ngrok()}&f&l)")}""")
            
            else:
                paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "fakeproxy", "ipNgrokError"])}')
                paint(f"""\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["proxyMessages", "proxyServerStarted"]).replace("[0]", f"127.0.0.1:{proxy_port}")}""")
        
        else:
            paint(f"""\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["proxyMessages", "proxyServerStarted"]).replace("[0]", f"127.0.0.1:{proxy_port}")}""")

        if proxy_type == 'fakeproxy':
            FakeProxy.show_data(address, log_file)

        else:
            while True:
                time.sleep(1)
    
    @staticmethod
    def replace_proxy_variables(proxy_type, proxy_config, address, velocity_mode):
        
        
        if '[[ADDRESS]]' in proxy_config:
            proxy_config = proxy_config.replace('[[ADDRESS]]', address)

        if '[[PORT]]' in proxy_config:
            if proxy_type == 'fakeproxy':
                port = JsonManager.get(['proxyConfig', 'fakeProxyPort'])

            elif proxy_type == 'velocity':
                port = JsonManager.get(['proxyConfig', 'velocityPort'])
                
            else:
                port = JsonManager.get(['proxyConfig', 'waterfallPort'])

            proxy_config = proxy_config.replace('[[PORT]]', port)

        else:
            port = "2"

        if '[[MODE]]' in proxy_config:
            proxy_config = proxy_config.replace('[[MODE]]', velocity_mode)

        return proxy_config, port
