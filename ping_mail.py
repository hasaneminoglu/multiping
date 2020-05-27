def mail(sonuclar=None,siteadress=None):
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email.mime.image import MIMEImage
    from email import encoders
    import platform
    import os

    plat = platform.system()
    os.chdir('C:\GRK\logs\multiping\\')

    test_nerede = open(siteadress+".txt", "r", encoding="utf-8")
    test_dizin = test_nerede.readlines()
    test_nerede.close()
    # print(test_dizin)

    msg = MIMEMultipart()
    protokols_bssids_list=[]

    for i in test_dizin:
        # print(i)
        mail_islemi = i.split("\\")[-1]
        # print(mail_islemi)
        marka = mail_islemi.split("_")[0]
        model=mail_islemi.split("_")[1]
        yazılım=mail_islemi.split("_")[2]
        serinumarası = mail_islemi.split("_")[3]
        bssid=mail_islemi.split("_")[4]
        #kanal=mail_islemi.split("_")[4]
        hangi_setup_pc = mail_islemi.split("_")[6]
        siteadress = mail_islemi.split("_")[7]
        protokol = mail_islemi.split("_")[8]
        kac_kez = mail_islemi.split("_")[9]
        protokol_bssid_list=[]
        protokol_bssid_list.append(protokol)
        protokol_bssid_list.append(bssid)
        if not protokol_bssid_list in protokols_bssids_list:
            protokols_bssids_list.append(protokol_bssid_list)

        part = MIMEBase('application', "octet-stream")
        path = r"" + str(mail_islemi.rstrip("\n"))
        # print(path)

        zip_file = open(path + '.zip', 'rb')
        part.set_payload(zip_file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment', filename=path + '.zip')
        # print(path)
        msg.attach(part)
        zip_file.close()

        os.chdir(path)
        graphs = hangi_setup_pc + "_" + protokol + "_" + kac_kez + ".png"
        img = open(graphs, 'rb').read()
        msgImg = MIMEImage(img, 'png')
        msgImg.add_header('Content-ID', '<image1>')
        msgImg.add_header('Content-Disposition', 'inline', filename=graphs)
        msg.attach(msgImg)
        os.chdir("../")
        # print("-----------------------------------")

    e_mail = 'Sizin mail adresiniz...'
    e_mail_password = 'Mail şifreniz'
    send_to_email = 'kime mail atılacağı'
    subject = 'Ping Sonuclari'

    protokollar=""
    for i in protokols_bssids_list:
        if len(protokols_bssids_list)>1:
            protokollar = protokollar + i[0]+" ( BSSID "+i[1] +")"+ " ve "
        else:
            protokollar = protokollar + i[0]+" ( BSSID "+i[1] +")"
    protokollar = protokollar.rstrip(" ve ")
    content = marka +" " + model + " "+ serinumarası +" serinumaralı modemin "+ yazılım +" yazılım kullanılarak " + hangi_setup_pc + " pc üzerinden " + protokollar + " wifi protokolleri ile " + siteadress + " adresine " + kac_kez + ' kez multiping atılmıştır.' + '\n'

    for i in sonuclar:
        #print(i)
        ping_ipadress=i[0]
        protokol=i[1]
        request_oranı_str=i[2]
        general_oranı_str=i[3]
        kac_kez_general_oranı=str(i[4])
        kanal=str(i[5])

        ek= ping_ipadress+' üzerinden ' +kanal+' kanal ve '+protokol+' protokol kullanılarak atılan Ping işleminin Request timeout olma oranı: % ' + request_oranı_str + ', General faiure olma oranı: % ' + general_oranı_str + ', Toplamda ' + kac_kez_general_oranı + ' Kaç kez General failure olmuştur.' + '\n'
        content=content+ek
    content=content+'İyi Çalışmalar.\n'

    msg['From'] = e_mail
    msg['To'] = send_to_email
    msg['Subject'] = subject
    body = MIMEText(content, 'plain')
    html = """ \
        <p>This is an inline image<br/>
            <img src="cid:image1">
        </p>
    """

    msg.attach(body)

    try:
        server = smtplib.SMTP('smtp.gmail.com', '587')
        server.starttls()
        server.login(e_mail, e_mail_password)
        server.send_message(msg, from_addr=e_mail, to_addrs=[send_to_email])
        # os.chdir("../")
        print('Mail Gönderildi...')
        sonuc_mail = siteadress + '_' + 'mail' + '.txt'
        MailFile = open(sonuc_mail, "w+")
        mail = "ok"
        # MailFile.write(dizin + '\\' + sonuclar + "\n")
        MailFile.write(mail)
        server.quit()
    except:
        # os.chdir("../")
        print('Mail Gönderilemedi...')
        print('Lütfen Ağ Durumunuzu kontrol ediniz!')
        print('Sonuçları klasörde bulabilirsiniz.')
        sonuc_mail = siteadress + '_' + 'mail' + '.txt'
        MailFile = open(sonuc_mail, "w+")
        mail = "nok"
        # MailFile.write(dizin + '\\' + sonuclar + "\n")
        MailFile.write(mail)
