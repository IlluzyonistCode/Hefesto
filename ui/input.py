import sys

from ui.colors import paint
from ui.display import print_banner
from core.config_manager import JsonManager
from ui.menu import commands
from utils.network import GetUtilities
from utils.validation import CheckUtilities
from utils.argument_checker import ArgumentChecker


class CommandInput():
    @staticmethod
    def command_input(api_process):
        version = JsonManager.get('currentVersion')
        bot = '✔️' if JsonManager.get(['minecraftServerOptions', 'checkServerLoginWithABot']) else '❌'
        proxy = '✔️' if JsonManager.get(['minecraftServerOptions', 'proxy']) else '❌'

        print_banner('menu', GetUtilities.get_translated_text(['banners', 'menu', 'message1']), GetUtilities.get_translated_text(['banners', 'menu', 'message2']), version, bot, proxy)
            
        while True:
            try:
                paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["input"])}', end='')
                arguments = input().split()

                if len(arguments) > 0:
                    command = arguments[0].lower()

                    if command not in commands:
                        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["invalidCommand"])}')

                    if command in commands and ArgumentChecker.check_arguments(command, arguments):
                        commands[command](*arguments[1:])


            except (RuntimeError, EOFError):
                pass

            except KeyboardInterrupt:
                if api_process is not None:
                    api_process.terminate()
                    
                sys.exit()
