from modules.minecraft.rcon.mcrcon import MCRcon, MCRconException

from ui.colors import paint
from ui.mccolor import mcreplace
from utils.network import GetUtilities
from utils.validation import CheckUtilities


def rcon_command(server, password, *args):
    

    try:
        if not CheckUtilities.check_ip_port(server):
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "invalidArguments", "InvalidRconFormat"])}')
            return
        
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "rcon", "connecting"])}')
        
        server = server.split(':')
        mcr = None

        with MCRcon(server[0], password, int(server[1]), timeout=35) as mcr:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "rcon", "establishedConnection"])}\n')
            
            while True:
                paint(f'{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "rcon", "command"])}', '')
                command = input()

                if command == '.exit':
                    paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "rcon", "stopping"])}')
                    mcr.disconnect()
                    return

                resp = mcr.command(command)
                resp = mcreplace(resp)
                paint(f'\n{GetUtilities.get_spaces()}{resp}')

    except TimeoutError:
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "rcon", "timeout"])}')

    except ConnectionRefusedError:
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "rcon", "connectionRefused"])}')

    except MCRconException:
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "invalidArguments", "invalidRconPassword"])}')
    
    except KeyboardInterrupt:
        if mcr is not None:
            mcr.disconnect()

        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "ctrlC"])}')

    except Exception as e:
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "rcon", "error"]).replace("[0]", str(e))}')

