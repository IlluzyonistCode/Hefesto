from modules.network.scanner import Scanner
from ui.colors import paint
from utils.network import GetUtilities
from utils.validation import CheckUtilities


def scan_command(target, port_range, scan_method, *args):
    
    
    try:
        if not CheckUtilities.check_scan_method(scan_method):
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "invalidArguments", "invalidScanMethod"])}')
            return
                
        scan_method = GetUtilities.get_scan_method(scan_method)

        if scan_method == 'nmap' and CheckUtilities.check_nmap() is False:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "scan", "nmapNotInstalled"])}')
            return
        
        if scan_method == 'masscan' and CheckUtilities.check_masscan() is False:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "scan", "masscanNotInstalled"])}')
            return
        
        if target.endswith('.txt'):
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "scan", "scanningFile"])}')

        else:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "scan", "scanningIpAddress"]).replace("[0]", target)}')

        servers_found = Scanner.scanner(target, port_range, scan_method)

        if servers_found is not None:
            if servers_found >= 1:
                paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "scan", "scanFinished"]).replace("[0]", str(servers_found))}')

            else:
                paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "scan", "noPortsFound"])}')

    except (KeyboardInterrupt):
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "ctrlC"])}')

