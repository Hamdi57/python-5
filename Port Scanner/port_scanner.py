import socket
import sys
import time
import threading

usage = "python3 port_scaner.py TARGET START_PORT END_PORT"
print("*"*70)
print("Port Scanner")
print("*"*70)
start_time = time.time()

# if user is not giving 4 arguments, then print the usage and exit
if (len(sys.argv) != 4):
    print(usage)
    sys.exit()

try:
    target = socket.gethostbyname(sys.argv[1])
except socket.gaierror:
    print("Name Resolution Error")
    sys.exit()

start_port = int(sys.argv[2])
end_port = int(sys.argv[3])
print("Scanning target", target)
def scan_port(port):
   # print("Scanning", port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn = s.connect_ex((target, port))
    if(not conn):
        print("Port {} is OPEN".format(port))
    s.close()
for port in range(start_port, end_port + 1):
    thread = threading.Thread(target = scan_port, args = (port,))
    thread.start()

end_time = time.time()
print("Time Ellapsed:", end_time - start_time, "sec")

<!--Use a multiprocessing pool instead of threads. This will allow you to scan multiple ports simultaneously, which will significantly improve the performance of the scanner.
Use a more efficient way to check if a port is open. The current code uses the connect_ex() method, which can be slow for some ports. You can use the getservbyport() method instead, which is faster.
Avoid printing the message "Scanning" for each port. This is unnecessary and can slow down the scanner.
Here is the optimized code:-->
import socket
import sys
import time
import multiprocessing

usage = "python3 port_scaner.py TARGET START_PORT END_PORT"
print("*"*70)
print("Port Scanner")
print("*"*70)
start_time = time.time()

# if user is not giving 4 arguments, then print the usage and exit
if (len(sys.argv) != 4):
    print(usage)
    sys.exit()

try:
    target = socket.gethostbyname(sys.argv[1])
except socket.gaierror:
    print("Name Resolution Error")
    sys.exit()

start_port = int(sys.argv[2])
end_port = int(sys.argv[3])
print("Scanning target", target)

def scan_port(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn = s.connect_ex((target, port))
    if(not conn):
        return 1
    return 0

pool = multiprocessing.Pool(processes=4)
results = pool.map(scan_port, range(start_port, end_port + 1))

for i in range(len(results)):
    if results[i]:
        print("Port {} is OPEN".format(i + start_port))

end_time = time.time()
print("Time Ellapsed:", end_time - start_time, "sec")
