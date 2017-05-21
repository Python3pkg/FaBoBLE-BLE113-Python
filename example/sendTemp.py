# coding: utf-8
## @package sendTemp
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
import spidev
import sys

TEMPPIN = 0

# advertising

port = '/dev/ttyAMA0'
rate = 9600

ble = FaBoBLE_BLE113.BLE113(port, rate)

ble.setDebug()

if ble.setAdvParameters():
    print("Success:setAdvParams()")
    uuid  = [0x00,0x11,0x11,0x33,0x44,0x55,0x66,0x77,0x88,0x99,0xaa,0xbb,0xcc,0xdd,0xee,0xff]
    major = [0x01,0x02]
    minor = [0x00,0x00]

    ble.setBeaconUuid(uuid)
    ble.setBeaconMajor(major)
    ble.setBeaconMinor(minor)

    if ble.sendBeacon():
        print("Success:sendBeacon()")
    else:
        print("Failed:sendBeacon()")
else:
    print("Failed:setAdvParams()")

if ble.setMode():
    print("Success:Start Beacon Advertising")
else:
    print("Failde:Start Beacon Advertising")

# Set SPI
spi = spidev.SpiDev()
spi.open(0,0)

def readadc(channel):
    adc = spi.xfer2([1,(8+channel)<<4,0])
    data = ((adc[1]&3) << 8) + adc[2]
    return data

def arduino_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min


while True:
    try:
        while True:
            data = readadc(TEMPPIN)
            volt = arduino_map(data, 0, 1023, 0, 5000)
            temp = arduino_map(volt, 300, 1600, -30, 100)
            print(("temp : {:4.1f} ".format(temp)))
            time.sleep( 0.5 )
            send_temp = int(temp)
            ble.setBeaconMinor([0,send_temp])
            if ble.sendBeacon()==False:
                print("Failed :sendBeacon()")
            time.sleep( 5 )

    except KeyboardInterrupt:
       spi.close()
       sys.exit(0)
