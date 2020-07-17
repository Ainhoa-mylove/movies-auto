from socket import *
import sys

PORT=8888
HOST='127.0.0.1'
ADDR=(HOST,PORT)
s=socket()
s.connect(ADDR)

def do_register():
    while True:
        name=input('User name:')
        passwd1=input('Passwd:')
        passwd2=input('Try again:')
        if(' 'in name)or(' 'in passwd1):
            print('用户名与密码不能有空格')
        if passwd1!=passwd2:
            print('两次输入的密码不一致')
            continue
        msg='R %s %s'%(name,passwd1)
        s.send(msg.encode())
        data=s.recv(128).decode()
        if data=='OK':
            print('注册成功')
            two_page(name)
        else:
            print('注册失败')

def do_login():
    name=input('User ID:')
    passwd=input('passwd:')
    if(' 'in name)or(' 'in passwd):
        print('用户名与密码不能有空格')
    msg='L %s %s'%(name,passwd)
    s.send(msg.encode())
    data=s.recv(128).decode()
    if data=='OK':
        print('登录成功！')
        two_page(name)
    else:
        print('登陆失败！')
    return

def two_page(name):
    while True:
        print("""
           =======================================
           1.抓取           2.查询           3.退出
           =======================================
        """)
        return

def main():
    print("""
    ======================================
    1.注册           2.登录           3.注销
    ======================================
    """)
    while True:
        cmd=input('请输入选项:')
        if cmd=='1':
            do_register()
        elif cmd=='2':
            do_login()
        elif cmd=='3':
            s.send(b'E')
            print('谢谢使用')
            return

if __name__ == '__main__':
    main()
