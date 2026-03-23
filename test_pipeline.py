"""
test_pipeline.py
Corre este script antes del pipeline real para verificar que todo esta configurado correctamente.
No carga ni modifica ningun dato.

Uso: python test_pipeline.py
"""

import os
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv

# ── Cargar .env ───────────────────────────────────────────────────────────────
dotenv_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=dotenv_path)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', '')

errores = []

def ok(msg):
    print(f"  ✓ {msg}")

def fallo(msg):
    print(f"  ✗ {msg}")
    errores.append(msg)

# ─────────────────────────────────────────────────────────────────────────────
print("\n── TEST 1: Variables del .env ───────────────────────────────────────────")

variables = [
    'SF_USERNAME',
    'SF_PASSWORD',
    'SF_SECURITY_TOKEN',
    'SF_CONSUMER_KEY',
    'SF_CONSUMER_SECRET',
    'GOOGLE_APPLICATION_CREDENTIALS',
    'GCP_PROJECT_ID',
    'BQ_DATASET',
    'BQ_TABLE',
]

for var in variables:
    valor = os.getenv(var)
    if valor:
        ok(f"{var} = {'*' * min(len(valor), 6)}... ({len(valor)} caracteres)")
    else:
        fallo(f"{var} no encontrada o vacía en .env")

# ─────────────────────────────────────────────────────────────────────────────
print("\n── TEST 2: Archivo google-credentials.json ──────────────────────────────")

creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', '')
if not creds_path:
    fallo("GOOGLE_APPLICATION_CREDENTIALS no está definida en .env")
elif not Path(creds_path).exists():
    fallo(f"Archivo no encontrado: {creds_path}")
else:
    ok(f"Archivo encontrado: {creds_path}")
    try:
        import json
        with open(creds_path) as f:
            creds = json.load(f)
        ok(f"JSON válido — tipo: {creds.get('type')}, proyecto: {creds.get('project_id')}")
    except Exception as e:
        fallo(f"Error leyendo el JSON: {e}")

# ─────────────────────────────────────────────────────────────────────────────
print("\n── TEST 3: Conexión a Salesforce ────────────────────────────────────────")

try:
    response = requests.post('https://login.salesforce.com/services/oauth2/token', data={
        'grant_type': 'password',
        'client_id': os.getenv('SF_CONSUMER_KEY'),
        'client_secret': os.getenv('SF_CONSUMER_SECRET'),
        'username': os.getenv('SF_USERNAME'),
        'password': os.getenv('SF_PASSWORD') + os.getenv('SF_SECURITY_TOKEN', '')
    }, timeout=15)

    auth = response.json()

    if 'access_token' in auth:
        ok(f"Autenticación exitosa")
        ok(f"Instance URL: {auth.get('instance_url')}")

        # Verificar que podemos hacer una query simple
        headers = {'Authorization': f"Bearer {auth['access_token']}"}
        test_query = requests.get(
            f"{auth['instance_url']}/services/data/v59.0/query",
            headers=headers,
            params={'q': 'SELECT COUNT() FROM Opportunity'},
            timeout=15
        ).json()

        if 'totalSize' in test_query:
            ok(f"Query exitosa — {test_query['totalSize']} Opportunities encontradas")
        else:
            fallo(f"Query falló: {test_query}")
    else:
        fallo(f"Autenticación falló: {auth.get('error')} — {auth.get('error_description')}")
        if auth.get('error') == 'invalid_grant':
            print("    → Verifica: contraseña correcta, Security Token actualizado,")
            print("      OAuth Username-Password Flow activado en Salesforce Setup,")
            print("      y que estés usando Connected App clásica (no External Client App).")

except requests.exceptions.ConnectionError:
    fallo("No hay conexión a internet o Salesforce no responde")
except requests.exceptions.Timeout:
    fallo("Timeout — Salesforce tardó demasiado en responder")
except Exception as e:
    fallo(f"Error inesperado: {e}")

# ─────────────────────────────────────────────────────────────────────────────
print("\n── TEST 4: Conexión a BigQuery ──────────────────────────────────────────")

try:
    from google.cloud import bigquery

    project_id = os.getenv('GCP_PROJECT_ID')
    dataset    = os.getenv('BQ_DATASET')
    table      = os.getenv('BQ_TABLE')

    client = bigquery.Client(project=project_id)
    ok(f"Cliente BigQuery creado — proyecto: {project_id}")

    # Verificar que el dataset existe
    dataset_ref = client.get_dataset(f"{project_id}.{dataset}")
    ok(f"Dataset encontrado: {dataset_ref.dataset_id}")

    # Verificar si la tabla existe (puede no existir la primera vez)
    try:
        table_ref = client.get_table(f"{project_id}.{dataset}.{table}")
        ok(f"Tabla encontrada: {table_ref.table_id} ({table_ref.num_rows} filas)")
    except Exception:
        ok(f"Tabla '{table}' no existe aún — se creará al correr el pipeline por primera vez")

except Exception as e:
    fallo(f"Error conectando a BigQuery: {e}")
    if '403' in str(e) or 'permission' in str(e).lower():
        print("    → Verifica que el Service Account tiene los roles:")
        print("      BigQuery Data Editor + BigQuery Job User")
    elif 'credentials' in str(e).lower():
        print("    → Verifica la ruta del archivo google-credentials.json en .env")

# ─────────────────────────────────────────────────────────────────────────────
print("\n── RESUMEN ──────────────────────────────────────────────────────────────")

if not errores:
    print("  ✓ Todo listo — puedes correr pipeline.py\n")
else:
    print(f"  ✗ {len(errores)} problema(s) encontrado(s):")
    for e in errores:
        print(f"    - {e}")
    print("\n  Corrige los errores antes de correr pipeline.py\n")
    sys.exit(1)
