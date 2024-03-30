## General info
https://www.waveshare.com/wiki/SIM7600G-H_4G_HAT

## Ideas on how to do a menu
https://www.electronicshub.org/arduino-nokia-5110-menu/
## Network registration info
https://m2msupport.net/m2msupport/network-registration/

## Network selection
https://m2msupport.net/m2msupport/network-information-automaticmanual-selection/

## Carrier code info
https://en.wikipedia.org/wiki/Mobile_Network_Codes_in_ITU_region_3xx_(North_America)#United_States_of_America_-_US
Pretty sure I want to use "310 090" for AT&T

## AT Commands
ATI Get chip info
AT+CPMUTEMP Read the temperature of the module
AT+CBC Read the voltage value of the power supply
AT+CPOF Power down the device
AT+CEER Get an error repors - page 403 of the AT command manual

### AT Commands - SIM
Get Sim card #
~ AT+CICCID

### AT Commands - APN
Get APN info - may have to set it?
~ AT+CGDCONT?
To set APN password if needed
~ AT+CGAUTH?

#### SpeeTalk
APN Setting:
• APN: mobilenet
• APN username: (none)
• APN password: (none)
• IP Address: Dynamic
• Data Roaming: Enabled
Enable data roaming.

### AT Commands - Call
~ ATD1207#######; - call that number (semi-colon is needed at end)
~ AT+CHUP - hangup
~ ATA - Answer incoming call | Chip will send 'RING' with an incoming call

### AT Commands - Network
Get Network registration
~ AT+CSQ - get signal strength (https://m2msupport.net/m2msupport/atcsq-signal-quality/)
| Code | Strength |
| ---- | -------- |
| 0 | -113dBm or less |
| 1 | -111 dBm |
| 2...30 | -109... -53 dBm |
| 31 | -51 dBm or greater |
| 99 | not known or not detectable |
| 100 | -116 dBm or less |
| 101 | -115 dBm |
| 102...191 | -114... -26dBm |
    
~ AT+CREG?
Get Network info
~ AT+CPSI?
    Example response: +CPSI: LTE,Online,310-260,0x52F4,13116161,39,EUTRAN-BAND2,750,3,3,-125,-1139,-758,10


### AT Commands - GPS
Check if GPS is turned on
~ AT+CGPS?
Turn on GPS
~ AT+CGPS=1
Get GPS location info (may take some time to aquire a signal)
~ AT+CGPSINFO
Get GPS satelite info
~ AT+CGNSSINFO



