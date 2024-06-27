import subprocess

def ping_host():
    for ipFix in range(1,5):
        host = '10.0.0.'+str(ipFix)
        result = subprocess.run(['ping', '-c', '1', host], stdout=subprocess.PIPE)
        if result.returncode == 0:
            print(f"{host} is reachable")
        else:
            print(f"{host} is unreachable")

ping_host()