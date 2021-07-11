import re
import sys
import requests
import datetime
from bs4 import BeautifulSoup as bs
from requests.packages.urllib3.exceptions import InsecureRequestWarning
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
time = datetime.datetime.now().strftime('%Y-%m-%d')
print(time)
f = open(time + '.csv', 'a')


def GetFile(path):  # 获取文件
    tree = ET.parse(path)
    root = tree.getroot()
    # print(root)
    # print(Item)
    ip_list = []
    for host in root.findall('host'):
        # print(host)
        if host[0].get('state') == "up":  # 判断第一个host中第一个state是否为up
            ip = host[1].get('addr')
            print(ip)
            ip_list.append(ip)
            Line_ip = ip
            f.writelines(Line_ip)
            # print(host[3][1:])
            for port in host[3][1:]:
                # print(port.get('portid'))
                Line_portid = str(port.get('portid'))
                GetTitle(Line_ip,Line_portid)



def GetTitle(ip,port):
    # MyUa = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"

    try:
        Myurl = "http://"+ip+":"+port
        headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
        'Connection': 'close'}
        r = requests.get(url=Myurl, verify=False, headers=headers, timeout=3)
        soup = bs(r.text.encode('utf-8'), 'html.parser')
        title = soup.find('title').text
        #print(r.status_code)
        if r.status_code == 200 and soup != "":
            print(Myurl + " It is Web title:" + title)
            f.writelines(r.status_code)
            f.writelines(title)
        elif r.status_code == 400:
            Myurl2 = "https://"+ip+":"+port
            headers = {
                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
                'Connection': 'close'}
            r = requests.get(url=Myurl2, verify=False, headers=headers, timeout=3)
            soup = bs(r.text.encode('utf-8'), 'html.parser')
            title = soup.find('title').text
            print(Myurl2 + " It is Web title:" + title)
            f.writelines(r.status_code)
            f.writelines(title)

        else:
            print(r.status_code)
            f.writelines(r.status_code)
            f.writelines(title)
    except:
        print("Network Error!")
        f.writelines("Network Error!")


if len(sys.argv) != 2:
    print("----------------USEAGE:python3 nmap_tools path-----------------")
    sys.exit()
path = sys.argv[1]
GetFile(path)
