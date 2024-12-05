from typing import Dict, List
from redis import Redis
from recall.config import config

#### save into Redis
redis_config = config['redis']
redis = Redis(host=redis_config['host'], port=redis_config['port'], db=redis_config['db'])

ITEM_EMB_KEY = 'recall:emb:item'
USER_EMB_KEY = 'recall:emb:user'

def save_item_embedding(item_emb: Dict):
    """
    item_emb: Dict[item_id -> List[float]]
    """
    encoded_emb = {k: stringify_vector(v) for (k, v) in item_emb.items()}
    redis.hset(ITEM_EMB_KEY, mapping=encoded_emb)

def get_all_fields_from_items() -> dict:
    try:
        fields = redis.hgetall(ITEM_EMB_KEY)  # Fetch all fields in the hash
        # Decode each field from bytes to string
        return {k.decode('utf-8'): v.decode('utf-8') for k, v in fields.items()}
    except Exception as e:
        print(f"Error getting all fields from hash {ITEM_EMB_KEY}: {e}")
        return {}
   
def save_user_embedding(user_emb: Dict):
    """
    user_emb: Dict[user_id -> List[float]] 
    """
    encoded_emb = {k: stringify_vector(v) for (k, v) in user_emb.items()}
    redis.hset(USER_EMB_KEY, mapping=encoded_emb)


def get_one_item_embedding(item_id: int) -> List[float]:
    emb = redis.hget(ITEM_EMB_KEY, item_id)
    if emb is None:
        return None
    return parse_vector_string(emb.decode())

def get_one_user_embedding(user_id: int) -> List[float]:
    emb = redis.hget(USER_EMB_KEY, user_id)
    if emb is None:
        return None
    return parse_vector_string(emb.decode())

def get_all_item_embedding() -> Dict[int, List[float]]:
    data = redis.hgetall(ITEM_EMB_KEY)
    print(data)
    res = {int(k.decode()): parse_vector_string(v.decode()) for (k, v) in data.items()}
    return res

def stringify_vector(vec):
    if vec is None:
        return ''
    return ':'.join(list(map(lambda v: str(v), vec)))

def parse_vector_string(s):
    if len(s) == 0:
        return None
    return [float(x) for x in s.split(':')]
