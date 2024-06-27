import socket

HOST = '10.0.0.2'  # 服務器 IP 地址
PORT = 65432        # 通信端口

# 創建 socket 對象
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # 嘗試連接到服務器
    s.connect((HOST, PORT))
    # 發送消息給服務器
    while True:
        msg = input()
        if msg == '0':
            break
        s.sendall(msg.encode())
    # 接收服務器的回覆
    data = s.recv(1024)

print('Received', repr(data))
