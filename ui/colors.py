from colorama import Fore, init
from ui.mccolor import mcreplace

init()


def paint(text, end=None):
    

    text = mcreplace(text)

    try:
        if end is not None:
            print(f'{text}{Fore.RESET}', end=end)

        else:
            print(f'{text}{Fore.RESET}')

    except UnicodeEncodeError:
        pass
