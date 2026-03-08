import os
import requests
import shutil

from utils.network import GetUtilities
from ui.colors import paint


def update_velocity(url):
    

    temp_folder = 'hefesto_temp'
    os.makedirs(temp_folder, exist_ok=True)

    with open(f'{temp_folder}/Velocity.jar', 'wb') as f:
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["proxyMessages", "downloadingUpdate"])}')
        velocity = requests.get(url)
        f.write(velocity.content)

    os.remove('assets/proxy/jar/fakeproxy/Velocity.jar')
    os.remove('assets/proxy/jar/velocity/Velocity.jar')
    shutil.copy('hefesto_temp/Velocity.jar', 'assets/proxy/jar/fakeproxy/Velocity.jar')
    shutil.copy('hefesto_temp/Velocity.jar', 'assets/proxy/jar/velocity/Velocity.jar')
    os.remove('hefesto_temp/Velocity.jar')
    shutil.rmtree('hefesto_temp')
    paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["proxyMessages", "updateCompleted"]).replace("[0]", "Velocity")}')
