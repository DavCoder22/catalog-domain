# catalog-domain/config/dev_config.py
import os

MONGO_URI = os.getenv('MONGO_URI', 'mongodb+srv://mongo:Sebasalejandro22@catalogcluster.wxsop.mongodb.net/?retryWrites=true&w=majority&appName=catalogCluster')
