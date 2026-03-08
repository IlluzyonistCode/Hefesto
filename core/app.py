import multiprocessing
import subprocess
import threading
import time
import sys

from ui.display import print_banner
from core.updater import HefestoUpdater
from core.proxy_updater import ProxyUpdater
from ui.input import CommandInput
from core.config_manager import JsonManager
from utils.validation import CheckUtilities
from utils.network import GetUtilities
from modules.network.api import run_flask_app


class Startup():
    @staticmethod
    def run():


        if JsonManager.get('api') not in ['localhost', 'mcsrvstat.us', 'mcstatus.io']:
            settings = JsonManager.load_json('./config/config.json')
            settings['api'] = 'mcsrvstat.us'
            JsonManager.save_json(settings, './config/config.json')

        HefestoUpdater.show_banner_update()

        if JsonManager.get(['proxyConfig', 'updateProxy']):
            ProxyUpdater.update_proxies()


        api_process = None

        if JsonManager.get('api') == 'localhost':
            try:
                starting_api_banner_name = 'starting_api'
                print_banner(starting_api_banner_name)
                time.sleep(1)

                if not CheckUtilities.check_local_port(JsonManager.get('local_api_port')):
                    api_process = multiprocessing.Process(target=run_flask_app)
                    api_process.daemon = True
                    api_process.start()

            except KeyboardInterrupt:
                settings = JsonManager.load_json('./config/config.json')
                settings['api'] = 'mcsrvstat.us'
                JsonManager.save_json(settings, './config/config.json')
                api_process = None

        try:
            presentation_banner_name = 'presentation'
            print_banner(presentation_banner_name, GetUtilities.get_translated_text(['banners', 'presentation', 'message1']), GetUtilities.get_translated_text(['banners', 'presentation', 'message1']), GetUtilities.get_translated_text('credits'))
            time.sleep(2)

        except KeyboardInterrupt:
            pass

        CommandInput.command_input(api_process)

