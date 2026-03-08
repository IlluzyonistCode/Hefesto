import subprocess

from ui.colors import paint


def print_banner(name, *arguments):
    

    if 'discord' not in name and 'help' not in name:
        subprocess.run('clear || cls', shell=True)

    file = f'./data/banners/{name}.txt'

    with open(file, 'r', encoding='utf8') as f:
        banner = f.read()

    if arguments is not None:
        for num, argument in enumerate(arguments):
            banner = banner.replace(f'[{num}]', argument)

    paint(banner)
