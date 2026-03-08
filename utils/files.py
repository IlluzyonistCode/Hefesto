from utils.validation import CheckUtilities


class FileUtilities:
    @staticmethod
    def write_file(file, text, mode='w', clean_file=False):
        

        try:
            with open(file, mode, encoding='utf8') as f:
                if clean_file:
                    f.truncate(0)

                f.write(text)

        except FileNotFoundError:
            pass

    @staticmethod
    def read_file(file, mode='read'):
        
            
        try:
            with open(file, 'r+', encoding=CheckUtilities.check_file_encoding(file)) as f:
                if mode == 'read':
                    return f.read()
                
                elif mode == 'readlines':
                    return f.readlines()
            
        except FileNotFoundError:
            return None
