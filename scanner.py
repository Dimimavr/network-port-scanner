import socket
import threading
from datetime import datetime
from ipaddress import ip_network
from concurrent.futures import ThreadPoolExecutor

# Λίστα για την αποθήκευση των αποτελεσμάτων
open_ports = {}

# Συνάρτηση για τη σάρωση μιας θύρας
def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = sock.connect_ex((str(ip), port))

        if result == 0:
            print(f"Port {port} is open on {ip}")
            if ip not in open_ports:
                open_ports[ip] = []
            open_ports[ip].append(port)
        sock.close()

    except Exception as e:
        print(f"Error scanning port {port} on {ip}: {str(e)}")

# Συνάρτηση που χρησιμοποιεί ThreadPoolExecutor για τη σάρωση θυρών
def scan_ports(ip, start_port, end_port):
    with ThreadPoolExecutor(max_workers=100) as executor:
        for port in range(start_port, end_port + 1):
            executor.submit(scan_port, ip, port)

# Συνάρτηση για σάρωση εύρους IP χρησιμοποιώντας ThreadPoolExecutor
def scan_ip_range(network, start_port, end_port):
    start_time = datetime.now()

    with ThreadPoolExecutor(max_workers=10) as executor:
        for ip in network:
            executor.submit(scan_ports, ip, start_port, end_port)

    end_time = datetime.now()
    total_time = end_time - start_time
    print(f"\nScan completed in: {total_time}")

    # Εμφάνιση των αποτελεσμάτων
    print("\nOpen ports for each IP:")
    for ip, ports in open_ports.items():
        print(f"{ip}: {', '.join(map(str, ports))}")

# Συνάρτηση για αποθήκευση αποτελεσμάτων σε αρχείο
def save_results_to_file(log_filename):
    with open(log_filename, "w") as file:
        for ip, ports in open_ports.items():
            file.write(f"{ip}: {', '.join(map(str, ports))}\n")
    print(f"\nResults saved to {log_filename}")

# Κεντρική λειτουργία
if __name__ == "__main__":
    # Ζήτηση στοιχείων από τον χρήστη
    start_ip = input("Enter the network IP address (e.g., 192.168.1.0): ")
    subnet_mask = input("Enter the subnet mask (e.g., /24): ")
    start_port = int(input("Enter the start port: "))
    end_port = int(input("Enter the end port: "))
    log_filename = input("Enter the name of the log file (e.g., scan_results.txt): ")

    # Δημιουργία του εύρους IPs με βάση το δίκτυο και το subnet mask
    network = ip_network(f"{start_ip}{subnet_mask}", strict=False)

    # Ξεκινάμε τη σάρωση
    scan_ip_range(network, start_port, end_port)

    # Αποθήκευση αποτελεσμάτων
    save_results_to_file(log_filename)
