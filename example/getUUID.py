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
import time

if __name__ == '__main__':

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

        # レコードが存在する場合出力
        buff = ble.getScanData()
        if buff["rssi"]!=0 and buff["packettype"] == 2:
            print("RSSI:",buff["rssi"], end=' ')
            print(" UUID:", end=' ')
            for i in range(10,26):
                print('%02x' % buff["data"][i], end=' ')
            print(" MAJOR:",buff["data"][26]<<8 | buff["data"][27], end=' ')
#            for i in range(26,28):
#                print '%02x' % buff["data"][i],
            print(" MINOR:", end=' ')
            print(" MAJOR:",buff["data"][28]<<8 | buff["data"][29], end=' ')
#            for i in range(26,28):
#            for i in range(28,30):
#                print '%02x' % buff["data"][i],
            print()
#        time.sleep(0.1);
