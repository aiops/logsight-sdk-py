
Setup VPN 
==========

Prerequisite
------------
Install you preferred VPN software 
  + [OpenVPN](https://openvpn.net/cloud-docs/openvpn-3-client-for-linux/)
  + [OpenVPN for Mac](https://openvpn.net/client-connect-vpn-for-mac-os/)

Testbed
--------
The testbed is running in server:
+ http://wally113.cit.tu-berlin.de:4200/


Set VPN 
--------
Establish a VPN
+ sudo openvpn3 session-start --config your_vpn_file.ovpn

To shutdown the VPN
+ pgrep openvpn | xargs sudo kill -9



