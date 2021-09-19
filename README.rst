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

How to release logsight

+ https://sherif.io/2016/09/30/Python-package-with-GitHub-PyPI.html

Project Stages
--------------

This project has three stages of release:

+ Unstable
    + The tip or HEAD of the master branch is referred to as unstable
+ Staged
    + A commit tagged with the suffix `-rc\d+` is a staged release/release candidate (e.g., `v0.3.1-rc2`)
+ Stable
    + A commit tagged without suffix `-rc\d+` is a stable release (e.g., `v0.3.1`)

There are no steps necessary to create an unstable release as that happens automatically whenever an untagged commit is pushed to `develop`.
However, the following workflow should be used when tagging a `staged release candidate` or `stable release`.


Workflow
--------

1. Checkout

    + `git checkout develop`
    + `git pull --rebase`

1. Ensure unit tests are passing

    + `python -m unittest discover tests`

3. Ensure `CHANGES.md` (or changelog.txt?) is up to date with latest

    + This file is the project's authoritative change log and should reflect new features, fixes, and any significant changes.

4. Increment version number in `setup.py`

    + `python setup.py --version`

5. Commit all those changes with consistent comment

    + `git commit -a -m "Prep for v$(python setup.py --version)-rc1 release candidate"`
    + `git push`

6. Branching and Merging

    + Once your branch is complete, ie. you finished your new feature and are ready to add it to your main branch for a new release, simply merge your feature branch back into the main branch.
    + `git checkout main`
    + `git pull`
    + `git merge develop` (merge in your feature branch) or
    + `git pull origin develop` (pull down your feature branch)
    + `git push`

6. Tagging
    + Once you have the project in the state you want for creating the release, you add a git tag with the version number of the release.
    + This will be reflected in the "releases" page of your GitHub repository.

    + `git tag -a v1.2.3-rc1 -m "Tag description v1.2.3-rc1"` or
    + `git tag -a v$(python setup.py --version) -m 'description'`
    + Show list of the existing tags
    + `git tag`

7. Push tag to remote

    + `git push origin v1.2.3-rc1` or
    + `git push --tags origin develop`

8. Confirm that GitHub has generated the release file

    + Browse to releases page and make sure the new version has a release entry
    + https://github.com/aiops/logsight-python-sdk/releases

9. Release testing

    + `python setup.py register -r pypitest` (register the package with PyPI testpypi.python.org)
    + `python setup.py sdist upload -r pypitest` (upload the stuff to PyPI Test)

10. Test the test release

    + `python3 -m pip install -i https://testpypi.python.org/pypi logsight` (attempt to install from PyPI test server)
    + When download packages from TestPyPI, you can specify --extra-index-url to point to PyPI
    + This is useful when the package you're testing has dependencies
    + `python3 -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ logsight`
    + `pip uninstall logsight`

11. Release

    + `rm -rf build; rm -rf dist;`
    + `python setup.py register -r pypi`
    + `python setup.py sdist upload -r pypi`
    + `pip install logsight`
    
