#!/usr/bin/env python
# coding: utf-8
# In[3]:
import ssl
import sys
import os
import base64
import subprocess
from base64 import b85decode,b85encode
from urllib.request import urlopen
unverified_context = ssl._create_unverified_context()
ver = "".join(sys.version.split(".")[:2])

import urllib.error

class DownloadError(Exception):
    pass

# In[ ]:

"""请根据你的需要修改"""
MIRROR = "https://mirrors.aliyun.com/pypi/simple/"
PASSWORD ='qwert'
USERNAME = 'admin'
FIRSTNAME = 'Steven'
LASTNAME = 'Li'  
EMAIL = 'admin@fab.org'
PORT = 8088 
SUPERSET_VER='2.1.0'


# In[ ]:


def check_os():
    """检查操作系统类型"""
    if sys.platform == 'win32':
        if os.environ.get('PROGRAMFILES(X86)'):
            # print('64 bit Windows')
            return  True
        else:
            # print('32 bit Windows')
            raise OSError('32 bit Windows not supported') 
    else:
        return False


# In[ ]:


def get_filename_from_url(url):
    """从URL中获取文件名"""
    if "/" in url:
        filename = url.split("/")[-1]
    return filename 


# In[2]:





# In[50]:

def download(url):
    """下载文件"""
    try:
        filename=get_filename_from_url(url)
        print(f"downloading {filename}")
        if not os.path.exists(filename):
            with urlopen(url, context=unverified_context) as r:
                if r.code !=200:
                    raise DownloadError(f"下载失败，HTTP状态码: {r.code}")
                with open(filename,'wb') as f:
                    f.write(r.read())
        return True
    except Exception as ex:
        print(ex)
        return False


# In[ ]:


if os.path.exists(f"python{ver}._pth"):
    print(f"modify python{ver}._pth")
    with open(f"python{ver}._pth","r") as f:
        txt = f.read().replace("#import","import")

    with open(f"python{ver}._pth","w") as f:
        f.write(txt)


# In[ ]:


# make sure all files download successfully
url = 'https://bootstrap.pypa.io/pip/get-pip.py'
download(url)


# In[ ]:


#f"pip config set global.index-url {MIRROR}"


# In[ ]:


print('installing pip...')

cmd = ['python', 'get-pip.py', '-i', MIRROR]
subprocess.run(cmd, shell=False)


# In[54]:


def install(pkgs):
    """安装Python包"""
    subprocess.check_call([sys.executable, '-m', 'pip', 'install']+pkgs +['-i', MIRROR])


# In[ ]:


def install_python_geohash():
    """安装python_geohash库"""
    if check_os():
        if ver not in ['38','39','310']:
            raise OSError('other Python version is not supported.')
        url =f"https://download.lfd.uci.edu/pythonlibs/archived/python_geohash-0.8.5-cp{ver}-cp{ver}-win_amd64.whl"
        download(url)
        install([f"python_geohash-0.8.5-cp{ver}-cp{ver}-win_amd64.whl"])


# In[ ]:


def install_requirements():
    """安装依赖库"""
    install_python_geohash()
    url=f"https://raw.githubusercontent.com/apache/superset/{SUPERSET_VER}/requirements/base.txt"
    download(url)
    print("modify base.txt")
    with open("base.txt","r") as f:
        txt = (f.read()
               .replace("-e file:.","#-e file:.")
               .replace("pyrsistent==0.16.1","pyrsistent==0.18.1")
              )
    with open(f"requirements.txt","w") as f:
        f.write(txt)
    install(["-r","requirements.txt"])
    install(['apache-superset'])
    install("mysqlclient pymssql psycopg2-binary clickhouse-sqlalchemy pillow".split(" "))

install_requirements()
# In[1]:


def create_secret_key():
    """生成密钥"""
    random_bytes = os.urandom(42) 
    base64_encoded = base64.b64encode(random_bytes)
    return base64_encoded.decode('utf-8')


# In[ ]:
# DATA=b'''
# BOpv^V`Xl0Wn>_9Zy<DNWgtOtVPj}zAX9H<ba!ELWgtdxb#7!~bZKvHASgjoMkye5Ze(S0Aa8DE3L_wIav*JQa%CW6Z*FvQX<~JB
# Z*m}PX=7z>b7df5XL4m_ZDnqBb1ontQ)Oi!bZBKDPES-xLq#BFX>4T*BOqjHb98cPVs&(7WFU8GbZ8)SXlZjGcW-iQAZBlJAYo)=
# X>@6CZeeU7X>Mk3a&2LBX>V={BOr2RXJK+=X>MmAV{dSIa%pF1bRchcZe?<FXlZaRARts|WgtOQMj&iyV`Xl0Wpf~OXlZjGW@&6?
# 3L_wNZy<SZbs%+aWMy(7bZBKDL2zMXXk{QwX=7z>b7d?bR%LQ?X>V>IGA=M6D0FCL3L_vQOlf0fZgXWKDLWu}Z*?GTVR;~KZ*(Aa
# b7dfOXlZjGW@&6?AZ2)CWpH#LX>K56Z*6dFX<=?-WeOu8cWHEJAarPDAWUgvWo~n2E+8OTZ*?GTVR;~LVsv3?ZXjVGV{dSIAa7<M
# bZBKDOlf0fZgXWIVRQ;33L_vOAZT=Sa5^t9cXxL#VQ^t%Xk{*Ma%V4WX=7z>b7gZcOi4pUPE$oKGA=L*BMKuRRc>r$b8{eaWpQ<B
# a%E&7VtF88aBysCV_{-!Wgu)}cOY+aAYo^6Wo2X_bZ;POZXkDZX>@6BXDkXMAaieKba!ELWgui}b98cPVs&(7WFU2JWMy(7bZBKD
# Olf0fZgXWIX>%ZCX>)XPX<~JBWn>_4ZXjW93L_vQK~o?}Qz9TjK~qUnEFf1&R7g)%R3KMDQc^)qR7pisAWu>tLr+dbNmNNsPE#OH
# Mj$~>SqdW{OG!>dEFfiRbZBLAAZ2)Pa%FRKAa8OYX>D+9X=P+CARtp^Wgv8DWgtvxV`Xl0Wgup6av*eQWeOu8b8uy2X=Z6-AZ%f7
# XLVs`Wgus7c4cyIX>MmAaAk6BX>)UFZ*FrSVQyp~Y-w$2bYXO9Z*Fr6BOrBdWMy(7bZBKDOlf0fZgXWW3TbU{Z*p`Xb9r+LX>D+C
# a&#bXb07+7ZE$aLbRckHbZBg8VhU+(aBp&SAaZ32X>D+Ca&#bKVRL0RGzw;NZ*3rRacp61V`yb<c`jvcXK8L_AZcxIZ*p`XV{&C-
# bY)*<Zf9w3WeRU|E@f_ZX>xCFTPH?LK~qa#K~PX9T_8OmCv$ahWpZ<6bSDZ53S?zwAY*c6VRU6*b7f<4WprO_WqBwmItm~lARuyK
# Ze(w5Ut)Q5Wpf}sAa8Rnb#h^DWN&RKG%_h53LqdLAYx&2Wi~WlWo~0{WMyO^Js@IXb7eL(E@Cz`Wo~0{WMwFFVQyq^ZC_$}bY*iX
# 3LqdLAaZ4Nb#iVXVqtS-HZ)&lZewp`Wn?a7Wn*t-Whf_gbY?9$Cn*XFW^!+BAaiwaWpZ<6bS`6WZf0p`AZcxIZ*p`XRz*@%Nl#8+
# Q&dt(PDcu9W*}BYQd3D!PG3`0Qb|rnAUq%^F)lSOFef?+ARr(hW^!+BAaiwaWpZ<6bS`6TX&`BBaBp&SAaiwaWpZ<6bP8o`b7eXT
# ARr(hW^!+BAaiwaWpZ<6bS`6TX)bMHX>K5CZE$aLbRcteaAk6HWpoM(WMyU`X>MtBC@DG$ARr(hX=WgBVRUG0X<{x=VRUFHB6D?c
# WpZ<6bYEj{Zf0p`E^v7wDK2GrX>)XQC@DG$ARr(hARr(ha%FUNa&90BARr(h3LqdLAaG%HXdpdsVRUG0X<{x=VRUFHA}%5+E@5JG
# Z)|mRWhf~wVRK(_Z*ysQC@BgcARr(LARr(hWgtBuV{&C-bY)*<Zf9w3Whf_eacpUHWjZe}FLQNpWpZ<6bS`9KCn*XbARr(kAmxap
# =9aDKp{VAVujP=Y<*k_IoTv&QARr)gVPb4$Ut?%xV{0HiAZ0FPcx7XCbY&<aQ$<WgLsTGcVQpm~Mp92rAaikSX>?^@ZDDhCWpW@_
# NJUabAar?fWj!Z!VPb4$Cm=yiL?CWqZDl<tWMXqCJ0dAAW@U6^Xm4(1C@BgcARr)VW*~H7Vr*q!V`yb#YdQ)bARr(hARr(kAn2i}
# <*k_IoT%@-jOB=#=8321p^WC6wC0wu=97)&y_^alARr(hARr)RE@gOSV|8?8C}tvcaAaY0Wgui?b0BkNbRctaY+-C;Xk~4AUv+Y6
# JtuQ<Y-x05IxjCTdvIZNXnikpb#P^Jb7gccWMU^GDGDGUARuLIb7eXTARr(hARr(hBOvIZsN}ef<*k_IoT%@-jOB=#<hYIIiKpnH
# jO4q!<h_;Vla1uPoC+WyARr(hARusIb8{ddARr1LARr(LARr(hcWHEJAa8JGZYU>nb#P^Jb7gd2V{dL|X=g5Qc_%C<cPA+zVRIm6
# X>4UW3LqdLARr(hAZBT7WiEGeX>?^MW+EaY3TbU{Z*p`XaA9<4Y-wT&X=WgBVRUG0X<{x=VRUFHB6D?cWpZ<6bYEj{Zf0p`UuAeM
# aCssrE@gOWb98ekDLM)uARr)Sa&K)Qb9HcKa&u*LUt@1>W@%?%Wq2TIZE$aLbRa4UQ$<5kMO0r)MOh#{AR>EXa%Ew3WnXh;V{&D5
# Uu$J~C@Fm+ARr(h3LqdLARr(hAR;0nDGDGUARr(hARuOGY-KKYa%psBC?Z^LA}I<WARr(hARr)SX>4UKcXDZTWhiDRQ&CJoOhZUT
# O<7+=K~zCPK~qIvRZ>YHJs=`;acpUHWjZe}FMDudbZC7qb9HcKa&u*LE@WaNCn*XFWMyU`ZDDC{C@DG$ARr(hX>MtBC@BgcARr)f
# d2=pda%Xm1FkK)$AaZ3cb9G`UawjM)b7OL8aCBTQaCvupTrOpJWhp--CoCW*CoCXyd2=pda%Xm1FkLAMARr(hb9r+vWq4_HD06ji
# WpZ<6bSNn)3LqdLAPQ+_AYWf@VQpn!Um!g_ASYj6ZDDC{UtcFW3LqdLAZ=l3ZYU`

# '''
# with open('app.py','wb') as f:
#     f.write(b85decode(DATA.replace(b"\n", b"")))
url = "https://raw.githubusercontent.com/alitrack/superset_app/master/app.py"
download(url)
url = "https://raw.githubusercontent.com/alitrack/superset_app/master/superset_config_ex.py"
download(url)


# In[ ]:

def init_db():
    subprocess.run(f'python app.py --help'.split(' '), shell=True)
    subprocess.run(f'python app.py db upgrade'.split(' '), shell=True)
    subprocess.run(f'python app.py fab create-admin --password {PASSWORD} --username {USERNAME} --firstname {FIRSTNAME} --lastname {LASTNAME} --email {EMAIL}'.split(' '), shell=True)
    subprocess.run(f'python app.py init'.split(' '), shell=True)
init_db()

# In[ ]:


run_cmd = f"""
python app.py run -p {PORT} --with-threads --reload --debugger
pause
"""
with open('run.cmd','w') as f:
    f.write(run_cmd)

