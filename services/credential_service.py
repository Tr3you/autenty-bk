from shared.utils import Utils
from shared.token import Token
from .redis_service import validate_credentials, create_user, delete_user, update_password, update_email, get_user
from .firestore_service import get_aplication

class CredentialService:
    
    def __init__(self) -> None:
        pass

    def sign_in(self, email: str, password: str, client_id: str) -> str | None:
        app = get_aplication(client_id);
        user = get_user(client_id, email, password)
        if validate_credentials(client_id, email, password):
            return Token.write_token({"uid": user.get(b'uid').decode('utf-8'), "email": email}, app.get('dayTokenDuration'))
        return None

    def sign_up(self, email: str, password: str, client_id: str) -> bool | str:
        uid = Utils.generate_uid()
        if create_user(client_id, uid, email, password):
            return uid
        return False

    def delete_user(self, email: str, client_id: str) -> bool:
        if delete_user(client_id, email):
            return True
        return False

    def update_password(self, email: str, new_password: str, old_password: str, client_id: str) -> bool | str:
        if update_password(email, new_password, old_password, client_id):
            return True
        return False

    def update_email(self, new_email: str, old_email: str, client_id: str) -> bool | str:
        if update_email(new_email, old_email, client_id):
            return True
        return False