import socket
import time
import random


client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP


# Enable broadcasting mode
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

client.bind(("", 37020))

#initialize a dict to keep track of recv message counts
message_count = {}

#define a threshold for counter-based scheme
COUNTER_THRESHOLD = 3



while True:
    # Thanks @seym45 for a fix
    data, addr = client.recvfrom(1024)
    message = data.decode()

    if message in message_count:
        message_count[message] += 1
    else:
        message_count[message] = 1
    
    print("received message: %s from %s"%message %addr)

    #if counter is below threshold, schedule rebroadcast

    if message_count[message] < COUNTER_THRESHOLD:
        # small random delay before rebroadcast
        time.sleep(random.uniform(0.1, 0.4))
        client.sendto(data, ("192.168.4.255", 37020))
        print(f"rebroadcasting message: {message}")