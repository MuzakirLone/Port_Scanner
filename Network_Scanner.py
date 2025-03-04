import socket
import threading

def scan_port(ip, port, open_ports):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((ip, port))
        if result == 0:
            print(f"Port {port} is open.")
            open_ports.append(port)
        sock.close()
    except KeyboardInterrupt:
        print("Scan interrupted by user.")
        exit()
    except socket.timeout:
        print(f"Timeout on port {port}.")
    except socket.error as err:
        print(f"Error on port {port}: {err}")
    finally:
        sock.close()

def main():
    ip = input("Enter the target IP address: ")
    start_port = int(input("Enter the start port: "))
    end_port = int(input("Enter the end port: "))
    
    print(f"Scanning {ip} from port {start_port} to {end_port}...")
    open_ports = []
    threads = []
    
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(ip, port, open_ports))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()
    
    if open_ports:
        print("Open ports:", ', '.join(map(str, open_ports)))
        with open("scan_results.txt", "w") as f:
            f.write(f"Open ports on {ip}: " + ', '.join(map(str, open_ports)) + "\n")
    else:
        print("No open ports found in the given range.")
        
if __name__ == "__main__":
    main()
