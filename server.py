from socket import *
from opreation_db import *
import sys
from threading import Thread


PORT=8888
HOST='127.0.0.1'
ADDR=(HOST,PORT)

def do_register(c,db,data):
    tmp=data.split(' ')
    name=tmp[1]
    passwd=tmp[2]
    if db.do_register(name,passwd):
        c.send(b'OK')
    else:
        c.send(b'False')

def do_login(c,db,data):
    tmp=data.split(' ')
    name=tmp[1]
    passwd=tmp[2]
    if db.do_login(name,passwd):
        c.send(b'OK')
    else:
        c.send(b'False')

def handle(c,db):
    db.create_cur()
    while True:
        data=c.recv(1024).decode()
        print(c.getpeername(),":",data)
        if not data or data[0]=='E':
            c.close()
            sys.exit('服务退出！！')
        elif data[0]=="R":
            do_register(c,db,data)
        elif data[0]=='L':
            do_login(c,db,data)
        elif data[0]=='E':
            c.close()
            sys.exit('客户端退出！！')

def main():
    db=Database()
    s=socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(5)
    print('Listen the port 8888')
    while True:
        try:
            c,addr=s.accept()
            print('Connect from:',addr)
        except KeyboardInterrupt:
            s.close()
            sys.exit('服务退出')
        except Exception as e:
            print(e)
            continue
        t=Thread(target=handle,args=(c,db))
        t.daemon=True
        t.start()
if __name__ == '__main__':
    main()

