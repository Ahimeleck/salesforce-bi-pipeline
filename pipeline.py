import logging
from sf_extractor import conectar_salesforce, extraer_objeto
from bq_loader import conectar_bigquery, cargar_tabla
from objects import OBJETOS

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s — %(levelname)s — %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
log = logging.getLogger(__name__)

# ── Conectar ──────────────────────────────────────────────────────────────────
try:
    access_token, instance_url = conectar_salesforce()
except Exception as e:
    log.error(f"No se pudo conectar a Salesforce: {e}")
    raise

try:
    client = conectar_bigquery()
except Exception as e:
    log.error(f"No se pudo conectar a BigQuery: {e}")
    raise

# ── Ejecutar objetos ──────────────────────────────────────────────────────────
exitosos = []
fallidos  = []

for obj in OBJETOS:
    try:
        records = extraer_objeto(instance_url, access_token, obj['query'])
        cargar_tabla(
            client=client,
            records=records,
            table_name=obj['table_name'],
            schema=obj['schema'],
            date_cols=obj.get('date_cols', []),
            numeric_cols=obj.get('numeric_cols', [])
        )
        exitosos.append(obj['table_name'])
    except Exception as e:
        log.error(f"{obj['table_name']}: {e}")
        fallidos.append(obj['table_name'])

# ── Resumen ───────────────────────────────────────────────────────────────────
log.info(f"Pipeline completo — {len(exitosos)} exitosos, {len(fallidos)} fallidos")
if fallidos:
    log.warning(f"Tablas con error: {', '.join(fallidos)}")
else:
    log.info("Todas las tablas cargadas correctamente")
