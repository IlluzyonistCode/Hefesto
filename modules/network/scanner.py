import re
import subprocess
import os

from ui.colors import paint
from core.config_manager import JsonManager
from utils.log_manager import LogManager
from utils.network import GetUtilities
from utils.validation import CheckUtilities
from modules.minecraft.show_minecraft_server import show_server
from modules.minecraft.get_minecraft_server_data import GetMinecraftServerData


class Scanner:
    @staticmethod
    def scanner(target, port_range, scan_method):
        

        command = Scanner.get_command(scan_method)
        command = command.replace('[TARGET]', target).replace('[PORTS]', port_range)
        servers_found = 0
        show_output = False
        first_line = True

        if os.name != 'nt' and scan_method != 'quboscanner':
            command = f'sudo {command}'

        if JsonManager.get(["scannerOptions", "showScanOutput"]):
            show_output = True

        try:
            log_file = LogManager.create_log_file('scan')
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            text_to_search, pattern, invalid_ip_text, invalid_ports_text = Scanner.get_scan_params(scan_method)

            for line in process.stdout:
                output_line = line.decode('latin-1').strip()

                if first_line:
                    if scan_method == 'quboscanner':
                        if 'not found' in output_line or '"java"' in output_line:
                            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "scan", "javaNotInstalled"])}')
                            return
                                    
                    first_line = False

                if show_output:
                    print(output_line)

                if any(text in output_line for text in invalid_ip_text):
                    paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "invalidArguments", "invalidIP"]).replace("[0]", target)}')
                    return

                if any(text in output_line for text in invalid_ports_text):
                    paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "invalidArguments", "invalidPorts"]).replace("[0]", port_range)}')
                    return

                if text_to_search in output_line:
                    server = Scanner.extract_server_info(output_line, pattern, scan_method)
                    
                    if server:
                        server_data = GetMinecraftServerData.get_data(server)
                        
                        if server_data is not None:
                            show_server(server_data)
                            servers_found += 1

                            if JsonManager.get('logs'):
                                log_data = list(server_data.values())
                                LogManager.write_log(log_file, 'scan', log_data)

            process.wait()
            return servers_found

        except (KeyboardInterrupt, ValueError):
            try:
                process.terminate()

            except UnboundLocalError:
                pass

            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "ctrlC"])}')
            return servers_found

    @staticmethod
    def get_command(scan_method):
        return JsonManager.get(['scannerOptions', f'{scan_method}Command'])

    @staticmethod
    def get_scan_params(scan_method):
        scan_params = {
            'nmap': ('Discovered open port', r'open port (\d+)/\w+ on (\d+\.\d+\.\d+\.\d+)', ['Failed to resolve "'], ['Your port specifications are illegal.', 'Your port range']),
            'masscan': ('Discovered open port', r'open port (\d+)/\w+ on (\d+\.\d+\.\d+\.\d+)', ['ERROR: bad IP address/range:', 'unknown command-line parameter'], ['bad target port:']),
            'quboscanner': (')(', r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+\b', ['Invalid IP range.'], ['port is out of range', 'For input string:'])
        }

        return scan_params.get(scan_method, ('', '', [], []))

    @staticmethod
    def extract_server_info(output_line, pattern, scan_method):
        match = re.search(pattern, output_line)

        if match:
            if scan_method in ('nmap', 'masscan'):
                server = f'{match.group(2)}:{match.group(1)}'

            else:
                server = match.group(0)

            return server
