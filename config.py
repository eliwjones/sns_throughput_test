USER = None
REGION = None
ACCESS_KEY = None
SECRET = None
ARN_BASE = None

for val in [USER, REGION, ACCESS_KEY, SECRET, ARN_BASE]:
    if val is None:
        raise Exception("Please populate all config.py constants!")
