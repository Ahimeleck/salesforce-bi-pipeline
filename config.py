import os
from pathlib import Path
from dotenv import load_dotenv

dotenv_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=dotenv_path)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

SF_USERNAME        = os.getenv('SF_USERNAME')
SF_PASSWORD        = os.getenv('SF_PASSWORD')
SF_SECURITY_TOKEN  = os.getenv('SF_SECURITY_TOKEN')
SF_CONSUMER_KEY    = os.getenv('SF_CONSUMER_KEY')
SF_CONSUMER_SECRET = os.getenv('SF_CONSUMER_SECRET')

GCP_PROJECT_ID = os.getenv('GCP_PROJECT_ID')
BQ_DATASET     = os.getenv('BQ_DATASET')
