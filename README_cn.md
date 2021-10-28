# Apache Superset 开箱即用开发笔记

## Python 版本选择

尝试过miniconda 和 Python embeded 后，选择了后者，因为体积更小。

本文以Python3.8.10为例，

## 安装Apache Superset

- 下载以下三个包（准备工作）

  - [python-3.8.10-embed-amd64.zip](https://www.python.org/ftp/python/3.8.10/python-3.8.10-embed-amd64.zip)
  - [get-pip.py](https://bootstrap.pypa.io/get-pip.py)
  - [python_geohash‑0.8.5‑cp38‑cp38‑win_amd64.whl](https://download.lfd.uci.edu/pythonlibs/w6tyco5e/python_geohash-0.8.5-cp38-cp38-win_amd64.whl)

  使用[非官方Windows 二进制Python扩展包](https://www.lfd.uci.edu/~gohlke/pythonlibs/)可以避免下载庞大的VC编译工具
- 解压缩python-3.8.10-embed-amd64.zip并修改`python38._ph`

  该文件为文本格式，打开-->把`# import site`前面的注释符号“#”删除-->保存-->结果如下，

```
python38.zip
.

# Uncomment to run site.main() automatically
import site
```

- 安装pip

  在Python目录下运行

```bash
python get-pip.py
```

- 安装python_geohash‑0.8.5‑cp38‑cp38‑win_amd64.whl

```bash
python -m pip install ..\python_geohash‑0.8.5‑cp38‑cp38‑win_amd64.whl
```

- 安装apache superset包及其它依赖

```bash
pip install apache-superset pillow -i   https://mirrors.aliyun.com/pypi/simple/
pip install markdown==3.2.2
```

如果不降级markdown版本，运行`superset`时会报如下错误,

```
Traceback (most recent call last):
  File "runpy.py", line 194, in _run_module_as_main
  File "runpy.py", line 87, in _run_code
  File "C:\superset\superset\Scripts\superset.exe\__main__.py", line 4, in <module>
  File "C:\superset\superset\lib\site-packages\superset\__init__.py", line 21, in <module>
    from superset.app import create_app
  File "C:\superset\superset\lib\site-packages\superset\app.py", line 23, in <module>
    from superset.initialization import SupersetAppInitializer
  File "C:\superset\superset\lib\site-packages\superset\initialization\__init__.py", line 48, in <module>
    from superset.security import SupersetSecurityManager
  File "C:\superset\superset\lib\site-packages\superset\security\__init__.py", line 17, in <module>
    from superset.security.manager import SupersetSecurityManager  # noqa: F401
  File "C:\superset\superset\lib\site-packages\superset\security\manager.py", line 66, in <module>
    from superset.utils.core import DatasourceName, RowLevelSecurityFilterType
  File "C:\superset\superset\lib\site-packages\superset\utils\core.py", line 64, in <module>
    import markdown as md
  File "C:\superset\superset\lib\site-packages\markdown\__init__.py", line 29, in <module>
    from .core import Markdown, markdown, markdownFromFile  # noqa: E402
  File "C:\superset\superset\lib\site-packages\markdown\core.py", line 27, in <module>
    from .preprocessors import build_preprocessors
  File "C:\superset\superset\lib\site-packages\markdown\preprocessors.py", line 29, in <module>
    from .htmlparser import HTMLExtractor
  File "C:\superset\superset\lib\site-packages\markdown\htmlparser.py", line 31, in <module>
    spec.loader.exec_module(htmlparser)
AttributeError: 'zipimporter' object has no attribute 'exec_module'
```

- 初始化superset

```
#初始化数据库
superset db upgrade

#创建管理员用户
superset fab create-admin

# 加载事例数据（可能会因为网络问题导致失败，可以忽略报错）
superset load_examples

# 创建默认角色和权限
superset init

# 下面命令是superset web server 以多线程、开发模式运行在8080端口上，端口如果冲突，可以修改。
superset run -p 8088 --with-threads --reload --debugger
```

这样创建的数据库在当前用户的.superset目录，假如当前用户名是`win`，则superset.db的完整路径是`c:\users\win\.superset\superset.db`。

## 制作开箱即用版本

- 将superset.db复制到python相同目录
- 创建app.py

```python
import sys
import os 
import pathlib

import re
from sqlalchemy.engine import create_engine
from superset.cli import superset

def init():
    # 如果superset_config.py 存在，表示已做过初始化
    # 如果换了路径，建议删除superset_config.py，重新执行初始化
    if pathlib.Path("superset_config.py").exists():
        return 
  
    path =pathlib.Path(__file__).absolute().as_posix()
    # 修改example数据库路径（需要绝对路径）
    e = create_engine('sqlite:///superset.db')
    e.execute(f"update dbs set sqlalchemy_uri='sqlite:///{path}/superset.db'")
    #superset从superset_config.py 读取数据库连接设置
    with open('superset_config.py','w') as file:
        file.write(f'SQLALCHEMY_DATABASE_URI = "sqlite:///{path}/superset.db"')

def main():
    init()
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(superset())
  
if __name__ == '__main__':
    main()

```

关于把app.py编译成app.exe，这是另外的话题了，涉及到了nuitka，有兴趣的可以去研究下，我的公众号里也有部分这方面的内容。
