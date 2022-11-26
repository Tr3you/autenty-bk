import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account.
cred = credentials.Certificate('serviceAccount.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()

def get_aplication(client_id: str) -> dict | None:
    application_ref = db.collection(u'apps')
    docs = application_ref.stream()
    for doc in docs:
        if doc.id == client_id:
            return doc.to_dict()
    return None

def get_application_by_secret(secret) -> dict:
    application_ref = db.collection(u'apps')
    query_ref = application_ref.where(u'secretId', u'==', secret).stream()
    for doc in query_ref:
        return doc.to_dict()
