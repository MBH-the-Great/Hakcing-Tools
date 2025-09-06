import os, platform, socket, psutil, getpass, subprocess
from datetime import datetime
from scapy.all import ARP, Ether, srp

report = ""

def add_to_report(title, content):
    global report
    report += f"\n=== {title} ===\n"
    if isinstance(content, list):
        for item in content:
            report += f"{item}\n"
    elif isinstance(content, dict):
        for k, v in content.items():
            report += f"{k}: {v}\n"
    else:
        report += str(content) + "\n"

def run_cmd(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, text=True).strip()
    except:
        return "[ERROR]"

def get_system_info():
    return {
        "Date & Time": str(datetime.now()),
        "OS": f"{platform.system()} {platform.release()}",
        "Architecture": platform.machine(),
        "Hostname": socket.gethostname(),
        "Username": getpass.getuser(),
        "Processor": platform.processor(),
        "Boot Time": datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"),
        "CPU Cores": psutil.cpu_count(logical=False),
        "Logical CPUs": psutil.cpu_count(logical=True),
        "RAM (GB)": round(psutil.virtual_memory().total / (1024**3), 2),
    }

def get_ip_addresses():
    results = []
    addrs = psutil.net_if_addrs()
    for iface, addr_list in addrs.items():
        for addr in addr_list:
            if addr.family == socket.AF_INET:
                results.append(f"{iface}: {addr.address}")
    return results

def get_active_connections():
    conns = []
    for conn in psutil.net_connections(kind='inet'):
        laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "-"
        raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "-"
        conns.append(f"{laddr} -> {raddr} | {conn.status}")
    return conns

def arp_scan(ip_range):
    results = []
    try:
        packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip_range)
        ans = srp(packet, timeout=2, verbose=0)[0]
        for _, rcv in ans:
            results.append(f"IP: {rcv.psrc} | MAC: {rcv.hwsrc}")
    except Exception as e:
        results.append(f"[ARP ERROR] {str(e)}")
    return results

def get_wifi_passwords():
    if platform.system() != "Windows":
        return ["[Unsupported on non-Windows OS]"]
    results = []
    profiles = run_cmd("netsh wlan show profiles").splitlines()
    for line in profiles:
        if "All User Profile" in line:
            profile = line.split(":")[1].strip()
            pw = run_cmd(f'netsh wlan show profile name="{profile}" key=clear')
            for pw_line in pw.splitlines():
                if "Key Content" in pw_line:
                    results.append(f"{profile}: {pw_line.split(':')[1].strip()}")
                    break
            else:
                results.append(f"{profile}: [NO PASSWORD FOUND]")
    return results

def get_installed_programs():
    if platform.system() != "Windows":
        return ["[Unsupported on non-Windows OS]"]
    output = run_cmd('powershell "gps | where {$_.MainWindowTitle} | select Description"')
    return [line.strip() for line in output.splitlines() if line.strip() and "Description" not in line]

def search_sensitive_files():
    results = []
    user_home = os.environ["USERPROFILE"]
    dirs = [os.path.join(user_home, "Documents"), os.path.join(user_home, "Desktop")]
    keywords = ['password', '.env', 'secret', 'database', 'db', 'config']
    for d in dirs:
        for root, _, files in os.walk(d):
            for f in files:
                if any(k in f.lower() for k in keywords):
                    results.append(os.path.join(root, f))
    return results

# === RUNNING EVERYTHING ===
add_to_report("SYSTEM INFO", get_system_info())
add_to_report("NETWORK IP ADDRESSES", get_ip_addresses())
add_to_report("ACTIVE CONNECTIONS", get_active_connections())
add_to_report("WIFI PASSWORDS", get_wifi_passwords())
add_to_report("INSTALLED PROGRAMS", get_installed_programs())
add_to_report("SENSITIVE FILES FOUND", search_sensitive_files())

# === Optional ARP Scan ===
ip_input = input("\nEnter IP range for ARP scan (e.g. 192.168.1.1/24), or press Enter to skip: ")
if ip_input.strip():
    add_to_report("ARP SCAN RESULTS", arp_scan(ip_input.strip()))

# === SAVE REPORT ===
with open("recon_report.txt", "w", encoding="utf-8") as f:
    f.write(report)

print("\n Recon complete. Results saved to recon_report.txt")
