import easydata2 as ed
import datetime as dt
from pathlib import Path
import time

DB_NAME = 'cd'
db_path = Path(f'{DB_NAME}.json')
if not db_path.exists():
    ed.create_database(DB_NAME)
    print('Файл кулдауна не обнаружен!')

def cooldown_check(user: str, arg: str, cd: int):
    if ed.is_item_exist(DB_NAME, user, arg):
        then = dt.datetime.strptime(ed.get_item_data(DB_NAME, user, arg), "%Y-%m-%d %H:%M:%S.%f")
        now = dt.datetime.now()
        delta = now - then
        if delta.total_seconds() >= cd:
            return True
        else:
            return(str(cd - delta.total_seconds()).split('.')[0])
    else:
        return True
    
def cooldown_set(user: str, arg: str):
    if ed.is_id_exist(DB_NAME, user):
        
        ed.give_item_data(DB_NAME, user, arg, str(dt.datetime.now()))

    else:
        ed.give_id_data(DB_NAME, user, {})
        ed.give_item_data(DB_NAME, user, arg, str(dt.datetime.now()))