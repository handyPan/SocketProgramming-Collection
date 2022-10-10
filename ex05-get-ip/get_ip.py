# Author: Handy Pan
# Date: Feb 11, 2022

import socket

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

print("%s is at %s"%(hostname,local_ip))
print()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print(s.getsockname())
print()

def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:       
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP
print(extract_ip())
print()

from netifaces import interfaces, ifaddresses, AF_INET
for ifaceName in interfaces():
    addresses = [ifaceName + " - " + i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
    print(' '.join(addresses))