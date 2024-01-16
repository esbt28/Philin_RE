import json
from typing import Any, Union

def create_database(f_name: str) -> None:
    file = f'{f_name}.json'
    
    with open(file, 'w') as f:
        json.dump({}, f)

def _read_data(f_name: str) -> dict[str, dict[str, Any]]:
    file = f'{f_name}.json'
    
    with open(file, 'r') as f:
        data = json.load(f)
        
    return data

def _write_data(f_name, value: dict[str, dict[str, Any]]) -> None:
    file = f'{f_name}.json'
    
    with open(file, 'w') as f:
        json.dump(value, f, indent=4)

def get_id_data(f_name: str, id: str) -> Union[dict[str, Any], None]:
    
    data = _read_data(f_name)
    
    return data.get(id, None)

def get_item_data(f_name: str, id: str, item: str) -> Any:
    
    data = _read_data(f_name)

    user_data = data.get(id, None)
    
    if not user_data:
        return
        
    return user_data.get(item, None)

def give_id_data(f_name: str, id: str, value: dict[str, dict[str, Any]]) -> None:
    
    data = _read_data(f_name)
    
    data[id] = value
    
    _write_data(f_name, data)
    
    return value
    
def give_item_data(f_name: str, id: str, item: str, value: Any) -> None:
    
    data = _read_data(f_name)
    
    user_data = data.get(id, None)

    if user_data == None and id not in data:
        give_id_data(f_name, id, {})
        user_data = {}

    user_data[item] = value 
    
    data[id] = user_data

    _write_data(f_name, data)
    
    return value

def give_all_data(f_name: str, item: str, value: Any) -> None:
    
    data = _read_data(f_name)
    
    for user in data:
        give_item_data(f_name, user, item, value)
        
    return value
        
def delete_id_data(f_name: str, id: str) -> None:
    data = _read_data(f_name)

    if not id in data:
        return

    del data[id]
    _write_data(f_name, data)
    
    return id

def ids(f_name: str) -> dict[str, Any]:
    
    data = _read_data(f_name)
    ids = []
    
    for id in data:
        
        ids.append(id)
    
    return ids
    
def is_id_exist(f_name: str, id: str):
    
    if get_id_data(f_name, id) != None:
        return True
    
    else:
        return False
    
def is_item_exist(f_name: str, id: str, item: str):
    
    if get_item_data(f_name, id, item) != None:
        return True
    
    else:
        return False