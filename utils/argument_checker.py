import os

from ui.colors import paint
from utils.network import GetUtilities


class ArgumentChecker:
    @staticmethod
    def check_arguments(command, arguments):
        

        commands = ArgumentChecker.get_command_indexes()

        if len(command) == 2:
            command = commands.get(command, command)

        if command in ['cls', 'clear']:
            return True

        if command in ['server', 'uuid', 'ipinfo', 'dnslookup', 'websearch', 'listening', 'playerlogs', 'resolver', 'checker', 'waterfall', 'shodan']:
            if ArgumentChecker.missing_arguments(command, 1, arguments):
                return False
            
        if command in ['subdomains', 'fakeproxy', 'rconbrute', 'velocity', 'rcon']:
            if ArgumentChecker.missing_arguments(command, 2, arguments):
                return False
            
        elif command in ['scan', 'connect', 'kickall']:
            if ArgumentChecker.missing_arguments(command, 3, arguments):
                return False
            
        elif command in ['login', 'pinlogin', 'kick']:
            if ArgumentChecker.missing_arguments(command, 4, arguments):
                return False
            
        elif command in ['sendcmd']:
            if ArgumentChecker.missing_arguments(command, 5, arguments):
                return False
            
        return True

    
    @staticmethod
    def missing_arguments(command, number_of_arguments, arguments):
        

        for i in range(1, int(number_of_arguments) + 1):
            try:
                arguments[i]

            except IndexError:
                missing_argument = GetUtilities.get_translated_text(['commands', command, f'argument{i}'])
                formatted_usage = f'{GetUtilities.get_translated_text(["commands", "commandUsage"])} {command} {" ".join(["&c" + arg if arg == missing_argument else "&7&l" + arg for arg in ArgumentChecker.get_command_arguments(command)])}'
                paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", command, f"missingArgument{str(i)}"])}')
                paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{formatted_usage}')
                return True
            
        return False

    @staticmethod
    def get_command_indexes():
        
        return {str(i).zfill(2): cmd for i, cmd in enumerate(['server', 'player', 'ipifo', 'dnslookup', 'shodan', 'websearch', 'subdomains', 'scan', 'listening', 'playerlogs', 'fakeproxy', 'login', 'pinlogin', 'sendcmd', 'kick', 'kickall', 'rconbrute', 'checker', 'waterfall', 'velocity', 'connect', 'rcon', 'config'], start=0)}
    
    @staticmethod
    def get_command_arguments(command):
        
        
        arguments = []

        for num in range(1, 11):
            if GetUtilities.get_translated_text(['commands', command, f'argument{num}']) is not None:
                arguments.append(GetUtilities.get_translated_text(['commands', command, f'argument{num}']))

        return arguments
