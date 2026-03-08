import subprocess
import time
import os
import sys

from core.app import Startup
from ui.display import print_banner
from utils.validation import CheckUtilities
from utils.local_file_utilities import LocalFileUtilities


if __name__ == '__main__':
    try:
        print('Downloading files necessary to use Hefesto...')
        LocalFileUtilities.check_local_files()

        pickaxe_banner_name = 'pickaxe'

        if os.name == 'nt':
            subprocess.run('title Hefesto / By @wrrulos', shell=True)

        print_banner(pickaxe_banner_name)
        time.sleep(1)

        Startup.run()

    except KeyboardInterrupt:
        sys.exit()
