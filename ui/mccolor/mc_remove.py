
from .mc import codes


def mcremove(text):
    

    for code in codes.items():
        text = text.replace(f'&{code[0]}', ''
                  ).replace(f'§{code[0]}', '')
    
    return text
