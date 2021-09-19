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

## Tagging

git tag -a v$(python setup.py --version) -m 'description of version v$(python setup.py --version)'


## TestPyPi

When download packages from TestPyPI, you can specify --extra-index-url to point to PyPI. This is useful when the package you're testing has dependencies:

+ python3 -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ logsight

## Development process

+ https://sherif.io/2016/09/30/Python-package-with-GitHub-PyPI.html


Nothing novel here, just want these instructions all in one place for my own use.

1.) Ensure everything is pushed to master and is working

2.) Ensure `CHANGES.md` is up to date with latest

3.) Ensure version in `setup.py` is incremented

4.) Tag the repo - e.g., `git tag 0.2 && git push origin 0.2`

5.) Draft a release with the latest tag and the content from `CHANGES.md`

6.) Create the build - `rm -rf build; rm -rf dist; python setup.py sdist bdist_wheel`

7.) Upload to Pypi using Twine - `twine upload dist/*`