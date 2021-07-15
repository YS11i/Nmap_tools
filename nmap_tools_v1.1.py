import csv
import time
import sys
from xml.etree.ElementTree import XML
import requests
import datetime
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup as bs
from requests.packages.urllib3.exceptions import InsecureRequestWarning
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
Time = datetime.datetime.now().strftime('%Y-%m-%d')
#print(Time)

def GetFile(path):  # 获取文件
    Date_list = []
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        #print(root.tag)
        # print(Item)
    except Exception as e:
        print(e)
        return {}
    
    for host in root.findall('host'):
        if host.find('status').get('state') == 'down':
            continue
        #print(host)
        address = host.find('address').get('addr',None)
        #print(address)
        if not address:
            continue
        
        ports = []
        for port in host.iter('port'):
            state = port.find('state').get('state','')
            portid = port.get('portid',None)
            serv = port.find('service')
            serv = serv.get('name')
            if serv == "":
                serv == "未知"
            #print(state,portid,serv)
            ports.append({'IP':address,'PORT':portid,'STATUS':state,'SERVICE':serv})
        return(ports)

              

def MkdirFile(Date_list):
    with open(Time+'.csv','w',newline='') as csvf:
        fieldnames = ['IP','PORT','STATUS','SERVICE','CODE','TITLE']
        writer = csv.DictWriter(csvf,fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(Date_list)
        print("文件输出成功！")

def GetTitle(ip,port):
    MyUa = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
    try:
        Myurl = "http://"+ip+":"+port
        headers = {'User-Agent': MyUa,'Connection': 'close'}
        r = requests.get(url=Myurl, verify=False, headers=headers, timeout=3)
        soup = bs(r.text.encode('utf-8'), 'html.parser')
        title = soup.find('title').text
        #print(r.status_code)
        code = r.status_code
        if code != 400 and soup != "":
            print(Myurl + " It is Web title:" + title)
            return(code,title)
        elif code == 400:
            Myurl2 = "https://"+ip+":"+port
            headers = {'User-Agent': MyUa,'Connection': 'close'}
            r = requests.get(url=Myurl2, verify=False, headers=headers, timeout=3)
            soup = bs(r.text.encode('utf-8'), 'html.parser')
            title = soup.find('title').text
            print(Myurl2 + " It is Web title:" + title)
            return(code,title)

        else:
            return(code,title)
            
    except:
        print("http://"+ip+":"+port+"  Network Error!")
        title = "Network Error!"
        code = '无'
        return(code,title)

def main():
    if len(sys.argv) != 2:
        print("----------------USEAGE:python3 nmap_tools path -----------------")
        sys.exit()
    path = sys.argv[1]
    #GetFile(path)
    #T = int(sys.argv[2])
    start_time = time.time()
    
    port = GetFile(path)

    #print(port)
    for j in port:
        a = j['IP']
        b = j['PORT']
        code,title = GetTitle(a,b)
        NewKey1 = 'CODE'
        NewKey2 = 'TITLE'
        j[NewKey1] = code
        j[NewKey2] = title

    #print(port)
    MkdirFile(port)

    print("用时:%s second"%(time.time() - start_time) )

if __name__ == '__main__':
    main()


