import os
import json


class JsonManager:
    @staticmethod
    def load_json(file_path):
        

        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf8') as f:
                return json.loads(f.read())

        return JsonManager.DEFAULT_CONFIG

    @staticmethod
    def save_json(content, file_path):
        

        with open(file_path, 'w', encoding='utf8') as f:
            f.write(json.dumps(content, indent=4))

    @staticmethod
    def get(key, file_path='./config/config.json'):
        
        
        content = JsonManager.load_json(file_path)
        
        if isinstance(key, list):
            value = content
            for k in key:
                if isinstance(value, dict):
                    value = value.get(k)
                else:
                    return None
            return value
        
        else:
            return content.get(key)
