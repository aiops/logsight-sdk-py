![log-quality](https://img.shields.io/badge/log%20quality-70-brightgreen)

# logsight SDK 

## VPN to testbed
+ Install [OpenVPN](https://openvpn.net/cloud-docs/openvpn-3-client-for-linux/) or [OpenVPN for Mac](https://openvpn.net/client-connect-vpn-for-mac-os/)
+ sudo openvpn3 session-start --config your_vpn_file.ovpn

To shoutdown the VPN
+ pgrep openvpn | xargs sudo kill -9

 
## Run tests

+ http://wally113.cit.tu-berlin.de:4200/


## Running all the tests

+ python -m unittest discover tests


## 

When download packages from TestPyPI, you can specify --extra-index-url to point to PyPI. This is useful when the package you're testing has dependencies:

+ python3 -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ logsight