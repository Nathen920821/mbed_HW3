# ble_scan_connect.py:
from bluepy.btle import Peripheral, UUID
from bluepy.btle import Scanner, DefaultDelegate
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
    def handleDiscovery(self, dev, isNewDev, isNewData):
       if isNewDev:
          print ("Discovered device", dev.addr)
       elif isNewData:
          print ("Received new data from", dev.addr)
class WriteDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
    def handleNotification(self, cHandle, data):
        print("A notification was received: %s" %data)
scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(10.0)
n=0
addr = []
for dev in devices:
    print ("%d: Device %s (%s), RSSI=%d dB" % (n, dev.addr,
dev.addrType, dev.rssi))
    addr.append(dev.addr)
    n += 1
    for (adtype, desc, value) in dev.getScanData():
      print (" %s = %s" % (desc, value))
number = input('Enter your device number: ')
print ('Device', number)
num = int(number)
print (addr[num])
#
print ("Connecting...")
dev = Peripheral(addr[num], 'random')
dev.setDelegate(WriteDelegate())
print ("Services...")
for svc in dev.services:
    print (str(svc))
#
try:
    testService = dev.getServiceByUUID(UUID(0x8888))
    for ch in testService.getCharacteristics():
        print (str(ch))
    ch = dev.getCharacteristics(uuid=UUID(0x9898))[0]

    descriptors = ch.getDescriptors(forUUID=0x2902)[0]
    print(descriptors)
    # Changing the value of the descriptor
    new_value = b'\x01\x00'  # Provide the new valu

    desc_read = descriptors.read()
    print(desc_read)

    descriptors.write(new_value)
    while True:
        if dev.waitForNotifications(1.0):
            continue
        print ("Waiting...")
    desc_read = descriptors.read()
    print(desc_read)
    #ch.write(bytes("python","utf-8"),withResponse = True)
#
finally:
    dev.disconnect()
