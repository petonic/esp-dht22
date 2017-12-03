# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import gc
#import webrepl
#webrepl.start()
gc.collect()

#
# Automatically execute the main Remote Temp sensor
# code.  The configuration is located at esp:/config.py
#
# [2017-09-24 SUN 13:06]
#
#
