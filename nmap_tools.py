import csv,threadpool,time,sys,requests,datetime,threading,argparse
from bs4 import BeautifulSoup as bs
from requests.packages.urllib3.exceptions import InsecureRequestWarning
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
Time = str(int(time.time()))

CODE = []

def parse_args():
    parser = argparse.ArgumentParser(epilog='\tExample: \r\npython3 ' + sys.argv[0] + " -f test.xml -w 1 -t 20")
    parser.add_argument("-f", "--file", help="The xml file path")
    parser.add_argument("-w", "--webfind", help="Web find")
    parser.add_argument("-t", "--threads", help="Web find threads")
    return parser.parse_args()

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
            #print(address,portid)
            try:
                serv = port.find('service').get('name','')
                #serv = serv.get('name')
                #print(serv)
            except:
                continue

            if serv == "":
                serv == "未知"
            #print(state,portid,serv)
            ports.append({'IP':address,'PORT':portid,'STATUS':state,'SERVICE':serv})
    return(ports)             

def MkdirFile(Date_list):
    with open('result/'+Time+'.csv','w',newline='') as csvf:
        fieldnames = ['IP','PORT','STATUS','SERVICE','URL','CODE','TITLE']
        writer = csv.DictWriter(csvf,fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(Date_list)
        print("文件输出成功！")

def GetTitle(url): 
    MyUa = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
    try:
        headers = {'User-Agent': MyUa,'Connection': 'close'}
        r = requests.get(url=url, verify=False, headers=headers, timeout=10)
    except:
        title = "Network Error!"
        code = 'NONE'
        CODE.append({'URL':url,'CODE':code,'TITLE':title})
        #print(url+" ------ "+"请求失败"+" ------ Network Error!")
        print("{:<40s}请求失败{:<20s}{:>20s}".format(url,"","Network Error!"))
        return(CODE)

    if r.apparent_encoding != None:
        encodeType = r.apparent_encoding
        res = r.content.decode(encodeType,'ignore')
    else:
        res = r.text

    soup = bs(res, 'html.parser')
    code = r.status_code
    if soup.title:
        title = str(soup.title.string)
        #print(title)
    else:
        title = "Web存在但无标题"    
    #print(r.status_code)        
    if code != 400 and soup != "":
        #print(url + " ------ 发现Web ------ title:" + title)
        print("{:<40s}发现Web{:>20s}title:{:<40s}".format(url,"",title))
        CODE.append({'URL':url,'CODE':code,'TITLE':title})
        return(CODE)
    elif code == 400:
        url = "https://"+url.strip('http://')
        #print(url)
        headers = {'User-Agent': MyUa,'Connection': 'close'}
        r = requests.get(url=url, verify=False, headers=headers, timeout=10)
        code = r.status_code
        soup = bs(r.text.encode('utf-8'), 'html.parser')
        
        if soup.title:
            title = str(soup.title.string)
            #print(title)
        else:
            title = "Web存在但无标题"   
        
        print("{:<40s}发现Web{:>20s}title:{:<40s}".format(url,"",title))

        CODE.append({'URL':url,'CODE':code,'TITLE':title})
        return(CODE)

    else:
        CODE.append({'URL':url,'CODE':code,'TITLE':title})
        return(CODE)


if __name__ == '__main__':
    args = parse_args()
    path = args.file
    start_time = time.time()
    if args.file == None:
        print('\tExample: \r\npython3 ' + sys.argv[0] + " -f test.xml -w 1 -t 20")
        exit()
    #解析xml模块
    MyUrl = GetFile(path)
    url = []
    for u in MyUrl:
        a = u['IP']
        b = u['PORT']
        c = u['STATUS']
        d = u['SERVICE']
        url.append("http://"+a+":"+b)

    #web探测模块
    if args.webfind == None:
        MkdirFile(MyUrl)
        print("用时:%.2f 秒"%(time.time() - start_time) )
    else:
        if args.threads == None:
            #默认线程30
            T = 30 
        else:
            T = int(args.threads)
   
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
        MkdirFile(MyUrl)
        print("用时:%.2f 秒"%(time.time() - start_time) )