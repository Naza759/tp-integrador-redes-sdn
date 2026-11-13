import requests

BASE_URL = "http://localhost:58000/api/v1"
CREDENTIALS = {
    "username": "cisco",
    "password": "class"
}

def main():
    print("Conectando con el Network Controller...")
    auth_resp = requests.post(f"{BASE_URL}/ticket", json=CREDENTIALS)
    auth_resp.raise_for_status()
    ticket = auth_resp.json()["response"]["serviceTicket"]
    print(f"Ticket obtenido: {ticket}\n")

    headers = {"X-Auth-Token": ticket}

    # Consultar dispositivos de red
    dev_resp = requests.get(f"{BASE_URL}/network-device", headers=headers)
    dev_resp.raise_for_status()
    devices = dev_resp.json()["response"]

    print("=== DISPOSITIVOS DE RED DESCUBIERTOS ===")
    print(f"{'HOSTNAME':<12} {'IP GESTIÓN':<16} {'PLATAFORMA':<14} {'ROL':<14} {'ESTADO'}")
    print("-" * 74)
    for dev in devices:
        hostname = dev.get("hostname", "N/A")
        ip = dev.get("managementIpAddress", "N/A")
        platform = dev.get("platformId", "N/A")
        role = dev.get("role", "UNKNOWN")
        status = dev.get("collectionStatus", "N/A")
        print(f"{hostname:<12} {ip:<16} {platform:<14} {role:<14} {status}")

    # Consultar hosts conectados
    host_resp = requests.get(f"{BASE_URL}/host", headers=headers)
    host_resp.raise_for_status()
    hosts = host_resp.json()["response"]

    print("\n=== HOSTS FINALES CONECTADOS ===")
    print(f"{'HOST':<12} {'IP':<16} {'MAC':<18} {'EQUIPO CONECTADO':<18} {'INTERFAZ'}")
    print("-" * 82)
    for h in hosts:
        name = h.get("hostName", "N/A")
        ip = h.get("hostIp", "N/A")
        mac = h.get("hostMac", "N/A")
        switch = h.get("connectedNetworkDeviceName", "N/A")
        iface = h.get("connectedInterfaceName", "N/A")
        print(f"{name:<12} {ip:<16} {mac:<18} {switch:<18} {iface}")

if __name__ == "__main__":
    main()