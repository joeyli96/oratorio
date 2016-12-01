from oauth2client import client, crypt
from .settings import SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
from .models import Speech, Recording


def get_context(token):
    """Throws crypt.AppIdentityError if token is not valid"""
    idinfo = verify_id_token(token)

    recordings = []
    for speech in Speech.objects.filter(user__email=idinfo["email"]):
        for recording in Recording.objects.filter(speech=speech):
            recordings.append(recording)

    context = {'recordings': recordings, }
    return context


def verify_id_token(token):
    """Throws crypt.AppIdentityError if token is not valid"""
    client_id = SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
    idinfo = client.verify_id_token(token, client_id)
    # If multiple clients access the backend server:
    if idinfo['aud'] not in [client_id]:
        raise crypt.AppIdentityError("Unrecognized client.")
    if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
        raise crypt.AppIdentityError("Wrong issuer.")
    return idinfo
