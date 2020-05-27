def ping(cmd=None):
    import subprocess
    import platform
    import datetime
    from tqdm import tqdm
    import os
    import time
    import socket
    time.sleep(5)

    #"ping -host www.google.com -count 10 -bilgi marka_fw -ipadress "+i[0]+" -protokol"+str(j[4])+" -kanal"+str(j[5])+" -signal "+str(j[-1])

    cmd_list=cmd.split(" ")
    #print(cmd_list)

    siteadress = cmd_list[2]
    ipadress = cmd_list[8]
    kac_kez = cmd_list[4]
    bilgi_modem = cmd_list[6]
    wifi_protokol = cmd_list[10]
    wifi_kanal = cmd_list[12]
    wifi_signal = cmd_list[14]
    bssid=cmd_list[-5]
    serinumarası = cmd_list[-3]
    saat=cmd_list[-1]

    tday = datetime.date.today()
    now = datetime.datetime.today()
    hour = datetime.datetime.strftime(now, '%X')
    #s, dk, sn = hour.rsplit(':')
    #saat = (s + '-' + dk + '-' + sn)
    plat = platform.system()
    hangi_setup_pc = socket.gethostname()

    #print(bilgi_modem)

    dizin = ('C:\\GRK\\logs\\multiping\\' + bilgi_modem +'_' + serinumarası + '_' + bssid + '_' + wifi_kanal + '_'+ hangi_setup_pc + '_' + siteadress + '_' + wifi_protokol + '_' + kac_kez + '_' + str(tday) + '_' + str(saat))

    os.chdir('C:\GRK\logs\multiping\\')
    sonuc_dizin = siteadress  + '.txt'
    if not os.path.isfile(sonuc_dizin):
        MailFile = open(sonuc_dizin, "w+", buffering=1)
    else:
        MailFile = open(sonuc_dizin, "a+", buffering=1)
    if not os.path.exists(dizin):
        MailFile.write(dizin+"\n")
    MailFile.close()

    # print(siteadress, ipadress, kac_kez, bilgi_modem)

    # dizin = ('C:\GRK\logs\multiping\\' + bilgi_modem + '_' + hangi_setup_pc + '_' + siteadress + '_'+ wifi_protokol + '_' + kac_kez + '_' + str(tday))

    sonuclar = bilgi_modem + '_' + serinumarası + '_' + bssid + '_' + wifi_kanal + '_' + hangi_setup_pc + '_' + siteadress + '_' + ipadress + '_' + kac_kez + '_' + 'sonuc' + '.txt'

    if not os.path.exists(dizin):
        os.makedirs(dizin)
    path = str(dizin)
    os.chdir(path)
    multi_test = 'multi_test_islem' + '.txt'
    test = open(multi_test, "a+", buffering=1, encoding="utf-8")
    test.write(ipadress + " : üzerinden ping işlemi başladı" + " : " + sonuclar + "\n")
    #test.close()
    # sonuclar = bilgi_modem + '_' + hangi_setup_pc + '_' + siteadress + '_' + ipadress + '_' + kac_kez + '_' + 'sonuc' + '.txt'

    """
    os.chdir("../")
    sonuc_dizin = siteadress + '_' + 'mail' + '.txt'
    if not os.path.isfile(sonuc_dizin):
        MailFile = open(sonuc_dizin, "w+",buffering=1)
    else:
        MailFile = open(sonuc_dizin, "a+",buffering=1)
    print(MailFile.readlines())
    if not os.path.exists(dizin):
        MailFile.write(dizin)
    print(MailFile.readlines())
    MailFile.close()

    os.chdir(path)
    """
    PingFile = open(sonuclar, "w+", buffering=1)
    print(ipadress + " ipadresi üzerinden " + siteadress + " adresine " + kac_kez + " kez ping atılmaktadır.")
    if plat == "Windows":
        time.sleep(5)
        value = range(0, int(kac_kez))
        ping = subprocess.Popen(['ping', '' + siteadress, '-n', '' + kac_kez, '-S', '' + ipadress], shell=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = []
        with tqdm(total=len(value)) as pbar:
            for i in value:
                pbar.set_description(ipadress + ' : ipadresi için işlemin Tamamlanma yüzdesi : ')
            while ping.stdout is not None:
                line = ping.stdout.readline()
                result.append(line.decode('UTF-8').strip('\r\n'))
                lines = line.decode('UTF-8').strip("\n")
                pbar.update()
                for line in lines:
                    PingFile.write(line)
                if not line:
                    ping.stdout.flush()
                    break
    """
    elif plat == "Linux":
        time.sleep(10)
        value = range(0, int(kac_kez))
        ping = subprocess.Popen(['ping', '' + siteadress, '-c', '' + kac_kez],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        result = []
        with tqdm(total=len(value)) as pbar:
            for i in value:
                pbar.set_description('Tamamlanan')
            while ping.stdout is not None:
                line = ping.stdout.readline()
                result.append(line.decode('UTF-8').strip('\n') + '\t')
                lines = line.decode('UTF-8').split('\t')
                pbar.update()
                for line in lines:
                    PingFile.write(line)
                if not line:
                    ping.stdout.flush()
                    break
    elif plat == "Darwin":
        time.sleep(10)
        value = range(0, int(kac_kez))
        ping = subprocess.Popen(['ping', '' + siteadress, '-c', '' + kac_kez],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        result = []
        with tqdm(total=len(value)) as pbar:
            for i in value:
                pbar.set_description('Tamamlanan')
            while ping.stdout is not None:
                line = ping.stdout.readline()
                result.append(line.decode('UTF-8').strip('\n')+'\t')
                lines = line.decode('UTF-8').split('\t')
                pbar.update()
                for line in lines:
                    PingFile.write(line)
                if not line:
                    ping.stdout.flush()
                    break
    else:
        print("Bilinmeyen OS")
        breakpoint()
    """
    PingFile.close()

    #test = open("multi_test_islem.txt", "a", encoding="utf-8")
    test.write(ipadress + " : üzerinden ping işlemi bitti" + "\n")
    test.close()