import subprocess
import os
import wifi_device_ozellikleri
import ping_apipa
import sys
import ping_wifi_ozellilerini_ogrenme
import time

def file(ssid=None,password=None,frekans=None):
    #ssid = 'EOX'
    #password = 'EOX1905gs3784'
    #frekans = "2.4GHz"
    file_in = """<?xml version="1.0"?>
    <WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
        <name>""" + ssid + """</name>
        <SSIDConfig>
            <SSID>
                <name>""" + ssid + """</name>
            </SSID>
        </SSIDConfig>
        <connectionType>ESS</connectionType>
        <connectionMode>auto</connectionMode>
        <MSM>
            <security>
                <authEncryption>
                    <authentication>WPA2PSK</authentication>
                    <encryption>AES</encryption>
                    <useOneX>false</useOneX>
                </authEncryption>
                <sharedKey>
                    <keyType>passPhrase</keyType>
                    <protected>false</protected>
                    <keyMaterial>""" + password + """</keyMaterial>
                </sharedKey>
            </security>
        </MSM>
        <MacRandomization xmlns="http://www.microsoft.com/networking/WLAN/profile/v3">
            <enableRandomization>false</enableRandomization>
        </MacRandomization>
    </WLANProfile>"""

    os.chdir('C:\GRK\logs\multiping\\')
    file = ssid + "_" + frekans + '.xml'
    if not os.path.isfile(ssid):
        SSIDFile = open(file, "w+", buffering=1)
        SSIDFile.write(file_in + "\n")
    SSIDFile.close()
    return file

def wifi_profil_sil():
    print("Bütün WiFi Profilleri Siliniyor...")
    delete_profile_cmd='netsh wlan delete profile name=* i=*'
    subprocess.call(delete_profile_cmd)

def connection(ssid=None,adaptor=None,file=None):
    #ssid = 'EOX'
    # password = 'EOX1905gs3784'
    #frekans = "2.4GHz"
    os.chdir('C:\GRK\logs\multiping\\')
    #file = ssid + "_" + frekans + '.xml'
    #adaptor = "Wi-Fi 5"

    # delete_profile_cmd='netsh wlan delete profile name=* i=*'
    # subprocess.call(delete_profile_cmd)

    PC_wifi_add_profile_cmd = 'netsh wlan add profile filename="' + file + '" interface="' + adaptor + '"'
    PC_wifi_modelar_cmd = 'netsh wlan connect ssid='+ssid+' name='+ssid+' interface="' + adaptor + '"'

    subprocess.call(PC_wifi_add_profile_cmd)
    subprocess.call(PC_wifi_modelar_cmd)

def auto():
    wifi_profil_sil()
    ozellikler=wifi_device_ozellikleri.SSID_Password()
    adaptor_list = []
    adaptor_ilist = []
    adaptor_blist = []
    #print(ozellikler)
    if ozellikler[0]=="1":
        ozellik = ozellikler[1][2]
        for ghzs in ozellik:
                adaptor_name=ghzs[-2]
                adaptor_ilist.append(adaptor_name)
        adaptor_list.append(adaptor_ilist)
        adaptor_list.append(adaptor_blist)
    elif ozellikler[0]=="2":
        ozellik = ozellikler[1][3]
        for ghzs in ozellik:
            adaptor_name = ghzs[-2]
            adaptor_blist.append(adaptor_name)
        adaptor_list.append(adaptor_ilist)
        adaptor_list.append(adaptor_blist)
    elif ozellikler[0]=="3":
        ozellik = ozellikler[1][2]
        for ghzs in ozellik:
            adaptor_name = ghzs[-2]
            adaptor_ilist.append(adaptor_name)
        ozellik = ozellikler[1][3]
        for ghzs in ozellik:
            adaptor_name = ghzs[-2]
            adaptor_blist.append(adaptor_name)
        adaptor_list.append(adaptor_ilist)
        adaptor_list.append(adaptor_blist)
    #print(ozellikler[0],adaptor_list,ozellikler[-4],ozellikler[-3],ozellikler[-2],ozellikler[-1])
    return ozellikler[0],adaptor_list,ozellikler[-4],ozellikler[-3],ozellikler[-2],ozellikler[-1]

def connect():
    oto=auto()
    #print(oto)
    if oto[0]=="1":
        dosya=file(ssid=oto[2],password=oto[3],frekans="2.4GHz")
        adaptorler=oto[1][0]
        for adaptor in adaptorler:
            connection(ssid=oto[2],adaptor=adaptor,file=dosya)
    elif oto[0]=="2":
        dosya=file(ssid=oto[4],password=oto[5],frekans="5GHz")
        adaptorler=oto[1][1]
        for adaptor in adaptorler:
            connection(ssid=oto[4],adaptor=adaptor,file=dosya)
    elif oto[0]=="3":
        dosya2 = file(ssid=oto[2],password=oto[3],frekans="2.4GHz")
        dosya5 = file(ssid=oto[4],password=oto[5],frekans="5GHz")
        iadaptorler=oto[1][0]
        badaptorler = oto[1][1]
        for iadaptor in iadaptorler:
            connection(ssid=oto[2],adaptor=iadaptor,file=dosya2)
        for badaptor in badaptorler:
            connection(ssid=oto[4],adaptor=badaptor,file=dosya5)

def apipa_kontrol():
    connect()
    apipa=ping_apipa.apipa_statik_sonuc()
    apipalar_list = []
    statiklar_list = []
    dns_statikler=[]
    for i in apipa:
        if i[2]=="apipa":
            apipa_list=[]
            apipa_list.append(i[0])
            apipa_list.append(i[4])
            apipa_list.append(i[3])
            apipalar_list.append(apipa_list)
        if i[-2]=="No":
            statik_list = []
            statik_list.append(i[0])
            statik_list.append(i[4])
            statik_list.append(i[3])
            statiklar_list.append(statik_list)
        if i[-1]=="statik":
            dnsstatik_list = []
            dnsstatik_list.append(i[0])
            dnsstatik_list.append(i[4])
            dnsstatik_list.append(i[3])
            dns_statikler.append(dnsstatik_list)
    if len(apipalar_list)>0:
        for i in apipalar_list:
            print(i[0] + " adlı ve " + i[1] + " MAC adresli interface üzerinde " + i[2] + " apipa ip'si bulunmaktadır.")
            print("Lütfen durumu kontrol edip tekrar proğramı tekrar başlatınız...")
            sys.exit()
    if len(statiklar_list)>0:
        for i in statiklar_list:
            print(i[0] + " adlı ve " + i[1] + " MAC adresli interface üzerinde " + i[2] + " statik dns'si bulunmaktadır.")
        while True:
            statik_cevap=input("Statik interfacelerin durumu dinamik ip'ye çevirsin mi? E/H : ").upper()
            if statik_cevap=="H":
                print("Lütfen durumu kontrol edip tekrar proğramı tekrar başlatınız...")
                sys.exit()
            elif statik_cevap=="E":
                for i in statiklar_list:
                    ping_apipa.dinamik_ip(i=i[0])
                break
            else:
                print("Lütfen Bozmaya Çalışmayınız...")
        time.sleep(3)
    if len(dns_statikler)>0:
        for i in dns_statikler:
            print(i[0] + " adlı ve " + i[1] + " MAC adresli interface üzerinde statik dns'si bulunmaktadır.")
        while True:
            dns_cevap=input("Statik interfacelerin durumu dinamik dns'ye çevirsin mi? E/H : ").upper()
            if dns_cevap=="H":
                print("Lütfen durumu kontrol edip tekrar proğramı tekrar başlatınız...")
                sys.exit()
            elif dns_cevap=="E":
                for i in dns_statikler:
                    ping_apipa.dinamik_dns(i=i[0])
                break
            else:
                print("Lütfen Bozmaya Çalışmayınız...")
        time.sleep(3)

def connection_kontrol():
    apipa_kontrol()
    check="ok"
    not_connection_list=[]
    wifi_adaptor=ping_wifi_ozellilerini_ogrenme.wifi_connection_specs()
    #print(wifi_adaptor)
    for i in wifi_adaptor:
        if i[2]!="connected":
            not_check_wifi_apaptor_str=""
            for j in i:
                not_check_wifi_apaptor_str=not_check_wifi_apaptor_str+"_"+j
            not_check_wifi_apaptor=not_check_wifi_apaptor_str.split("disconnected")
            #print(not_check_wifi_apaptor)
            check="nok"
            for m in not_check_wifi_apaptor:
                nok=m.split("_")
                if len(nok)>1:
                    nok_check_list=[]
                    nok_check_list.append(nok[1])
                    nok_check_list.append(nok[2])
                    not_connection_list.append(nok_check_list)
    return check , not_connection_list

def kontrol_sonuc():
    if connection_kontrol()[0] == "ok":
        multi_run="başladı"
    else:
        multi_run = "başlamadı"
        # print(connection_kontrol())
        j = connection_kontrol()[1]
        # print(j)
        for k in j:
            print(k[0] + " Adlı ve " + k[1] + " MAC adresli kablosuz wifi adaptör Modeme Bağlı değildir.")
        sys.exit()
    return multi_run