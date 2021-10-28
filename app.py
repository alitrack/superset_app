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
from sqlalchemy.engine import create_engine
from superset.cli import superset

def init():
    if pathlib.Path("superset_config.py").exists():
        return 
    
    path =pathlib.Path(__file__).absolute().as_posix()
    e = create_engine('sqlite:///superset.db')
    e.execute(f"update dbs set sqlalchemy_uri='sqlite:///{path}/superset.db'")
    with open('superset_config.py','w') as file:
        file.write(f'SQLALCHEMY_DATABASE_URI = "sqlite:///{path}/superset.db"')

def main():
    init()
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(superset())
    
if __name__ == '__main__':
    main()
