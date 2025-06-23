import pickle
import base64


def email_to_db(email):
    return base64.encodebytes(pickle.dumps(email)).decode('utf-8')


def db_to_email(data):
    return pickle.loads(base64.decodebytes(data.encode('utf-8')))

