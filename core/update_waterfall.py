import os
import requests
import shutil

from utils.network import GetUtilities
from ui.colors import paint


def update_waterfall(url):
    

    temp_folder = 'hefesto_temp'
    os.makedirs(temp_folder, exist_ok=True)

    with open(f'{temp_folder}/waterfall.jar', 'wb') as f:
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["proxyMessages", "downloadingUpdate"])}')
        waterfall = requests.get(url)
        f.write(waterfall.content)

    os.remove('assets/proxy/jar/waterfall/waterfall.jar')
    shutil.copy('hefesto_temp/waterfall.jar', 'assets/proxy/jar/waterfall/waterfall.jar')
    os.remove('hefesto_temp/waterfall.jar')
    shutil.rmtree('hefesto_temp')
    paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["proxyMessages", "updateCompleted"]).replace("[0]", "waterfall")}')
