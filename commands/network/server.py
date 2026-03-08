from ui.colors import paint
from modules.minecraft.show_minecraft_server import show_server
from modules.minecraft.get_minecraft_server_data import GetMinecraftServerData
from utils.network import GetUtilities
from utils.log_manager import LogManager


def server_command(server, *args):
    

    try:
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "gettingDataFromServer"])}')
        server_data = GetMinecraftServerData.get_data(server)

        if server_data is not None:
            show_server(server_data)

            log_file = LogManager.create_log_file('server')

            log_data = list(server_data.values())
            LogManager.write_log(log_file, 'server', log_data)

        else:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "invalidArguments", "invalidServer"])}')

    except (KeyboardInterrupt):
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "ctrlC"])}')


