# coding: utf-8
## @package faboBLE113
#  This is a library for the FaBo BLE113 Brick.
#
#  http://fabo.io/301.html
#
#  Released under APACHE LICENSE, VERSION 2.0
#
#  http://www.apache.org/licenses/
#
#  FaBo <info@fabo.io>

import FaBoBLE_BLE113

port = '/dev/ttyAMA0'
rate = 9600

print("Start!")
ble = FaBoBLE_BLE113.BLE113(port, rate)

ble.setDebug()

# Scanパラメータセット
param = [
    0x80,  # interval1 データ検索間隔 0x4 - 0x4000
    0x00,  # interval2  1 -> 625us
    0x28,  # window1   検索時間 0x4 - 0x4000
    0x00,  # window2    1 -> 625us
    0x01   # 1:Active scanning, 0:Passive scanning
]

if ble.setScanParams(param):
    print("param set OK!")
else:
    print("param set NG!")

print("sd_ble_gap_scan_start()")

if ble.scan():
    print("Scan OK!")
else:
    print("Scan NG!")

while True:
    # BLE内部処理のためloop内で呼び出してください
    ble.tick()

    buff =  ble.getScanData()
    if buff["rssi"]!=0:
        print("RSSI:"       ,buff["rssi"], end=' ')
        print("PacketType:" ,'%02x' % buff["packettype"], end=' ')
        print("Sender:", end=' ')
        for i in range(5, -1, -1):
            print('%02x' % buff["sender"][i], end=' ')
        print("AddrType:"   ,'%02x' % buff["addrtype"], end=' ')
        print("Bond:"       ,'%02x' % buff["bond"], end=' ')
        print("Data:", end=' ')
        for i in range(buff["data_len"]):
            print('%02x' % buff["data"][i], end=' ')
        print()
