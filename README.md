# Nmap_tools
nmap结果处理工具
根据xml输出文件，处理nmap探测到的端口信息，并对所有端口进行web服务探测,需要在运行目录下创建result文件夹

USAGE：
* 解析nmap xml结果

python3 nmap_tools -f xxx.xml 
* 解析nmap xml结果并对所有已开放端口进行Web探测

python3 nmap_tools -f xxx.xml -w 1 -t 30
