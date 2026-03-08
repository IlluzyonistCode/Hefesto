from ui.colors import paint
from utils.network import GetUtilities
from modules.minecraft.launcher import ProxyLauncher


def velocity_command(target, mode, *args):
    
    
    try:
        if mode.lower() not in ['none', 'legacy', 'bungeeguard', 'modern']:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "invalidArguments", "invalidForwardingMode"])}')
            return
        
        ProxyLauncher.start_proxy('velocity', target, mode)

    except KeyboardInterrupt:
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "ctrlC"])}')

