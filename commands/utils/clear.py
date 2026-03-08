import subprocess

from core.config_manager import JsonManager
from ui.display import print_banner
from utils.validation import CheckUtilities
from utils.network import GetUtilities


def clear_command(*args):
    

    version = JsonManager.get('currentVersion')
    bot = '✔️' if JsonManager.get(['minecraftServerOptions', 'checkServerLoginWithABot']) else '❌'
    proxy = '✔️' if JsonManager.get(['minecraftServerOptions', 'proxy']) else '❌'

    subprocess.run('clear || cls', shell=True)

    print_banner('menu', GetUtilities.get_translated_text(['banners', 'menu', 'message1']), GetUtilities.get_translated_text(['banners', 'menu', 'message2']), version, bot, proxy)

