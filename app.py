# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
import sys
import os 
import pathlib
import re
import base64
from sqlalchemy.engine import create_engine
os.environ['FLASK_APP'] = 'superset'


def create_secret_key():
    random_bytes = os.urandom(42) 
    base64_encoded = base64.b64encode(random_bytes)
    return base64_encoded.decode('utf-8')

from superset.config import VERSION_STRING
if VERSION_STRING < '1.5.0':
    from superset.cli import superset
else:
    from superset.cli.main import superset

def init():
    if pathlib.Path("superset_config.py").exists():
        return 
    
    path =pathlib.Path(".").absolute().as_posix()
    if pathlib.Path('superset.db').exists:
        e = create_engine('sqlite:///superset.db')
        # 判断表是否存在
        table_check = e.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='dbs';").fetchone()
        if table_check:
            # 表存在，则执行更新操作
            e.execute(f"update dbs set sqlalchemy_uri='sqlite:///{path}/superset.db'")
        else:
            # 表不存在，则不执行任何操作
            pass    

    
    with open('superset_config.py','w') as file:
        file.write(f"""
import pathlib
if pathlib.Path("superset_config_ex.py").exists():
    from superset_config_ex import *
SECRET_KEY = "{create_secret_key()}"    
        """)
        file.write("\n")
        file.write(f'SQLALCHEMY_DATABASE_URI = "sqlite:///{path}/superset.db"')

def main():
    init()
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(superset())
    
if __name__ == '__main__':
    main()