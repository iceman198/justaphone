## General info
https://www.waveshare.com/wiki/SIM7600G-H_4G_HAT

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

### AT Commands - GPS
Check if GPS is turned on
~ AT+CGPS?
Turn on GPS
~ AT+CGPS=1
Get GPS location info (may take some time to aquire a signal)
~ AT+CGPSINFO
Get GPS satelite info
~ AT+CGNSSINFO