import logging
import requests
from config import (
    SF_USERNAME, SF_PASSWORD, SF_SECURITY_TOKEN,
    SF_CONSUMER_KEY, SF_CONSUMER_SECRET
)

log = logging.getLogger(__name__)

def conectar_salesforce():
    response = requests.post('https://login.salesforce.com/services/oauth2/token', data={
        'grant_type':    'password',
        'client_id':     SF_CONSUMER_KEY,
        'client_secret': SF_CONSUMER_SECRET,
        'username':      SF_USERNAME,
        'password':      SF_PASSWORD + SF_SECURITY_TOKEN
    })
    auth = response.json()
    if 'access_token' not in auth:
        raise Exception(f"Error autenticando Salesforce: {auth}")
    log.info("Conectado a Salesforce")
    return auth['access_token'], auth['instance_url']

def extraer_objeto(instance_url, access_token, query):
    headers = {'Authorization': f'Bearer {access_token}'}
    raw = requests.get(
        f"{instance_url}/services/data/v59.0/query",
        headers=headers,
        params={'q': query}
    )
    if raw.status_code != 200:
        raise Exception(f"Salesforce respondió {raw.status_code} — {raw.text[:200]}")
    result = raw.json()
    if 'records' not in result:
        raise Exception(f"Respuesta inesperada: {result}")
    return result['records']

