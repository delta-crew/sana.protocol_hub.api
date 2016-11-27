import os

# Database
DB_HOST     = os.getenv('PH_API_DB_HOST', 'localhost:5432')
DB_USER     = os.getenv('PH_API_DB_USER', 'ph')
DB_PASSWORD = os.getenv('PH_API_DB_PASSWORD', 'password')
DB_DATABASE = os.getenv('PH_API_DB_DATABASE', 'ph')
DB_URI      = 'postgresql://{}:{}@{}/{}'.format(
                  DB_USER, DB_PASSWORD, DB_HOST, DB_DATABASE)

# Development
DEV         = os.getenv('PH_DEV', False)
