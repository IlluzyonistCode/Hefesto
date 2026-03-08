import requests
import json
import time
import sys

from ui.display import print_banner
from core.config_manager import JsonManager
from utils.network import GetUtilities
from utils.validation import CheckUtilities


class HefestoUpdater:
    @staticmethod
    def show_banner_update():
        
        try:
            update_banner_name = 'update'

            print_banner(
                update_banner_name,
                GetUtilities.get_translated_text(['banners', 'update', 'title']),
                GetUtilities.get_translated_text(['banners', 'update', 'checkingUpdates']),
                '', '', '', '', ''
            )

            time.sleep(1)

            if HefestoUpdater.check_update():
                print_banner(
                    update_banner_name,
                    GetUtilities.get_translated_text(['banners', 'update', 'title']),
                    GetUtilities.get_translated_text(['banners', 'update', 'checkingUpdates']),
                    GetUtilities.get_translated_text(['banners', 'update', 'newVersion']),
                    '', '', '', ''
                )

                time.sleep(1)

                print_banner(
                    update_banner_name,
                    GetUtilities.get_translated_text(['banners', 'update', 'title']),
                    GetUtilities.get_translated_text(['banners', 'update', 'checkingUpdates']),
                    GetUtilities.get_translated_text(['banners', 'update', 'newVersion']),
                    GetUtilities.get_translated_text(['banners', 'update', 'url']),
                    '&a&lhttps://github.com/Corruptor/Hefesto', ''
                )

                time.sleep(10)
                sys.exit()

            else:
                print_banner(
                    update_banner_name,
                    GetUtilities.get_translated_text(['banners', 'update', 'title']),
                    GetUtilities.get_translated_text(['banners', 'update', 'checkingUpdates']),
                    GetUtilities.get_translated_text(['banners', 'update', 'notFound']),
                    '', '', ''
                )

                time.sleep(2)

        except KeyboardInterrupt:
            return

    @staticmethod
    def check_update():
        current_version = JsonManager.get('currentVersion')

        latest_version = HefestoUpdater.get_latest_version()
        
        if current_version != latest_version:
            return True
        
        return False

    @staticmethod
    def get_latest_version():
        try:
            response = requests.get('https://raw.githubusercontent.com/Corruptor/Hefesto/main/config/config.json', timeout=10)
            response.raise_for_status()
            
            # Clean the response text to handle potential extra data
            response_text = response.text.strip()
            
            # Try to find valid JSON in the response
            if response_text.startswith('{'):
                # Find the end of the JSON object
                brace_count = 0
                json_end = 0
                for i, char in enumerate(response_text):
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            json_end = i + 1
                            break
                
                if json_end > 0:
                    json_text = response_text[:json_end]
                    js = json.loads(json_text)
                    return js['currentVersion']
            
            # If JSON parsing fails, return current version as fallback
            from core.config_manager import JsonManager
            return JsonManager.get('currentVersion')
            
        except (requests.RequestException, json.JSONDecodeError, KeyError, Exception):
            # Fallback to current version if any error occurs
            from core.config_manager import JsonManager
            return JsonManager.get('currentVersion')
