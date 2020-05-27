import subprocess

def wifi_connection_specs():
    cmd = 'netsh wlan show interfaces'
    specs = subprocess.getoutput(cmd).split("\n")
    #print(subprocess.getoutput(cmd))
    wifi_connect_specs_list=[]
    liste = []
    for i in specs:
        if i.find("Name") != -1:
            Wifi_Name=i.split(":",1)[1]
            liste.append(Wifi_Name.lstrip(" "))
        elif i.find("Physical address") != -1:
            WiFi_MAC=i.split(":",1)[1]
            liste.append(WiFi_MAC.lstrip(" "))
        elif i.find("State") != -1:
            WiFi_durum=i.split(":",1)[1]
            liste.append(WiFi_durum.lstrip(" "))
        elif i.find("BSSID") != -1:
            SSID_MAC=i.split(":",1)[1]
            liste.append(SSID_MAC.lstrip(" "))
        elif i.find("Radio type") != -1:
            Connection_Type=i.split(":",1)[1]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            =i.split(":",1)[1]
            liste.append(Connection_Type.lstrip(" "))
        elif i.find("Channel") != -1:
            WiFi_Channel=i.split(":",1)[1]
            liste.append(WiFi_Channel.lstrip(" "))
        elif i.find("Receive rate (Mbps)") != -1:
            Download_Speeds=i.split(":",1)[1]
            liste.append(Download_Speeds.lstrip(" "))
        elif i.find("Transmit rate (Mbps)") != -1:
            Upload_Speeds=i.split(":",1)[1]
            liste.append(Upload_Speeds.lstrip(" "))
        elif i.find("Signal") != -1:
            Signal_Kalitesi=i.split(":",1)[1]
            liste.append(Signal_Kalitesi.strip(" "))
        if len(liste)==9:
            wifi_connect_specs_list.append(liste)
            liste=[]
    return (wifi_connect_specs_list)

if __name__ == "__main__":
    print(wifi_connection_specs())

