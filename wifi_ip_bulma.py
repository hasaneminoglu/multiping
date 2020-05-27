import subprocess, time
import platform

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

def apipa_ip():
    i=index_kontrol()
    gw_iface = interface_bul().get(i)
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
            print("İnterface'nin dinamik "+ip_adress+" ip'si bulunmaktadır.")
            return ip_var,dnmk_ip,ip_adress
        elif ip_adress.split(".")[0] == "169":
            dnmk_ip = "apipa"
            print("İnterface'nin apipa " + ip_adress + " ip'si bulunmaktadır.")
            return ip_var,dnmk_ip,ip_adress
    else:
        dnmk_ip="yok"
        print("İnterface'nin herhangi bir ip'si bulunmamaktadır.")
        return ip_var,dnmk_ip,ip_adress

def osystem():
    plat = platform.system()
    while True:
        if plat == "Windows":
            print("Sisteme Hoş Geldiniz!!!")
            break
        else:
            print("Bu işlemler sadece Windows'ta çalışmaktadır...")

def index_sirala():
    osystem()
    indexler = interface_bul()
    print("index\tinterface")
    for i in indexler:
        print(str(i) + "\t\t" + str(indexler.get(i)))

def index_kontrol():
    index_sirala()
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

def dinamik_ip(i=None):
    if i is None:
        i = index_kontrol()
    gw_iface = interface_bul().get(i)
    dinamik_cmd='netsh interface ip set address "'+gw_iface+'" dhcp'
    subprocess.call(dinamik_cmd)

def dinamik_dns(i=None):
    if i is None:
        i=index_kontrol()
    gw_iface = interface_bul().get(i)
    dinamik_cmd='netsh interface ip set dns "'+gw_iface+'" dhcp'
    subprocess.call(dinamik_cmd)


def interface_wifibul():
    wifiler = {}
    for i in interface_bul():
        if interface_bul().get(i).find("Wi-Fi") != -1 or interface_bul().get(i).find("Kablosuz") != -1:
            wifiler[i]=interface_bul().get(i)
    return wifiler

def wifi_index_sirala():
    osystem()
    print("index\tinterface")
    for j in interface_wifibul():
        print(str(j) + "\t\t" + str(interface_wifibul().get(j)))

def wifi_name():
    if len(interface_wifibul()) == 0:
        print("Wifi Modül bulunmamaktadır.")
        breakpoint()
    elif len(interface_wifibul()) > 0:
        for i in interface_wifibul():
            #print(i)
            #print(interface_bul().get(i))
            yield interface_config(i=i)[1] , interface_bul().get(i)
    else:
        id=None
        return id


def interface_config(i=None):
    if i is None:
        i = index_kontrol()
    gw_iface = interface_bul().get(i)
    cmd = 'netsh interface ipv4 show config name="' + gw_iface + '"'
    config = subprocess.getoutput(cmd).split("\n")
    dnsler=[]
    ip_adress=None
    Netmask=None
    Default_Gateway=None
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
    """
    if DHCP=="Yes":
        if ip_adress is not None or Netmask is not None or Default_Gateway is not None:
            print("Dinamik olarak "+ ip_adress +" ip'si " +Netmask+" Mask'ı " + Default_Gateway+" gateway ip'si almıştır.")
        if ip_adress is None or Netmask is None or Default_Gateway is None:
            print("Dinamik olarak hiçbir ip'si bulunmamaktadır.")
    elif DHCP=="No":
        if ip_adress is not None or Netmask is not None or Default_Gateway is not None:
            print("Statik olarak "+ ip_adress +" ip'si " +Netmask+" Mask'ı " + Default_Gateway+" gateway ip'si almıştır.")
    """
    """
    if dns_durum=="dinamik":
        print("DNS sunucusundan alınmış ",end="")
        for i in dnsler:
            if i is None:
                print("hiçbir")
            else:
                print(i,end=" ")
        print("dns bilgisi bulunmaktadır.")
    elif dns_durum=="statik":
        print("Statik olarak verilmiş ",end="")
        for i in dnsler:
            print(i,end=" ")
        print("dnsleri bulunmaktadır.")
    """
    return DHCP,ip_adress,Netmask,Default_Gateway,dns_durum,dnsler

def statik_dns_mi(i=None):
    if i is None:
        i = index_kontrol()
    gw_iface = interface_bul().get(i)
    cmd = 'netsh interface ipv4 show config name="' + gw_iface + '"'
    config = subprocess.getoutput(cmd).split("\n")
    dnsler = []
    for line in config:
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
    if dns_durum=="dinamik":
        print("DNS sunucusundan alınmış ",end="")
        for i in dnsler:
            if i is None:
                print("hiçbir")
            else:
                print(i,end=" ")
        print("dns bilgisi bulunmaktadır.")
    elif dns_durum=="statik":
        print("Statik olarak verilmiş ",end="")
        for i in dnsler:
            print(i,end=" ")
        print("dnsleri bulunmaktadır.")
    return dns_durum, dnsler


if __name__ == "__main__":
    wifi_index_sirala()
    for i in wifi_name():
        print(i)
