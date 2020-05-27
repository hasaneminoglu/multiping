import wifi_ip_bulma
import mmulti
import time
import ping_wifi_ozellilerini_ogrenme
import threading
import excel_ping
import ping_zip
import ping_mail
import os
import datetime
import upnp_multiping
import platform
import sys
import ping_baglanma

#print(ping_wifi_ozellilerini_ogrenme.wifi_connection_specs())

print("""
        *****************************
        *  multi ping atma programı *
        *                           *
        *                           *
        *           Hasan Eminoğlu  *
        *                   2020v1  *
        *****************************
        """)

def osystem():
    plat = platform.system()
    while True:
        if plat == "Windows":
            print("Multiping Sistemine Hoş Geldiniz!!!")
            break
        else:
            print("Bu işlemler sadece Windows'ta çalışmaktadır...")
            sys.exit()






def modembilgisi():
    bilgiler=upnp_multiping.modem_bilgisi()
    for i in bilgiler:
        if i[0]=="upnp":
            marka=bilgiler[1]
            model=bilgiler[2]+"("+bilgiler[3]+")"
            serinumarası=bilgiler[4]
        else:
            print("Hangi Marka Modemden ping Atılmaktadır. Boş geçerseniz marka olarak belirnecektir.")
            marka = input("Lütfen Multi Ping Atmak Modemin Markasını Giriniz: ")
            if marka == "":
                marka = "marka"

            print("Hangi Modelden ping Atılmaktadır. Boş geçerseniz model olarak belirnecektir.")
            model = input("Lütfen Multi Ping Atmak Modemin modelini Giriniz: ")
            if model == "":
                model = "model"

            print("Modemin Serinuması giriniz. Boş geçerseniz 111111111 olarak belirnecektir.")
            serinumarası = input("Lütfen Multi Ping Atmak Modemin Firmware Bilgisini Giriniz: ")
            if serinumarası == "":
                serinumarası = "111111111"

            return marka, model, serinumarası

    while True:
        print(marka + " " + model + " " + serinumarası+" Serinumaralı Modem")
        Cevap=input("Yukarıdaki Modem Bilgileri Doğru mu? E/H basınız: ").upper()
        if Cevap=="E":
            return marka,model,serinumarası
            break
        elif Cevap=="H":
            print("Hangi Marka Modemden ping Atılmaktadır. Boş geçerseniz marka olarak belirnecektir.")
            marka = input("Lütfen Multi Ping Atmak Modemin Markasını Giriniz: ")
            if marka == "":
                marka = "marka"

            print("Hangi Modelden ping Atılmaktadır. Boş geçerseniz model olarak belirnecektir.")
            model = input("Lütfen Multi Ping Atmak Modemin modelini Giriniz: ")
            if model == "":
                model = "model"

            print("Modemin Serinuması giriniz. Boş geçerseniz 111111111 olarak belirnecektir.")
            serinumarası = input("Lütfen Multi Ping Atmak Modemin Firmware Bilgisini Giriniz: ")
            if serinumarası == "":
                serinumarası = "111111111"

            return marka, model, serinumarası
            break
        else:
            print("Lütfen Bozmaya Çalışmayınız!!!!")

osystem()
bilgiler=modembilgisi()
marka=bilgiler[0]
model=bilgiler[1]
serinumarası=bilgiler[2]

print("Modemin yazılımını giriniz. Boş geçerseniz fw olarak belirnecektir.")
fw=input("Lütfen Multi Ping Atmak Modemin Firmware Bilgisini Giriniz: ")
if fw=="":
    fw="fw"

print("Ping Atılmak istenilen siteyi Boş geçerseniz www.google.com olarak belirlenecektir.")
site_adress=input("Lütfen Multi Ping Atmak istediğiniz Siteyi Giriniz: ")
if site_adress=="":
    site_adress="www.google.com"

print(site_adress + " adresine kaç kez ping atmak istiyorsunuz, Boş geçerseniz default değer 10 olacaktır.")
kac_kez=input("Lütfen Kaç kez Ping Atmak istediğinizi Giriniz: ")
if kac_kez=="":
    kac_kez="10"

print("interface kontrolleri yapılıyor...")

sonuc_list=[]

def protokol_ssidmac():
    wifi_adaptor = ping_wifi_ozellilerini_ogrenme.wifi_connection_specs()
    protokol_ssidmac_listesi=[]
    for i in wifi_adaptor:
        kanal=i[5]
        protokol=i[4]
        ssidmac=i[3]
        protokol_ssidmac_list = []
        protokol_ssidmac_list.append(protokol)
        protokol_ssidmac_list.append(ssidmac.replace(":",""))
        protokol_ssidmac_list.append(kanal)
        if not protokol_ssidmac_list in protokol_ssidmac_listesi:
            protokol_ssidmac_listesi.append(protokol_ssidmac_list)
    return protokol_ssidmac_listesi
#print(protokol_ssidmac())

def zaman():
    #tday = datetime.date.today()
    now = datetime.datetime.today()
    hour = datetime.datetime.strftime(now, '%X')
    s, dk, sn = hour.rsplit(':')
    saat = (s + '-' + dk + '-' + sn)
    return saat



def delete_file():
    os.chdir('C:\GRK\logs\multiping\\')
    if os.path.isfile(site_adress+".txt"):
        os.remove(site_adress+".txt")

def multi():
    ipadress_list = []
    def thread_metot(cmd, ipadress):
        print("{} ipadresi için işlem başladı".format(ipadress))
        mmulti.ping(cmd=cmd)
        time.sleep(1)
        print("{} için işlem bitti".format(ipadress))
        sonuc = ipadress + "finish"
        sonuc_list.append(sonuc)

    def multirun():
        saat=zaman()
        wifi_adaptor = ping_wifi_ozellilerini_ogrenme.wifi_connection_specs()
        #print(wifi_adaptor)
        """
        global multi_run
        if connection_kontrol()[0]=="ok":
            #multi_run="başladı"
        """
        t = 0
        # print(wifi_ip_bulma)
        for i in wifi_ip_bulma.wifi_name():
            # print(i)
            for j in wifi_adaptor:
                if i[1] == j[0].lstrip():
                    ipadress_list.append(i[0])
                    cmd = "ping -host " + site_adress + " -count " + kac_kez + " -bilgi " + marka + "_" + model + "_" + fw + " -ipadress " + \
                          i[0] + " -protokol " + str(j[4]) + " -kanal " + str(j[5]) + " -signal " + str(
                        j[-1]) + " -BSSID " + str(j[3]).replace(":",
                                                                "") + " -serinumarası " + serinumarası + " -saat " + saat
                    thread_m = threading.Thread(target=thread_metot, args=(cmd, i[0]))
                    thread_m.start()
    multirun()


def islem_kontrol():
    while True:
        if len(sonuc_list)==len(ping_wifi_ozellilerini_ogrenme.wifi_connection_specs()):
            print("Ping Atma işlemleri bitti")
            break
    return "Tamamlandı"


def excel_start():
    while True:
        islem="Tamamlandı"
        if islem==islem_kontrol():
            sonuclar=excel_ping.ping_excel(siteadress=site_adress)
            return sonuclar
            break

def zip():
    ping_zip.zip(siteadress=site_adress)

def mail(sonuc=None):
    ping_mail.mail(sonuclar=sonuc,siteadress=site_adress)



if __name__ == "__main__":
    if ping_baglanma.kontrol_sonuc()=="başladı":
        delete_file()
        multi()
        # apipa_kontrol()
        sonuc_list = excel_start()
        zip()
        mail(sonuc=sonuc_list)
    else:
        print("İşlemde Hata oluştu")

