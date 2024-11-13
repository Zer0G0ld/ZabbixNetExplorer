import nmap  # type: ignore
import socket
import logging as log
from scapy.all import ARP, Ether, srp  # type: ignore

# Configuração de logging
log.basicConfig(level=log.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Função para obter dados da máquina usando nmap
def data_machine_ip(ip):
    try:
        nm = nmap.PortScanner()
        nm.scan(ip, '22')  # escaneia a porta 22 (SSH)
        system = nm[ip]['osmatch'][0]['name'] if 'osmatch' in nm[ip] else "Desconhecido"
        hostname = nm[ip].hostname() if nm[ip].hostname() else "Desconhecido"
        return hostname, system
    except Exception as e:
        log.error(f"Não foi possível obter dados da máquina {ip}: {e}")
        return None, None

# Função para configurar o script
def setup():
    print("""
    Este script é para vasculhar a rede e buscar dados para automatizar a adição de hosts no Zabbix.
    Vamos fazer um scan na sua rede procurando por IPs ativos e verificar se ele tem o Zabbix.
    Vamos procurar também o nome de cada máquina com seu respectivo IP e MAC, buscando o nome e o sistema operacional dela.
    """)
    acordo = input("Concorda com isso? Sim[S] ou Não[N]: ").strip().lower()

    if acordo == 's':
        # Cria os arquivos
        create_files()

        # Escaneia a rede
        devices = scan_network(ip_range)

        # Variáveis para contar dispositivos ativos e inativos
        active_count = 0
        inactive_count = 0
        os_count = {}

        # Verifica cada dispositivo encontrado
        if devices:
            for device in devices:
                ip = device['ip']
                mac = device['mac']  # Obtém o MAC address do dispositivo

                # Obtendo o nome do host e sistema operacional
                hostname, system = data_machine_ip(ip)

                if system:
                    os_count[system] = os_count.get(system, 0) + 1

                if check_zabbix_agent(ip):
                    add_to_files(ip, mac, "on")  # Envia para arquivo de Zabbix On
                    active_count += 1
                else:
                    add_to_files(ip, mac, "off")  # Envia para arquivo de Zabbix Off
                    inactive_count += 1

            # Exibe o resumo final
            print(f"\nResumo do Scan:")
            print(f"Range escaneado: {ip_range}")
            print(f"Dispositivos encontrados: {len(devices)}")
            print(f"Ativos com Zabbix: {active_count}")
            print(f"Inativos sem Zabbix: {inactive_count}")
            print(f"\nQuantidade de hosts por Sistema Operacional:")
            for system, count in os_count.items():
                print(f"{system}: {count} hosts")
        else:
            log.info("Nenhum dispositivo ativo encontrado.")
    elif acordo == 'n':
        print("Operação cancelada.")
    else:
        print("Resposta inválida. Por favor, digite 'S' para Sim ou 'N' para Não.")

# Criando arquivos que dizem os IPs ativos com Zabbix e os IPs inativos
def create_files():
    fileIPON = "IpZabbixOn.txt"
    fileIPOFF = "IpZabbixOff.txt"
    
    # Cria ou limpa os arquivos antes de adicionar os IPs
    with open(fileIPON, "w") as f_on, open(fileIPOFF, "w") as f_off:
        f_on.write("IPs com Zabbix Agent:\n")
        f_off.write("IPs sem Zabbix Agent:\n")

# Função para escanear a rede e encontrar dispositivos ativos
def scan_network(ip_range):
    print(f"Escaneando a rede {ip_range}...")
    # Cria um pacote ARP para o IP range especificado
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp

    # Envia o pacote e recebe a resposta
    log.debug("Enviando pacote ARP...")
    result = srp(packet, timeout=2, verbose=0)[0]
    log.debug("Pacote enviado, processando respostas...")

    # Lista de dispositivos ativos
    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})

    return devices

# Função para verificar se o Zabbix Agent está rodando
def check_zabbix_agent(ip):
    port = 10050  # Porta padrão do Zabbix Agent
    try:
        # Tenta conectar no IP e porta 10050
        with socket.create_connection((ip, port), timeout=2) as sock:
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False

# Função para adicionar os IPs nos arquivos
def add_to_files(ip, mac, status):
    if status == "on":
        with open("IpZabbixOn.txt", "a") as f_on:
            f_on.write(f"{ip}   {mac}   Zabbix Ativo\n")
    else:
        with open("IpZabbixOff.txt", "a") as f_off:
            f_off.write(f"{ip}  {mac}   Zabbix Inativo\n")

# Define o range de IPs da sua rede (ajuste conforme necessário)
ip_range = "192.168.1.0/24"  # Exemplo de rede padrão

# Chama a função de configuração
setup()
