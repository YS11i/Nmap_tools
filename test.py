import csv
import time
import sys
import requests
import datetime
import threading
import threadpool
from bs4 import BeautifulSoup as bs
from requests.packages.urllib3.exceptions import InsecureRequestWarning
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
Time = datetime.datetime.now().strftime('%Y-%m-%d')
#print(Time)
CODE = []

def GetFile(path):  # 获取文件
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        #print(root.tag)
        # print(Item)
    except Exception as e:
        print(e)
        return {}
    ports = []
    for host in root.findall('host'):
        
        if host.find('status').get('state') == 'down':
            continue
        #print(host)
        address = host.find('address').get('addr',None)
        #print(address)
        if not address:
            continue
        
        
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
        fieldnames = ['IP','PORT','STATUS','SERVICE','URL','CODE','TITLE']
        writer = csv.DictWriter(csvf,fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(Date_list)
        print("文件输出成功！")

def GetTitle(url): 
    MyUa = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"   
    try:
        headers = {'User-Agent': MyUa,'Connection': 'close'}
        r = requests.get(url=url, verify=False, headers=headers, timeout=5)
        soup = bs(r.text.encode('utf-8'), 'html.parser')
        title = soup.find('title').text
        #print(r.status_code)
        code = r.status_code
        if code != 400 and soup != "":
            print(url + " ------ 发现Web ------ title:" + title)
            CODE.append({'URL':url,'CODE':code,'TITLE':title})
            return(CODE)
        elif code == 400:
            url2 = "https://"+url.strip('http://')
            headers = {'User-Agent': MyUa,'Connection': 'close'}
            r = requests.get(url=url2, verify=False, headers=headers, timeout=5)
            code = r.status_code
            soup = bs(r.text.encode('utf-8'), 'html.parser')
            title = soup.find('title').text
            print(url2 + " ------ 发现Web ------ title:" + title)

            CODE.append({'URL':url2,'CODE':code,'TITLE':title})
            return(CODE)

        else:
            CODE.append({'URL':url,'CODE':code,'TITLE':title})
            return(CODE)
            
    except:
        title = "Network Error!"
        code = '无'
        CODE.append({'URL':url,'CODE':code,'TITLE':title})
        print(url+" ------ "+"请求失败"+" ------ Network Error!")
        return(CODE)


if __name__ == '__main__':
    if len(sys.argv) != 3:
            print("----------------USEAGE:python3 nmap_tools path threads-----------------")
            print("----------------example:python3 nmap_tools 1.xml 10--------------------")
            sys.exit()
    path = sys.argv[1]
    start_time = time.time()
    T = int(sys.argv[2])
    MyUrl = GetFile(path)
    url = []
    for u in MyUrl:
        a = u['IP']
        b = u['PORT']
        c = u['STATUS']
        d = u['SERVICE']
        url.append("http://"+a+":"+b)
    #print(url)
   
    pool = threadpool.ThreadPool(T)
    threading = threadpool.makeRequests(GetTitle,url)
    [pool.putRequest(req) for req in threading]
    pool.wait()
    N = 0
    for d in MyUrl:
    #print(d)
        key1 = 'URL'
        key2 = 'CODE'
        key3 = 'TITLE'
        c1 = CODE[N]['URL']
        c2 = CODE[N]['CODE']
        c3 = CODE[N]['TITLE']
        #print(c1,c2)
        d[key1] = c1
        d[key2] = c2
        d[key3] = c3
        N += 1
    #print(MyUrl)
    MkdirFile(MyUrl)
    print("用时:%s second"%(time.time() - start_time) )