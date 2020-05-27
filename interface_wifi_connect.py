import pywifi
import time
from pywifi import const

wifi = pywifi.PyWiFi()

print(type(wifi.interfaces()))
print(const.IFACE_SCANNING)

print(pywifi.wifi.Interface.scan())

for j in pywifi.wifi.Interface.scan():
    print(j)

print(wifi.interfaces()[0])
for i in wifi.interfaces():
    print(i)



"""
iface = wifi.interfaces()[0]

iface.disconnect()
time.sleep(1)
assert iface.status() in\
    [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]

profile = pywifi.Profile()
profile.ssid = 'EOX'
profile.auth = const.AUTH_ALG_OPEN

profile.akm.append(const.AKM_TYPE_WPA2PSK)
profile.cipher = const.CIPHER_TYPE_CCMP
profile.key = 'EOX1905gs3784'


iface.remove_all_network_profiles()
tmp_profile = iface.add_network_profile(profile)

iface.connect(tmp_profile)
time.sleep(30)
assert iface.status() == const.IFACE_CONNECTED

iface.disconnect()
time.sleep(1)
assert iface.status() in\
    [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]
"""