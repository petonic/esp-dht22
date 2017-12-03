#
# Config file for rem_temp
#
# Contains WIFI credentials, MQTT Broker Address, MQTT Pub Channel

# Wifi Credentials
WL_SSID      = 'PanchoNet'
WL_PASSWD    = 'asdfZXC12'
WL_MYIP      = '192.168.86.69'      # DHCP Locked to this ESP8266
WL_ROUTER    = '192.168.86.1'
WL_NETMASK   = '255.255.255.0'
WL_DNS       = '8.8.8.8'           # DNS -- not sure that this is needed at all

# MQTT Constants
MQ_BROKER_IP = '192.168.86.52'      # PanchoMe.local
MQ_TOPIC     = 'dht22/mobile1'
MQ_CLIENT    = 'dht_mob_1'
MQ_PORT      = '1883'              # 1883 is the default for MQTT
MQ_USER      = "ha-mqtt"
MQ_PASSWORD  = "asdfZXC12"

# DHT-22 Constants
DHT_PIN      = 4                   # This is marked as D2 on the Node MCU

# Program constants
DELAY_SEEK   = 10                  # Number of secs between WIFI searches
DELAY_MLOOP  = 60                  # Number of secs between temp readings
