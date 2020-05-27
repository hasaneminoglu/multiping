def modem_bilgisi():
    import upnpclient
    devices = upnpclient.discover()
    #print(devices)
    if len(devices)>0:
        d = devices[0]
        sonuc="upnp"
        marka = d.manufacturer
        model = d.model_name
        model_numarası = d.model_number
        modem_serinumarası = d.serial_number
        return sonuc,marka,model,model_numarası,modem_serinumarası
    else:
        return "not_upnp","marka","model","model_numarası","modem_serinumarası"
#print(modem_bilgisi())