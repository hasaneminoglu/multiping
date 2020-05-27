import subprocess
import wifi_ip_bulma

def wifi_driver_specs():
    wifi_devices_list=[]
    wifi_adaptor = wifi_ip_bulma.wifi_name()
    for i in wifi_adaptor:
        #print(i)
        Adaptor = i[1]
        cmd = 'Get-NetAdapterAdvancedProperty "' + Adaptor + '" | ft DisplayName, DisplayValue, ValidDisplayValues'
        process = subprocess.Popen(["powershell", cmd], stdout=subprocess.PIPE);
        result = process.communicate()[0]
        driver_specs = result.decode().split("\n")
        Displayname_list = []
        for i in driver_specs:
            # print("iiiiii",i)
            if i.find("Wireless Mode") != -1:
                # print("llllllllllll",i)
                Displayname = i.split("Wireless Mode")
                Displayname_list.append(Displayname[0]+"Wireless Mode")
        #print(Displayname_list)
        if len(Displayname_list)>1:
            for i in Displayname_list:
                if i.find("n/")!=-1 or i.find("/n")!=-1:
                    Name= i.split("Wireless Mode",1)
                    DisplayName=(Name[0]+"Wireless Mode")
                    #print(DisplayName)
        else:
            DisplayName=Displayname_list[0]
        ps_limit_set_cmd="$FormatEnumerationLimit=-1"
        #subprocess.call(["powershell", ps_limit_set_cmd]);
        PC_wifi_modelar_cmd = 'Get-NetAdapterAdvancedProperty "' + Adaptor + '" -DisplayName "' + DisplayName + '"| ft ValidDisplayValues '
        process = subprocess.Popen(["powershell",ps_limit_set_cmd,"\n",PC_wifi_modelar_cmd], stdout=subprocess.PIPE);
        result = process.communicate()[0]
        PC_wifi_modelar_sonuc = result.decode()
        #print(PC_wifi_modelar_sonuc)
        #print(PC_wifi_modelar_sonuc.split("\n"))
        sonuc=PC_wifi_modelar_sonuc.split("\n")[3]
        #print(sonuc)
        sonuc=sonuc.strip("{")
        sonuc = sonuc.strip("}\r")
        mode_sonuclar=sonuc.split(", ")
        mode_sonuclar.append(Adaptor)
        mode_sonuclar.append(DisplayName)
        wifi_devices_list.append(mode_sonuclar)
    return wifi_devices_list

def wifi_frekans_working_bulma():
    bghz=0
    bghz_list=[]
    ighz=0
    ighz_list=[]
    sonuclar=wifi_driver_specs()
    for i in sonuclar:
        m = "ac"
        for m in i:
            #print(i[-2] + " Adlı WiFi Adaptor (2.4 ve 5) GHz Desteklemektedir.")
            #print("Maksimum Wireless Modu : " + i[-3])
            bghz+=1
            bghz_list.append(i)
            break
        else:
            #print(i[-2] + " Adlı WiFi Adaptor Sadece 2.4 GHz Desteklemektedir.")
            #print("Maksimum Wireless Modu : " + i[-3])
            ighz+=1
            ighz_list.append(i)
    return ighz,bghz,ighz_list,bghz_list

def SSID_Password():
    ghz_istek = bilgi_verme()
    if ghz_istek[0] == "1":
        iSSID = input("Lütfen SSID'yi Giriniz : ")
        iPassword = input("Lütfen şifreyi'yi Giriniz : ")
        bSSID = ""
        bPassword = ""
    elif ghz_istek[0]  == "2":
        iSSID = ""
        iPassword = ""
        bSSID = input("Lütfen SSID'yi Giriniz : ")
        bPassword = input("Lütfen şifreyi'yi Giriniz : ")
    elif ghz_istek[0]  == "3":
        iSSID = input("Lütfen 2.4 GHz için SSID'yi Giriniz : ")
        iPassword = input("Lütfen 2.4 GHz için şifreyi'yi Giriniz : ")
        bSSID = input("Lütfen 5 GHz için SSID'yi Giriniz : ")
        bPassword = input("Lütfen 5 GHz için şifreyi'yi Giriniz : ")

    return ghz_istek[0],ghz_istek[1],iSSID, iPassword, bSSID, bPassword



def bilgi_verme():
    ghzs = wifi_frekans_working_bulma()
    while True:
        ghz_istek = input("""Hangi frekansa göre işlem yapmak istiyorsunuz
    1 - 2.4 GHz
    2 - 5 GHz
    3 - 2.4 ve 5 GHz
	Seçeneğiniz : 
    """)
        if ghz_istek == "1":
            print(str(int(ghzs[0])+int(ghzs[1]))+" adet 2.4 GHz frekansı destekleyen wifi adaptor bulunmaktadır.")
            ghzs=iki_frekansi_yapma()
            return ghz_istek , ghzs
            break
        elif ghz_istek == "2":
            print(str(ghzs[1]) + " adet 5 GHz frekansı destekleyen wifi adaptor bulunmaktadır.")
            return ghz_istek , ghzs
            break
        elif ghz_istek == "3":
            print(str(int(ghzs[0])) + " adet sadece 2.4 GHz frekansı destekleyen wifi adaptor bulunmaktadır.")
            print(str(ghzs[1]) + " adet 2.4 ve 5 GHz frekansı destekleyen wifi adaptor bulunmaktadır.")
            if int(ghzs[0])!=int(ghzs[1]):
                print("Sistem Otomatik olarak 2.4 ve 5 GHz frekanslarına wifi adaptörleri bölecektir.")
                ghzs=ortalama_yapma()
            return ghz_istek , ghzs
            break
        else:
            print("Lütfen Bozmaya Çalışmayınız.....")

def ortalama_yapma():
    wifiler_bilgi=wifi_frekans_working_bulma()
    i_sayi=int(wifiler_bilgi[0])
    b_sayi=int(wifiler_bilgi[1])
    i_list=wifiler_bilgi[2]
    b_list=wifiler_bilgi[3]
    o_sayi=int((i_sayi+b_sayi)/2)
    ie_aktarma_sayi=o_sayi-i_sayi
    #print(ie_aktarma_sayi,o_sayi,i_sayi)
    b_kalan_sayi=b_sayi-o_sayi
    while ie_aktarma_sayi > 0:
        cikan=b_list[-1]
        i_list.append(cikan)
        b_list.remove(cikan)
        ie_aktarma_sayi-=1
    return (o_sayi-i_sayi,b_kalan_sayi,i_list,b_list)

def iki_frekansi_yapma():
    wifiler_bilgi = wifi_frekans_working_bulma()
    i_sayi = int(wifiler_bilgi[0])
    b_sayi = int(wifiler_bilgi[1])
    i_list = wifiler_bilgi[2]
    b_list = wifiler_bilgi[3]
    ie_aktarma_sayi = b_sayi - i_sayi
    # print(ie_aktarma_sayi,o_sayi,i_sayi)
    while ie_aktarma_sayi > 0:
        cikan = b_list[-1]
        i_list.append(cikan)
        b_list.remove(cikan)
        ie_aktarma_sayi -= 1
    b_kalan_sayi = len(b_list)
    i_sayi = len(i_list)
    #print(i_list)
    return (i_sayi, b_kalan_sayi, i_list, b_list)

"""
if __name__ == "__main__":
    #print(wifi_driver_specs())
    #wifi_frekans_working_bulma()
    #bilgi_verme()
    print(SSID_Password())
    #print(iki_frekansi_yapma())
"""


