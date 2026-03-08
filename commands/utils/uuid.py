from ui.colors import paint
from utils.network import GetUtilities
from utils.log_manager import LogManager


def uuid_command(username, *args):
    

    try:
        online_uuid, offline_uuid = GetUtilities.get_player_uuid(username)
        
        log_file = LogManager.create_log_file('uuid')

        if online_uuid is not None:
            log_data = f'[Username] {username} [UUID Premium] {online_uuid} [UUID No Premium] {offline_uuid}\n'
            
            paint(f'\n{GetUtilities.get_spaces()}&4[&cUU&f&lID&4] {GetUtilities.get_translated_text(["commands", "uuid", "onlineUUID"])} {online_uuid}\n{GetUtilities.get_spaces()}&4[&cUU&f&lID&4] {GetUtilities.get_translated_text(["commands", "uuid", "offlineUUID"])} {offline_uuid}')

        else:
            log_data = f'[Username] {username} [UUID No Premium] {offline_uuid}\n'
            
            paint(f'\n{GetUtilities.get_spaces()}&4[&cUU&f&lID&4] {GetUtilities.get_translated_text(["commands", "uuid", "offlineUUID"])} {offline_uuid}')

        LogManager.write_log(log_file, 'uuid', log_data)

    except KeyboardInterrupt:
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "ctrlC"])}')

