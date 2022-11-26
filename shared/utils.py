import random
import string
from services.firestore_service import get_aplication, get_application_by_secret
from datetime import date


class Utils:

    def generate_uid() -> str:
        number_of_strings = 5
        length_of_string = 20
        uid = ""
        for x in range(number_of_strings):
           uid =  ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))
        return uid

    def validate_secret(secret: str) -> bool:
        app = get_application_by_secret(secret)
        if app != None:
            return True
        return False

    def validate_password_format(password: str, client_id: str) -> bool:
        app = get_aplication(client_id)
        haveNum, haveEspecial, haveMayus = False, False, False
        if(app == None):
            return False
        formats = [app.get("passMinLenght"), app.get("passMustEspecials"), app.get("passMustMayus"), app.get("passMustNumbers")]
        for character in password:
            if character.isdigit():
                haveNum = True
            if character.isupper():
                haveMayus = True
            if character == "@" or character == "_" or character == "-" or character == "?" or character == "¿" or character == "!" or character == "¡":
                haveEspecial= True
        if len(password) < formats[0]:
            return False
        if formats[1] == True and haveEspecial == False:
            return False
        if formats[2] == True and haveMayus == False:
            return False
        if formats[3] == True and haveNum == False:
            return False
        return True

    def validate_change_credential(credential_to_change: str, client_id: str) -> bool:
        app = get_aplication(client_id)
        today = date.today()
        if credential_to_change == 'email':
            pass
        elif credential_to_change == 'password':
            pass
        return True