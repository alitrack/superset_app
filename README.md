# superset_app

Apache Superset out of box version (Windows 64bit)

## prepare job

### download 3 files

* [python-3.8.10-embed-amd64.zip](https://www.python.org/ftp/python/3.8.10/python-3.8.10-embed-amd64.zip)
* [get-pip.py](https://bootstrap.pypa.io/get-pip.py)

* python_geohash‑0.8.5‑cp38‑cp38‑win_amd64.whl [download from here](https://www.lfd.uci.edu/~gohlke/pythonlibs/)

unzip python-3.8.10-embed-amd64.zip and goto the unzip folder

### modify `python38._ph`

```
python38.zip
.

# Uncomment to run site.main() automatically
import site
```

### install pip

```bash
python ..\get-pip.py
```

### install python_geohash

```bash
python -m pip install ..\python_geohash‑0.8.5‑cp38‑cp38‑win_amd64.whl
```

## install Apache Superset and pillow

```bash
python -m pip install -U apache-superset  pillow markdown==3.2.2 Werkzeug==2.0.3
```

## install some common database drivers
```bash
python -m pip install mysqlclient pymssql==2.1.5 psycopg2-binary clickhouse-driver==0.2.0  clickhouse-sqlalchemy==0.1.6  duckdb-engine
```

### init Apache Superset

```bash
set FLASK_APP=superset 

# initialize the database:
Scripts\superset db upgrade

# Create an admin user
Scripts\superset fab create-admin

# Load some data to play with
Scripts\superset load_examples

# Create default roles and permissions
Scripts\superset init

# To start a development web server on port 8088, use -p to bind to another port
Scripts\superset run -p 8088 --with-threads --reload --debugger
```


### copy `superset.db` to current folder

```bash
copy %UserProfile%\.superset\superset.db 
```


### run app.py

```bash
 python app.py
```

first time it will create `superset_config.py` and modify the example url to current folder(need absolute path).
