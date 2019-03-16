import os
import sys

from dotenv import load_dotenv


# Load variables from .env
load_dotenv(override=True)

REQUIRED_ENV_VARS = (
    'TOKEN',
    'USERNAME',
    'PASSWORD'
)

for var in REQUIRED_ENV_VARS:
    if var not in os.environ:
        sys.exit(f'{var} is required parameter')
