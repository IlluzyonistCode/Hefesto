import dns
import socket
import requests
import hashlib
import uuid
import json
import re
import os

from json import JSONDecodeError

from core.config_manager import JsonManager
from utils.validation import CheckUtilities


class GetUtilities:
    cloudflare_ips = ['104.16.', '104.17.', '104.18.', '104.19.', '104.20.', '104.21.', '104.22.', '104.23.', '104.24.', '104.25.', '104.26.', '104.27.', '104.28.', '104.29.', '104.30.', '104.31.', '172.64.', '172.65.', '172.66.', '172.67.', '172.68.', '172.69.', '172.70.', '172.71.', '1.1.1.1']

    @staticmethod
    def get_spaces():
        
         
        return '    '
    

    @staticmethod
    def get_dns_records(hostname, record_type='All'):
        

        try:
            records_list = []
            records = dns.resolver.resolve(hostname, record_type)

            for record in records:
                records_list.append(record.to_text())

            return records_list

        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers, dns.exception.Timeout):
            return None
        
    @staticmethod
    def get_clean_list_player_names(player_list):
        
        
        texts_with_spaces = 0

        for player in player_list:
            if 'name' in player:
                username_variable = 'name'
                break

            elif 'name_clean' in player:
                username_variable = 'name_clean'
                break
 
        for player in player_list:
            if ' ' in player[username_variable]:
                texts_with_spaces += 1

        if texts_with_spaces >= 3:
            players = str([f'{player[username_variable]}' for player in player_list])
            players = players.replace('[', '').replace(']', '').replace("'", '').replace("&f&l(&500000000-0000-0000-0000-000000000000&f&l), ", '').replace("&f&l(&500000000-0000-0000-0000-000000000000&f&l)", '').replace(', ', ' ')

        else:
            players = str([f'&f&l{player[username_variable]} &f&l({GetUtilities.get_uuid_color(player[username_variable], player["uuid"])}{player["uuid"]}&f&l)' for player in player_list])
            players = players.replace('[', '').replace(']', '').replace("'", '').replace("&f&l(&500000000-0000-0000-0000-000000000000&f&l), ", '').replace("&f&l(&500000000-0000-0000-0000-000000000000&f&l)", '')

        re.findall(
            r'[0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z]-[0-9a-z][0-9a-z][0-9a-z][0-9a-z]-[0-9a-z][0-9a-z][0-9a-z][0-9a-z]-[0-9a-z][0-9a-z][0-9a-z][0-9a-z]-[0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z]',
             players
        )

        return players
    
    @staticmethod
    def get_player_uuid(username):
        

        api = 'https://api.mojang.com/users/profiles/minecraft/'

        try:
            r = requests.get(f'{api}{username}')
            r_json = r.json()

            online_uuid = r_json['id']
            online_uuid = f'{online_uuid[0:8]}-{online_uuid[8:12]}-{online_uuid[12:16]}-{online_uuid[16:20]}-{online_uuid[20:32]}'

            offline_uuid = str(uuid.UUID(bytes=hashlib.md5(bytes(f'OfflinePlayer:{username}', 'utf-8')).digest()[:16], version=3))

            return online_uuid, offline_uuid

        except (JSONDecodeError, KeyError):
            offline_uuid = str(uuid.UUID(bytes=hashlib.md5(bytes(f'OfflinePlayer:{username}', 'utf-8')).digest()[:16], version=3))
            return None, offline_uuid
        
    @staticmethod
    def get_uuid_color(username, uuid):
        

        online_uuid, offline_uuid = GetUtilities.get_player_uuid(username)

        if uuid == online_uuid:
            return '&a'
            
        elif uuid == offline_uuid:
            return '&7'
            
        else:
            return '&5'
        
    @staticmethod
    def get_subdomains_virustotal(domain):
        url = 'https://www.virustotal.com/vtapi/v2/domain/report'
        params = {'apikey': JsonManager.get('virusTotalApiKey'), 'domain':domain}
        domains = []
        ips = []

        try:
            response = requests.get(url, params=params)
            subdomains = sorted(response.json()['subdomains'])

        except (KeyError, ValueError):
            return None, None
        
        response = requests.get(f'https://api.hackertarget.com/hostsearch/?q={domain}')

        for line in response.iter_lines():
            line = str(line).split(',')

            if len(line) > 1:
                value = line[0].strip("'b")
                ip = line[1].strip("'b")

                if value != "API count exceeded - Increase Quota with Membership":
                    if ip not in ips:
                        ips.append(ip)

                    if [value, ip] not in domains:
                        domains.append([value, ip])

        for subdomain in subdomains:
            if subdomain not in [item[0] for item in domains]:
                try:
                    ip = socket.gethostbyname(subdomain)

                    if ip not in ips:
                        ips.append(ip)
                    
                    if [subdomain, ip] not in domains:
                        domains.append([subdomain, ip])

                except (socket.gaierror, socket.error):
                    pass

        return domains, ips
    
    @staticmethod
    def get_ms_color(ms):
        

        if '.' in str(ms):
            ms = str(ms).split('.')[0]

        if int(ms) <= 100:
            return f'&a{ms}'

        elif int(ms) <= 250:
            return f'&e{ms}'

        else:
            return f'&c{ms}'
        
    @staticmethod
    def get_ip_address(hostname):
        

        try:
            ip_address = socket.gethostbyname(str(hostname))
            return ip_address

        except socket.error:
            return None
        
    @staticmethod
    def get_ip_info(ip_address, reverse=True):
        

        r = requests.get(f'http://ip-api.com/json/{ip_address}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,timezone,isp,org,as,asname,reverse,query')
        r_json = r.json()
        domains = None

        if r_json['status'] == 'success':        
            if reverse:
                try:
                    domains = socket.gethostbyaddr(ip_address)[0]

                except socket.herror:
                    pass

            return (r_json, domains)
        
        return None
        
    @staticmethod
    def get_ip_ngrok():
        

        try:
            r = requests.get('http://localhost:4040/api/tunnels')
            r_json = r.json()
            domain = r_json['tunnels'][0]['public_url']
            _, _, domain = domain.partition('//')
            domain, port = domain.split(':')
            ip_address = f"{socket.gethostbyname(domain)}:{port}"
            return ip_address
        
        except (requests.exceptions.RequestException, json.JSONDecodeError, IndexError, socket.gaierror):
            return None
    
    @staticmethod
    def get_headers():
        

        headers_list = [
            {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'},
            {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; AS; rv:11.0) like Gecko'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; AS; rv:11.0) like Gecko'},
            {'User-Agent': 'Mozilla/5.0 (Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'},
            {'User-Agent': 'Mozilla/5.0 (Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0'},
            {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11.2; rv:78.0) Gecko/20100101 Firefox/78.0'},
            {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11.2; rv:85.0) Gecko/20100101 Firefox/85.0'},
            {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'},
            {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.63'},
            {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.68'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'},
            {'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'},
            {'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0'},
            {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:78.0) Gecko/20100101 Firefox/78.0'},
            {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:85.0) Gecko/20100101 Firefox/85.0'},
            {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'},
            {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:78.0) Gecko/20100101 Firefox/78.0'},
            {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:85.0) Gecko/20100101 Firefox/85.0'},
            {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'},
            {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0'}
        ]
        return headers_list
    
    def get_scan_method(method):
        

        if method == '0' or method == 'nmap':
            return 'nmap'

        if method == '1' or method == 'qubo' or method == 'quboscanner':
            return 'quboscanner'

        if method == '2' or method == 'masscan':
            return 'masscan'
        
    def get_loop_argument(argument):
        

        if argument == 'y' or argument == 'yes':
            return True

        return False
            
    @staticmethod
    def get_translated_text(text):
        
        from utils.text import EnglishText
        
        if isinstance(text, list):
            return EnglishText.get_text(text)
        else:
            return EnglishText.get_text([text])
    
    
    @staticmethod
    def get_separate_ips(ips):
        cloudflare = []
        unknowns_ip = []

        for ip in ips:
            is_cloudflare_ip = False
            for cf_ip in GetUtilities.cloudflare_ips:
                if ip.startswith(cf_ip):
                    is_cloudflare_ip = True
                    break

            if is_cloudflare_ip:
                cloudflare.append(ip)
            else:
                unknowns_ip.append(ip)

        return unknowns_ip, cloudflare
