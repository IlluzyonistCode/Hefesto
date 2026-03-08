
from .mc import colors
from .mc import codes


def mcreplace(text, reset_all=True):
    

    for code in codes.items():
        if str(code[0]) in colors:
            text = text.replace(f'&{code[0]}', f'&r{code[1]}'
                    ).replace(f'§{code[0]}', f'&r{code[1]}')
            
        else:
            text = text.replace(f'&{code[0]}', code[1]
                    ).replace(f'§{code[0]}', code[1])

    if reset_all:
        return f'{text}\033[0m'
    
    else:
        return text
