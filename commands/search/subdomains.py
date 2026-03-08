import socket
import os

from ui.colors import paint
from utils.network import GetUtilities
from utils.log_manager import LogManager


def subdomains_command(domain, wordlist, *args):
    
    
    log_file = LogManager.create_log_file('subdomains')
    
    log_data = f'Domain: {domain}\n'

    try:
        if not os.path.exists(wordlist):
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "invalidArguments", "invalidFile"]).replace("[0]", wordlist)}')
            return
        
        subdomains = 0

        with open(wordlist, 'r', encoding='utf8') as f:
            subdomain_list = f.readlines()

        subdomain_list = [subdomain.strip() for subdomain in subdomain_list]
        
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "subdomains", "lookingForSubdomains"]).replace("[0]", domain)}')

        if len(subdomain_list) >= 1:
            paint('')

        for subdomain in subdomain_list:
            try:
                host = f'{subdomain}.{domain}'
                ip = socket.gethostbyname(host)
                
                paint(f'{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "subdomains", "found"]).replace("[0]", host).replace("[1]", ip)}')
                
                log_data += f'{host} ({ip})\n'
                
                subdomains += 1

            except socket.gaierror:
                continue

        if subdomains >= 1:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "subdomains", "subdomainsFound"]).replace("[0]", str(subdomains))}')
            log_data += '\n'
            
            LogManager.write_log(log_file, 'subdomains', log_data)

        else:
            paint(f'{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "subdomains", "subdomainsNotFound"])}')

    except KeyboardInterrupt:
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "ctrlC"])}')

    except (UnicodeError, PermissionError):
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "invalidArguments", "invalidFile"]).replace("[0]", wordlist)}')

