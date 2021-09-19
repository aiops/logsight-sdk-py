![log-quality](https://img.shields.io/badge/log%20quality-70-brightgreen)

|PyPI version shields.io|
|PyPI license|

.. |PyPI version shields.io| image:: https://img.shields.io/pypi/v/ansicolortags.svg
   :target: https://pypi.python.org/pypi/ansicolortags/

.. |PyPI license| image:: https://img.shields.io/pypi/l/ansicolortags.svg
   :target: https://pypi.python.org/pypi/ansicolortags/


logsight SDK 
============

VPN to testbed
--------------
+ Install [OpenVPN](https://openvpn.net/cloud-docs/openvpn-3-client-for-linux/) or [OpenVPN for Mac](https://openvpn.net/client-connect-vpn-for-mac-os/)
+ sudo openvpn3 session-start --config your_vpn_file.ovpn

To shoutdown the VPN
+ pgrep openvpn | xargs sudo kill -9

Endpoint
+ http://wally113.cit.tu-berlin.de:4200/


Release process with GitHub and PyPI
====================================
+ https://sherif.io/2016/09/30/Python-package-with-GitHub-PyPI.html

1. Ensure unit tests are passing
   + `python -m unittest discover tests`
3. Ensure everything is pushed to master (develop?) and is working
4. Ensure `CHANGES.md` (or changelog.txt?) is up to date with latest
5. Increment version number in `setup.py`
6. Commit all those changes
   + Commit above changes for a with consistent comment
   + e.g., "Prep for 0.2.5 release"
7. Tag the repo
   + Once you have the project in the state you want for creating the release, you add a git tag with the version number of the release. This will be reflected in the “releases” page of your GitHub repository.
   + `git tag 1.2.3 -m "Adds 1.2.3 tag for PyPI"`
   + `git tag -a v$(python setup.py --version) -m 'description'`
8. Push git tag to remote
   + `git push origin 1.2.3` or
   + `git push --tags origin develop`
9. Confirm that GitHub has generated the release file
   + Browse to releases page and make sure the new version has a release entry
   + https://github.com/aiops/logsight-python-sdk/releases
10. Release testing
    + Register and upload to testpypi.python.org
    + `python setup.py register -r pypitest`
    + `python setup.py sdist upload -r pypitest`
11. Test the test release
    + `pip install -i https://testpypi.python.org/pypi logsight`
    + When download packages from TestPyPI, you can specify --extra-index-url to point to PyPI
    + This is useful when the package you're testing has dependencies
    + `python3 -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ logsight`
    + `pip uninstall logsight`
12. Release
    + `rm -rf build; rm -rf dist;`
    + `python setup.py register -r pypi`
    + `python setup.py sdist upload -r pypi`
    + `pip install logsight`
    
