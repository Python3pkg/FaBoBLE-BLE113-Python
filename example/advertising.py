# coding: utf-8
## @package advertising
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
import RPi.GPIO as GPIO

port = '/dev/ttyAMA0'
rate = 9600

# Button Brick接続ピン
BUTTON_PIN = 4

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN)
# ボタンの押下状況取得用
buttonState = 0
isFirst = False

# BLE設定、初期処理
ble = FaBoBLE_BLE113.BLE113(port, rate)

# デバッグ有効
ble.setDebug()

if ble.setAdvParameters():
    print("Success:setAdvParams()")
    uuid  = [0xcb,0x86,0xbc,0x31,0x05,0xbd,0x40,0xcc,0x90,0x3d,0x1c,0x9b,0xd1,0x3d,0x96,0x6b]
    major = [0x00,0x71]
    minor = [0x00,0x71]

    ble.setBeaconUuid(uuid)
    ble.setBeaconMajor(major)
    ble.setBeaconMinor(minor)

    # Beacon設定
    if ble.sendBeacon():
        print("Success:sendBeacon()")
    else:
        print("Failed:sendBeacon()")
else:
    print("Failed:setAdvParams()")

# アドバタイズ開始
if ble.setMode():
    print("Success:Start Beacon advertising")
else:
    print("Failed:Start Beacon advertising")

while True:
    # ボタンの押下状況を取得
    buttonState = GPIO.input(BUTTON_PIN)
    # ボタン押下判定
    if buttonState:
        # ボタン押下時初回のみ実行
        if isFirst == False:
            isFirst == True
            # アドバタイズ状態判定
            if ble.isAdvertising()==False:
                # アドバタイズ開始
                if ble.setMode():
                    print("Success:Start Beacon advertising")
                else:
                    print("Failed:Start Beacon advertising")
            else:
                # アドバタイズ終了
                if ble.stopAdv():
                    print("Success:Stop Beacon advertising")
                else:
                    print("Failed:Stop Beacon advertising")
    else:
        isFirst = False
