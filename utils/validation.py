import subprocess
import socket
import os

from core.config_manager import JsonManager


class CheckUtilities:
    
    @staticmethod
    def check_local_port(port):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        result = s.connect_ex(('127.0.0.1', port))
        s.close()
            
        if result == 0:
            return True
            
        return False
    
    
    @staticmethod
    def check_ngrok():

        if subprocess.call(f'{JsonManager.get(["proxyConfig", "ngrokCommand"])} version >nul 2>&1', shell=True) != 0:
            return False
        
        return True
    
    def check_ip_address(ip_address):
        

        try:
            socket.inet_pton(socket.AF_INET, ip_address)
            return True

        except socket.error:
            return False
        
    def check_scan_method(method):
        

        methods = ['nmap', 'qubo', 'quboscanner', 'masscan', '0', '1', '2']

        if method in methods:
            return True

        return False
    
    def check_nmap():
        

        if subprocess.call(f'nmap --version >nul 2>&1', shell=True) != 0:
            return False
        
        return True
    
    def check_masscan():
        

        if subprocess.call(f'masscan --version >nul 2>&1', shell=True) != 0:
            return False

        return True
        
    def check_file_encoding(file):
        

        try:
            with open(file, 'r+', encoding='utf8') as f:
                f.read()

            return 'utf8'

        except (UnicodeError, UnicodeDecodeError, UnicodeEncodeError, LookupError):
            return 'unicode_escape'
        
    def check_loop_argument(argument):
        

        valid_arguments = ['yes', 'y', 'no', 'n']

        if argument in valid_arguments:
            return True

        return False
    
    def check_ip(ip_address):
        

        try:
            socket.inet_pton(socket.AF_INET, ip_address)
            return True

        except socket.error:
            return False
    
    def check_port(port):
        

        try:
            if int(port) <= 65535:
                return True

            return False

        except ValueError:
            return False
        
    def check_ip_port(ip_port):
        

        if ':' in ip_port:
            ip_port = ip_port.split(':')

            if CheckUtilities.check_ip(ip_port[0]):
                if CheckUtilities.check_port(ip_port[1]):
                    try:
                        _ = ip_port[2]
                        return False

                    except IndexError:
                        return True
                    
        return False

