from ui.colors import paint
from modules.minecraft.launcher import ProxyLauncher
from utils.network import GetUtilities


def waterfall_command(target, *args):
    
    
    try:
        ProxyLauncher.start_proxy('waterfall', target)

    except KeyboardInterrupt:
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "ctrlC"])}')

