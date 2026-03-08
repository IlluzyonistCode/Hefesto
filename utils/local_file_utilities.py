import os
import requests
import json


class LocalFileUtilities:
    url_and_paths = [
        ['./config/bruteforce_config.json', 'https://raw.githubusercontent.com/Corruptor/Hefesto/main/config/bruteforce_config.json'],
        ['./config/sendcmd_config.json', 'https://raw.githubusercontent.com/Corruptor/Hefesto/main/config/sendcmd_config.json'],
        ['./data/banners/help.txt', 'https://raw.githubusercontent.com/Corruptor/Hefesto/main/data/banners/help.txt'],
        ['./data/banners/menu.txt', 'https://raw.githubusercontent.com/Corruptor/Hefesto/main/data/banners/menu.txt'],
        ['./data/banners/pickaxe.txt', 'https://raw.githubusercontent.com/Corruptor/Hefesto/main/data/banners/pickaxe.txt'],
        ['./data/banners/presentation.txt', 'https://raw.githubusercontent.com/Corruptor/Hefesto/main/data/banners/presentation.txt'],
        ['./data/banners/proxy_update.txt', 'https://raw.githubusercontent.com/Corruptor/Hefesto/main/data/banners/proxy_update.txt'],
        ['./data/banners/starting_api.txt', 'https://raw.githubusercontent.com/Corruptor/Hefesto/main/data/banners/starting_api.txt'],
        ['./data/banners/update.txt', 'https://raw.githubusercontent.com/Corruptor/Hefesto/main/data/banners/update.txt'],
        ['./assets/proxy/server-icon.png', 'https://raw.githubusercontent.com/Corruptor/Hefesto/main/assets/proxy/server-icon.png'],
        ['./assets/proxy/settings/fakeproxy.config', 'https://raw.githubusercontent.com/Corruptor/Hefesto/main/assets/proxy/settings/fakeproxy.config'],
        ['./assets/proxy/settings/variables.txt', 'https://raw.githubusercontent.com/Corruptor/Hefesto/main/assets/proxy/settings/variables.txt'],
        ['./assets/proxy/settings/velocity.config', 'https://raw.githubusercontent.com/Corruptor/Hefesto/main/assets/proxy/settings/velocity.config'],
        ['./assets/proxy/settings/waterfall.config', 'https://raw.githubusercontent.com/Corruptor/Hefesto/main/assets/proxy/settings/waterfall.config'],
        ['./assets/proxy/jar/fakeproxy/Velocity.jar', 'https://raw.githubusercontent.com/Corruptor/Hefesto/main/assets/proxy/jar/fakeproxy/Velocity.jar'],
        ['./assets/proxy/jar/fakeproxy/forwarding.secret', 'https://raw.githubusercontent.com/Corruptor/Hefesto/main/assets/proxy/jar/fakeproxy/forwarding.secret'],
        ['./assets/proxy/jar/fakeproxy/velocity.toml', 'https://raw.githubusercontent.com/Corruptor/Hefesto/main/assets/proxy/jar/fakeproxy/velocity.toml'],
        ['./assets/proxy/jar/fakeproxy/server-icon.png', 'https://raw.githubusercontent.com/Corruptor/Hefesto/main/assets/proxy/jar/fakeproxy/server-icon.png'],
        ['./assets/proxy/jar/fakeproxy/plugins/RPoisoner-1.1-SNAPSHOT.jar', 'https://raw.githubusercontent.com/Corruptor/Hefesto/main/assets/proxy/jar/fakeproxy/plugins/RPoisoner-1.1-SNAPSHOT.jar'],
        ['./assets/proxy/jar/velocity/Velocity.jar', 'https://raw.githubusercontent.com/Corruptor/Hefesto/main/assets/proxy/jar/velocity/Velocity.jar'],
        ['./assets/proxy/jar/velocity/forwarding.secret', 'https://raw.githubusercontent.com/Corruptor/Hefesto/main/assets/proxy/jar/velocity/forwarding.secret'],
        ['./assets/proxy/jar/velocity/velocity.toml', 'https://raw.githubusercontent.com/Corruptor/Hefesto/main/assets/proxy/jar/velocity/velocity.toml'],
        ['./assets/proxy/jar/velocity/server-icon.png', 'https://raw.githubusercontent.com/Corruptor/Hefesto/main/assets/proxy/jar/velocity/server-icon.png'],
        ['./assets/proxy/jar/velocity/plugins/Hefesto-1.1-SNAPSHOT.jar', 'https://raw.githubusercontent.com/Corruptor/Hefesto/main/assets/proxy/jar/velocity/plugins/Hefesto-1.1-SNAPSHOT.jar'],
        ['./assets/proxy/jar/waterfall/waterfall.jar', 'https://raw.githubusercontent.com/Corruptor/Hefesto/main/assets/proxy/jar/waterfall/waterfall.jar'],
        ['./assets/proxy/jar/waterfall/config.yml', 'https://raw.githubusercontent.com/Corruptor/Hefesto/main/assets/proxy/jar/waterfall/config.yml'],
        ['./assets/proxy/jar/waterfall/server-icon.png', 'https://raw.githubusercontent.com/Corruptor/Hefesto/main/assets/proxy/jar/waterfall/server-icon.png'],
        ['./assets/proxy/jar/waterfall/plugins/RBungeeExploit-1.0.jar', 'https://raw.githubusercontent.com/Corruptor/Hefesto/main/assets/proxy/jar/waterfall/plugins/RBungeeExploit-1.0.jar'],
        ['./assets/scanner/old_qubo.jar', 'https://raw.githubusercontent.com/Corruptor/Hefesto/main/assets/scanner/old_qubo.jar'],
        ['./assets/scripts/checker.js', 'https://raw.githubusercontent.com/Corruptor/Hefesto/main/assets/scripts/checker.js'],
        ['./assets/scripts/connect.js', 'https://raw.githubusercontent.com/Corruptor/Hefesto/main/assets/scripts/connect.js'],
        ['./assets/scripts/kick.js', 'https://raw.githubusercontent.com/Corruptor/Hefesto/main/assets/scripts/kick.js'],
        ['./assets/scripts/login.js', 'https://raw.githubusercontent.com/Corruptor/Hefesto/main/assets/scripts/login.js'],
        ['./assets/scripts/pinlogin.js', 'https://raw.githubusercontent.com/Corruptor/Hefesto/main/assets/scripts/pinlogin.js'],
        ['./assets/scripts/sendcmd.js', 'https://raw.githubusercontent.com/Corruptor/Hefesto/main/assets/scripts/sendcmd.js'],
        ['./assets/scripts/utils.js', 'https://raw.githubusercontent.com/Corruptor/Hefesto/main/assets/scripts/utils.js'],
        ['./data/usernames.txt', 'https://raw.githubusercontent.com/Corruptor/Hefesto/main/data/usernames.txt'],
    ]

    @staticmethod
    def check_local_files():
        

        directories_to_create = [
            './data/',
            './config/',
            './data/banners/',
            './data/presence/',
            './assets/proxy/',
            './assets/proxy/settings/',
            './assets/proxy/jar/fakeproxy/plugins/',
            './assets/proxy/jar/velocity/plugins/',
            './assets/proxy/jar/waterfall/plugins/',
            './assets/scanner/',
            './assets/scripts/',
        ]

        for directory in directories_to_create:
            if not os.path.exists(directory):
                os.makedirs(directory)

        if not os.path.exists(f'./config/config.json'):
            data = {
                "api": "mcsrvstat.us",
                "local_api_port": 55455,
                "shodanApiKey": "",
                "virusTotalApiKey": "0a1f92cc877fb00875cf0fa6e856db8009fb322fce4b507a9ef40e22d63b7fa4",
                "minecraftServerOptions": {
                    "checkServerLoginWithABot": True,
                    "proxy": False,
                    "proxyFileForTheBot": "./proxy.txt",
                    "nodeCommand": "node"
                },
                "scannerOptions": {
                    "nmapCommand": "nmap -p [PORTS] -n -T5 -Pn -vvv -sS [TARGET]",
                    "quboscannerCommand": "cd ./assets/scanner && java -Dfile.encoding=UTF-8 -jar old_qubo.jar -range [TARGET] -ports [PORTS] -th 500 -ti 2000",
                    "masscanCommand": "masscan -p [PORTS] [TARGET]",
                    "showScanOutput": False
                },
                "proxyConfig": {
                    "convertDomainToIP": True,
                    "updateProxy": True,
                    "ngrokCommand": "ngrok",
                    "waterfallPort": "25570",
                    "waterfallCommand": "java -Xms512M -Xmx512M -jar WaterFall.jar >nul 2>&1",
                    "velocityPort": "25580",
                    "velocityCommand": "java -Xms512M -Xmx512M -jar Velocity.jar >nul 2>&1",
                    "fakeProxyPort": "33330",
                    "fakeProxyUpdateDelay": "2",
                    "fakeProxyCommandPrefix": ".",
                    "waterfallVersion": "https://api.papermc.io/v2/projects/waterfall/versions/1.20/builds/549/downloads/waterfall-1.20-549.jar",
                    "velocityVersion": "https://api.papermc.io/v2/projects/velocity/versions/3.2.0-SNAPSHOT/builds/294/downloads/velocity-3.2.0-SNAPSHOT-294.jar"
                },
                "logs": True,
                "currentVersion": "4.1.0"
            }

            with open(f'./config/config.json', 'w') as f:
                json.dump(data, f, indent=4)

        if not os.path.exists(f'./data/presence/richPresence.command'):
            with open(f'./data/presence/richPresence.command', 'w') as f:
                f.write('Help')

        if not os.path.exists(f'./data/presence/richPresence.status'):
            with open(f'./data/presence/richPresence.status', 'w') as f:
                f.write('True')

        for path, url in LocalFileUtilities.url_and_paths:
            if not os.path.exists(path):
                response = requests.get(url)

                if response.status_code == 200:
                    with open(path, 'wb') as f:
                        f.write(response.content)
