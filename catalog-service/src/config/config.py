# src/config/config.py

import os
from config.dev_config import get_db_config as get_dev_db_config
from config.prod_config import get_db_config as get_prod_db_config
from config.test_config import get_db_config as get_test_db_config

def get_config(env='dev'):
    config_map = {
        'dev': get_dev_db_config,
        'prod': get_prod_db_config,
        'test': get_test_db_config
    }
    return config_map.get(env, get_dev_db_config)()

# Uso en tu aplicación
environment = os.getenv('FLASK_ENV', 'dev')
db_config = get_config(environment)
