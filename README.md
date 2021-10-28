# superset_app

Apache Superset out of box version (Windows 64bit)

## prepare job

### download 3 files

* [python-3.8.10-embed-amd64.zip](https://www.python.org/ftp/python/3.8.10/python-3.8.10-embed-amd64.zip)
* [get-pip.py](https://bootstrap.pypa.io/get-pip.py)

* [python_geohash‑0.8.5‑cp38‑cp38‑win_amd64.whl](https://download.lfd.uci.edu/pythonlibs/w6tyco5e/python_geohash-0.8.5-cp38-cp38-win_amd64.whl)

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

## install apache superset and pillow

```bash
pip install apache-superset pillow
pip install markdown==3.2.2
```

### init superset

```bash
# initialize the database:
superset db upgrade

# Create an admin user
$ export FLASK_APP=superset
superset fab create-admin

# Load some data to play with
superset load_examples

# Create default roles and permissions
superset init

# To start a development web server on port 8088, use -p to bind to another port
superset run -p 8088 --with-threads --reload --debugger
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
