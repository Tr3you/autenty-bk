import redis
import os


redis_client = redis.Redis(
  host= os.getenv('REDIS_HOST'),
  port= os.getenv('REDIS_PORT'),
  password= os.getenv('REDIS_PASSWORD'),
  ssl=True
)

def validate_credentials(client_id, email, password) -> bool:
    user = redis_client.hgetall(f'{client_id}:{email}')
    if user.get(b'password') != None and user.get(b'password').decode('utf-8') == password:
        return True
    return False

def get_user(client_id, email, password) -> dict | None:
    user = redis_client.hgetall(f'{client_id}:{email}')
    if user.get(b'password') != None and user.get(b'password').decode('utf-8') == password:
        return user
    return None

def create_user(client_id, uid, email, password) -> bool:
    hash_data = {"uid": uid, "email": email, "password": password}
    return redis_client.hmset(f'{client_id}:{email}', hash_data)

def delete_user(client_id, email) -> bool:
    try:
        fields = ["uid", "email", "password"]
        for field in fields:
            redis_client.hdel(f'{client_id}:{email}', field)
        return True
    except Exception:
        return False

def update_password(email, new_password, old_password, client_id) -> bool:
    if validate_credentials(client_id, email, old_password):
        redis_client.hset(f'{client_id}:{email}', "password", new_password)
        return True
    return False

def update_email(new_email, old_email, client_id) -> bool:
    user = redis_client.hgetall(f'{client_id}:{old_email}')
    if user.get('email') != None:
        try:
            delete_user(client_id, old_email)
            create_user(client_id, user.get('uid'), new_email, user.get('password'))
            return True
        except Exception:
            return False
    return False

    