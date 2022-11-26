from jwt import encode
from os import getenv
from datetime import datetime, timedelta


class Token:

    @classmethod
    def write_token(self, data: dict, days: int) -> bytes | None:
        try:
            token = encode(payload={**data, "exp": self.expire_date(days=days)},
                       key=getenv('SECRET_JWT'), algorithm='HS256')
            return token.encode("UTF-8")
        except Exception as e:
            print(str(e))
            return None


    @classmethod
    def expire_date(self, days: int) -> datetime:
        now = datetime.now()
        return now + timedelta(days)
