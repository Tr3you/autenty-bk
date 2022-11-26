from flask import Flask, request
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
from services.credential_service import CredentialService
from shared.utils import Utils

app = Flask(__name__)
cors = CORS(app)
credential_service = CredentialService()
load_dotenv()


@app.before_request
def middleware():
    secret = request.headers.get("secret")
    if not Utils.validate_secret(secret):
        return {"message": "You are not authorized to make this request."}, 401


# Este metodo sirve para iniciar sesion al usuario
@app.route('/sign-in', methods=['POST'])
@cross_origin()
def sign_in():
    data = request.get_json()
    if(data.get('email') == None or data.get('password') == None or data.get('clientId') == None):
        return {"message": "Missing parameters"}, 400
    token = credential_service.sign_in(data['email'], data['password'], data['clientId'])
    if token != None:
        return {"message": "OK", "token": token.decode('utf-8')}, 200
    return {"message": "Credentials are incorrect"}, 500


# Este metodo sirve pare crear credenciales
@app.route('/sign-up', methods=['POST'])
@cross_origin()
def sign_up():
    data = request.get_json()
    if(data.get('email') == None or data.get('password') == None or data.get('clientId') == None):
        return {"message": "Missing parameters"}, 400

    if not Utils.validate_password_format(data['password'], data['clientId']):
        return  {"message": "Password does not meet the required format or client secret is wrong"}, 400

    uid = credential_service.sign_up(data['email'], data['password'], data['clientId'])
    if uid != False:
        return {"message": "OK", "uid": uid}, 200
    return {"message": "something went wrong, try again"}, 500


# Elimina una cuenta de usuario
@app.route('/delete', methods=['DELETE'])
@cross_origin()
def delete_user():
    data = request.get_json()
    if(data.get('email') == None or data.get('clientId') == None):
        return {"message": "Missing parameters"}, 400
    if credential_service.delete_user(data['email'], data['clientId']):
        return {"message": "OK"}, 200
    return {"message": "something went wrong, try again"}, 500


# Actualizar contraseña
@app.route('/restore-password', methods=['PUT'])
@cross_origin()
def change_password():
    data = request.get_json()
    if(data.get('email') == None or data.get('newPassword') == None or data.get('oldPassword') == None or data.get('clientId') == None):
        return {"message": "Missing parameters"}, 400
    if credential_service.update_password(data['email'],data['newPassword'], data['oldPassword'], data['clientId']):
        return {"message": "OK"}, 200
    return {"message": "Passwords do not match or are incorrect"}, 500


# Actualizar el correo
@app.route('/change-email', methods=['PUT'])
@cross_origin()
def update_email():
    data = request.get_json()
    if(data.get('newEmail') == None == None or data.get('oldEmail') == None or data.get('clientId') == None):
        return {"message": "Missing parameters"}, 400
    if credential_service.update_email(data['newEmail'], data['oldEmail'], data['clientId']):
        return {"message": "OK"}, 200
    return {"message": "The email address you entered does not belong to any account"}, 500


if __name__ == '__main__':
    load_dotenv()
    app.run(debug=False, port='4000', host='0.0.0.0')




