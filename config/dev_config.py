# catalog-domain/config/dev_config.py
import os

MONGO_URI = os.getenv('MONGO_URI', 'mongodb+srv://mongo:Sebasalejandro22@catalogcluster.wxsop.mongodb.net/?retryWrites=true&w=majority&appName=catalogCluster')
ELASTICSEARCH_HOSTS = os.getenv('ELASTICSEARCH_HOSTS', 'https://c4e7f575d7964e5baadcc40ef7bd056c.us-central1.gcp.cloud.es.io:443')
ELASTICSEARCH_API_KEY = os.getenv('ELASTICSEARCH_API_KEY', 'VVlseFo1VUI1eUN1VGJfQUZVMEw6Zm53UU9Ib1RUYUdrTzBmWC1VdlRYdw==')
