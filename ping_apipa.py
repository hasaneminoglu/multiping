import subprocess
import ping_wifi_ozellilerini_ogrenme
import win32com.shell.shell as shell

def interface_bul():
    interfaces = {}
    cmd = 'netsh interface show interface'
    Interfaces = subprocess.getoutput(cmd)
    GwInterface = Interfaces.split("\n")
    id = 1
    for Interface in GwInterface:
        id += 1
        if Interface.find("Dedicated") != -1:
            interfaceler = Interface.split("Dedicated")
            iface = interfaceler[1]
            gw_iface = (iface.split("\n")[0]).strip()
            interfaces[id] = gw_iface
    return interfaces

def interface_wifibul():
    wifiler = {}
    for i in interface_bul():
        if interface_bul().get(i).find("Wi-Fi") != -1 or interface_bul().get(i).find("Kablosuz") != -1:
            wifiler[i]=interface_bul().get(i)
    return wifiler

"""
def index_kontrol():
    #index_sirala()
    interface_bul()
    durum=True
    while durum:
        giris_index=input("lütfen index bilgisini giriniz: ").upper()
        indexler=interface_bul()
        if giris_index.isdigit():
            for i in indexler:
                if i == int(giris_index):
                    durum = False
                    id = int(giris_index)
                    break
        else:
            try:
                if giris_index=="Q":
                    durum = False
                    id = giris_index
                    break
            except:
                pass
    return id
        
"""

def apipa_ip():
    i=interface_wifibul()
    for j in i:
        gw_iface = interface_bul().get(j)
        cmd = 'netsh interface ipv4 show config name="' + gw_iface + '"'
        config = subprocess.getoutput(cmd).split("\n")
        for statik in config:
            if statik.find("IP Address:") != -1:
                ip_adress = (statik.split(":")[1].strip())
                ip_var = True
                break
            else:
                ip_var=False
                ip_adress=""
        if ip_var==True:
            if ip_adress.split(".")[0]=="192":
                dnmk_ip="ip"
                #print("İnterface'nin dinamik "+ip_adress+" ip'si bulunmaktadır.")
                yield gw_iface,ip_var,dnmk_ip,ip_adress
            elif ip_adress.split(".")[0] == "169":
                dnmk_ip = "apipa"
                #print("İnterface'nin apipa " + ip_adress + " ip'si bulunmaktadır.")
                yield gw_iface,ip_var,dnmk_ip,ip_adress
        else:
            dnmk_ip="yok"
            #print("İnterface'nin herhangi bir ip'si bulunmamaktadır.")
            yield gw_iface,ip_var,dnmk_ip,ip_adress

#print(ping_wifi_ozellilerini_ogrenme.wifi_connection_specs())



def interface_config(i=None):
    if i is None:
        j = interface_wifibul()
        for i in j:
            gw_iface = interface_bul().get(i)
            cmd = 'netsh interface ipv4 show config name="' + gw_iface + '"'
            config = subprocess.getoutput(cmd).split("\n")
            dnsler = []
            ip_adress = None
            Netmask = None
            Default_Gateway = None
            for line in config:
                if line.find("DHCP enabled:") != -1:
                    DHCP = (line.split(":")[1].strip())
                if line.find("IP Address:") != -1:
                    ip_adress = (line.split(":")[1].strip())
                if line.find("Subnet Prefix:") != -1:
                    Netmask = (line.split("mask")[1].strip()).strip(")")
                if line.find("Default Gateway:") != -1:
                    Default_Gateway = (line.split(":")[1].strip())
                if line.find("Statically Configured DNS Servers:") != -1:
                    dns_durum = "statik"
                    DNS1 = (line.split(":")[1].strip())
                    dnsler.append(DNS1)
                if line.find("DNS servers configured through DHCP:") != -1:
                    dns_durum = "dinamik"
                    Dinamic_DNS = (line.split(":")[1].strip())
                    dnsler.append(Dinamic_DNS)
                if line is not None and line.split(".")[0].strip().isdigit():
                    dnsler.append(line.strip())
            yield gw_iface,DHCP, ip_adress, Netmask, Default_Gateway, dns_durum, dnsler

def apipa_sonuc():
    wifi_full_spec_list = []
    for i in apipa_ip():
        wifi_list = []
        for j in ping_wifi_ozellilerini_ogrenme.wifi_connection_specs():
            if i[0] == j[0]:
                for k in i:
                    wifi_list.append(k)
                wifi_list.append(j[1])
                wifi_full_spec_list.append(wifi_list)
    return wifi_full_spec_list

def apipa_statik_sonuc():
    wifi_full_spec_list = []
    for i in apipa_ip():
        wifi_list = []
        for j in ping_wifi_ozellilerini_ogrenme.wifi_connection_specs():
            if i[0] == j[0]:
                for k in i:
                    wifi_list.append(k)
                wifi_list.append(j[1])
                #wifi_full_spec_list.append(wifi_list)
        for k in interface_config():
            if i[0] == k[0]:
                wifi_list.append(k[1])
                wifi_list.append(k[5])
                wifi_full_spec_list.append(wifi_list)
    return wifi_full_spec_list

def dinamik_ip(i=None):
    gw_iface = i
    dinamik_cmd='netsh interface ip set address "'+gw_iface+'" dhcp'
    shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c '+dinamik_cmd)

def dinamik_dns(i=None):
    gw_iface = i
    dinamik_cmd='netsh interface ip set dns "'+gw_iface+'" dhcp'
    shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c '+dinamik_cmd)

"""
print(apipa_sonuc())
for i in interface_config():
    print(i)
    print("--------------------")
"""
#print(apipa_statik_sonuc())
