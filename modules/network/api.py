import asyncio

from flask import Flask, request, jsonify
from waitress import serve

from core.config_manager import JsonManager
from utils.network import GetUtilities
from modules.minecraft.minecraft_server_data import MinecraftServerData

app = Flask(__name__)


def convert_server_data(server_data):
    

    if server_data is None:
        return None

    if server_data.platform_type == 'Java':
        response = {
            'platform_type': server_data.platform_type,
            'ip_port': server_data.ip_port,
            'motd': server_data.motd,
            'version': server_data.version,
            'protocol': server_data.protocol,
            'connected_players': server_data.connected_players,
            'max_player_limit': server_data.max_player_limit,
            'player_list': server_data.player_list,
            'default_player_list': server_data.default_player_list,
            'favicon': server_data.favicon,
            'mod_type': server_data.mod_type,
            'mod_list': server_data.mod_list,
            'latency': server_data.latency,
            'bot_response': server_data.bot_response
        }
            
    elif server_data.platform_type == 'Bedrock':
        response = {
            'platform_type': server_data.platform_type,
            'ip_port': server_data.ip_port,
            'motd': server_data.motd,
            'version': server_data.version,
            'protocol': server_data.protocol,
            'brand': server_data.brand,
            'connected_players': server_data.connected_players,
            'max_player_limit': server_data.max_player_limit,
            'map': server_data.map,
            'gamemode': server_data.gamemode,
            'latency': server_data.latency,
            'bot_response': server_data.bot_response
        }

    else:
        response = None

    return response


@app.route('/api/minecraft_server_data', methods=['GET'])
def get_minecraft_server_data():
    
    
    server_address = request.args.get('server_address')
    bot = request.args.get('bot') == 'True'
    clean_data = request.args.get('clean_data') == 'True'
    
    if server_address:
        minecraft_server_data = asyncio.run(MinecraftServerData.get_server_data(server_address, bot, clean_data))

        if minecraft_server_data is not None:
            response = convert_server_data(minecraft_server_data)
            return jsonify(response)

        else:
            return jsonify({'Error': f'{GetUtilities.get_translated_text(["commands", "invalidArguments", "invalidServer"])}'}), 400

    else:
        return jsonify({'Error': f'{GetUtilities.get_translated_text(["commands", "server", "missingArgument1"])}'}), 400


def run_flask_app():
    

    serve(app, host='0.0.0.0', port=JsonManager.get('local_api_port'))

   
