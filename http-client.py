import socket;from os import system;system("cls");from sys import argv,exit
from dns import resolver
def getFil(link):
	if "http://" not in link or "https://" not in link:
		if link.count("/") > 0:c=[i for i, n in enumerate(link) if n=="/"][0];return c
		else:return "/"
	else:
		if link.count("/") > 2:c=[i for i, n in enumerate(link) if n=="/"][2];return c
		else:return "/"

if len(argv) == 1: #only file
	if argv[1] == "-d":exit()
	elif argv[1] == "help":print("how to exec this file:\n\npython httpclient.py [HTTP request type] [website] [port] (data)");exit()
	else:typ="get";th="google.com";target_port=80;data={};n=False
elif len(argv) == 2: #HTTP request type
	th="google.com";target_port=80;data={}
	if argv[1] == "-d":n=True;typ="get"
	else:n=False;typ=argv[1]
elif len(argv) == 3: #website domain
	if argv[2] == "-d":typ=argv[1];n=True;th="google.com";target_port=80;data={}
	else:n=False;th=argv[2]
elif len(argv) == 4: #port
	th=argv[2]
	if argv[3] == "-d":n=True;target_port = 80;data={}
	elif argv[3] not in ["80", "443", "8080"]:exit() #if not HTTP or HTTPS port(except -d)
	else:n=False;target_port = int(argv[3]);data={}
elif len(argv) == 5:
	th=argv[2];target_port=int(argv[3])
	if argv[4] == "-d" or ("{" not in argv[4] and "}" not in argv[4]): data = {};n=True #check for -d or no data
	else:n=False;data = argv[4].replace('"',"'")
typ=argv[1];client = socket.socket(socket.AF_INET, socket.SOCK_STREAM);print("set up socket")   
try:
	v=getFil(th)
	if v != "/":n=th[:v];x=th[v:]
	else:x="/";n = th
	target_host = resolver.Resolver().resolve(n,'A').rrset[0].to_text()
	#connect the client to website
	print("connecting to website");client.connect((target_host,target_port))  
	if target_port == 80 or target_port == 8080:i="HTTP"
	elif target_port == 443:i = "HTTPS"
	else:i="HTTP"
	# send some data
	request = "{} {} {}/1.1\r\nHost: {}\r\nUser-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36\r\nContent-Type: application/json\r\nConnection:close\r\nContent-Length: 0\r\n\r\n{}".format(typ.upper(),x,i,n,data)
	print("sending request:\n{}\n----------".format(request));client.send(request.encode())
	response = client.recv(4096);print("response from host \"{}\":\n{}".format(n, response.decode("utf-8")))
except Exception as e:
	a=list(str(type(e)));a="".join(a[a.index(" "):a.index(">")]);a=a.replace("'","")
	if n:print("somehow this client failed ({} \"{}\")".format(a.strip(),e))
	else:print("somehow this client failed ({})".format(a.strip()))
