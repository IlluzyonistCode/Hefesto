from commands.utils.clear import clear_command
from commands.utils.help import help_command
from commands.network.server import server_command
from commands.utils.uuid import uuid_command
from commands.network.ipinfo import ipinfo_command
from commands.utils.dnsloookup import dnslookup
from commands.search.shodan import shodan_command
from commands.search.websearch import websearch_command
from commands.search.subdomains import subdomains_command
from commands.network.scan import scan_command
from commands.network.listening import listening_command
from commands.network.playerlogs import playerlogs_command
from commands.search.resolver import resolver_command
from commands.proxy.fakeproxy import fakeproxy_command
from commands.minecraft.login import login_command
from commands.minecraft.pinlogin import pinlogin_command
from commands.minecraft.sendcmd import sendcmd_command
from commands.minecraft.kick import kick_command
from commands.minecraft.kickall import kickall_command
from commands.minecraft.rconbrute import rconbrute
from commands.network.checker import checker_command
from commands.proxy.waterfall import waterfall_command
from commands.proxy.velocity import velocity_command
from commands.minecraft.connect import connect_command
from commands.minecraft.rcon import rcon_command

commands = {
    **dict.fromkeys(['cls', 'clear'], clear_command),
    **dict.fromkeys(['00', 'help'], help_command),
    **dict.fromkeys(['01', 'server'], server_command),
    **dict.fromkeys(['02', 'uuid'], uuid_command),
    **dict.fromkeys(['03', 'ipinfo'], ipinfo_command),
    **dict.fromkeys(['04', 'dnslookup'], dnslookup),
    **dict.fromkeys(['05', 'shodan'], shodan_command),
    **dict.fromkeys(['06', 'websearch'], websearch_command),
    **dict.fromkeys(['07', 'subdomains'], subdomains_command),
    **dict.fromkeys(['08', 'scan'], scan_command),
    **dict.fromkeys({'09', 'listening'}, listening_command),
    **dict.fromkeys(['10', 'playerlogs'], playerlogs_command),
    **dict.fromkeys(['10', 'resolver'], resolver_command),
    **dict.fromkeys(['12', 'fakeproxy'], fakeproxy_command),
    **dict.fromkeys(['13', 'login'], login_command),
    **dict.fromkeys(['14', 'pinlogin'], pinlogin_command),
    **dict.fromkeys(['15', 'sendcmd'], sendcmd_command),
    **dict.fromkeys(['16', 'kick'], kick_command),
    **dict.fromkeys(['17', 'kickall'], kickall_command),
    **dict.fromkeys(['18', 'rconbrute'], rconbrute),
    **dict.fromkeys(['19', 'checker'], checker_command),
    **dict.fromkeys(['20', 'waterfall'], waterfall_command),
    **dict.fromkeys(['21', 'velocity'], velocity_command),
    **dict.fromkeys(['22', 'connect'], connect_command),
    **dict.fromkeys(['23', 'rcon'], rcon_command),
}
