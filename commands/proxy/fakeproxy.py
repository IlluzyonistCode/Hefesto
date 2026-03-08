from ui.colors import paint
from modules.minecraft.launcher import ProxyLauncher
from utils.network import GetUtilities


def fakeproxy_command(target, mode, *args):
    

    try:
        if mode.lower() not in ['none', 'legacy', 'bungeeguard', 'modern']:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "invalidArguments", "invalidForwardingMode"])}')
            return
        
        ProxyLauncher.start_proxy('fakeproxy', target, mode)

    except KeyboardInterrupt:
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "ctrlC"])}')

