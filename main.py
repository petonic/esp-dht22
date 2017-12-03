#
# Main file for DHT remote temperature MQTT sensors
#
# Config constants are defined in CONFIG.PY for
# Wireless config as well as MQTT Pub info.
#
# Written by Mike Petonic 2017-09-24
#

from config import *             # Project specific configuration
import network
import machine
import time
import dht
import simple
from simple import MQTTClient



wl_net = None              # Holds the WLAN object, None if not connnected

def init_wifi():
    wl_net = network.WLAN(network.STA_IF); wl_net.active(True)
    # Repeat this until our network in WL_SSID is found as the
    # first element of a tuple that is returned.

    my_wifi_found = False
    my_bin_wifi = WL_SSID.encode('utf-8')

    while not my_wifi_found:
        networks = wl_net.scan()             # Scan for available access points
        for i in networks:
            if i[0] == my_bin_wifi:
                my_wifi_found = True
                break
        if my_wifi_found:
            print('! Found wifi network {}, connecting...'.format(WL_SSID),
                  end='')
            break
        print('... {} not found in wireless list: {}'.format(
                WL_SSID, repr(networks)))

        time.sleep(DELAY_SEEK)

    wl_net.connect(WL_SSID, WL_PASSWD) # Connect to an AP

    while not wl_net.isconnected():
        print('Sleeping for 0.5 seconds')
        time.sleep(0.5)

    print('Connected!')
    ifc = wl_net.ifconfig()
    print('Interface info: {}'.format(repr(ifc)))
    return wl_net


def main():
    global wl_net
    # Initialize wireless network
    if not wl_net:
        wl_net = init_wifi()

    # Initialize DHT
    sensor = dht.DHT22(machine.Pin(4))

    # Main loop to read temp and send it
    # Read the temperature
    sensor.measure()
    temp = sensor.temperature() * 9.0 / 5.0 + 32.0
    humid = sensor.humidity()
    print('v1.2: Temp / Humid = {:2} / {:2}'.format(
            temp, humid))

    # Send it through MQTT
    mqtt_c = MQTTClient(MQ_CLIENT, MQ_BROKER_IP, user=MQ_USER,
                        password=MQ_PASSWORD)
    mqtt_c.connect()

    json_array = {
        "temp": "{}".format(temp),
        "hum": "{}".format(humid),
    }

    import ujson

#    {"source":"TV (0)","pvr_status":"NONE","powerstate":"Normal","tv_mode":"Cable (1)","volume":"7","channel_number":"45","channel_name":"Nat Geo HD","program_name":"Personaje ale nazismului","resolution":"1920x1080","error":false}

    mqtt_c.publish(MQ_TOPIC.encode('utf-8'), ujson.dumps(json_array), retain=True)

    mqtt_c.disconnect()

    # configure RTC.ALARM0 to be able to wake the device
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)

    # set RTC.ALARM0 to fire after 10 seconds (waking the device)
    rtc.alarm(rtc.ALARM0, 10000)  # For debugging, 10 seconds
    # rtc.alarm(rtc.ALARM0, 1000 * DELAY_MLOOP)  # Default: 60 seconds
    # Make sure that the Node MCU has pin D0 (L15) wired to RST (R3)

    # put the device to sleep
    machine.deepsleep()



if __name__ == '__main__':
    main()
