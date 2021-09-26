
Release process
===============

Releases logsight SDK for Python to the following external systems:

+ GitHub_
+ `Test PyPI`_ and PyPI_

.. _github: https://github.com/aiops/logsight-sdk-py
.. _test pypi: https://test.pypi.org/search/?q=%22logsight-sdk-py%22&o=
.. _pypi: https://pypi.org/search/?q=%22logsight-sdk-py%22&o=


Project Stages
--------------

This project has three stages of release:

+ Unstable
    + The tip or HEAD of the `develop` branch is referred to as unstable
+ Staged
    + A commit tagged with the suffix `-rc\d+` is a release candidate (e.g., `0.3.1-rc2`)
+ Stable
    + A commit tagged without suffix `-rc\d+` is a stable release (e.g., `0.3.1`)

Tags follow `Semantic Versioning`_.
There are no steps necessary to create an unstable release as that happens automatically whenever an untagged commit is pushed to `develop`.
However, the following workflow should be used when tagging a `staged release candidate` or `stable release`.

.. _Semantic Versioning: https://semver.org


Preproduction
-------------

To test the SDK with a preproduction server, install OpenVPN_ and point the VPN to the running testbed_ using your config file `your_vpn_file.ovpn`.

.. _openvpn: https://openvpn.net/cloud-docs/openvpn-3-client-for-linux/
.. _testbed: http://wally113.cit.tu-berlin.de:4200/

.. code-block:: console

    sudo openvpn3 session-start --config your_vpn_file.ovpn


Workflow
--------

#. Checkout

    + `git checkout develop` (checked out into develop branch)
    + `git pull origin develop --rebase` (update and merge any remote changes of the current branch)

#. Ensure unit tests are passing

    + `python -m unittest discover tests`

#. Ensure `CHANGES.md` (or changelog.txt?) is up to date with latest

    + This file is the project's authoritative change log and should reflect new features, fixes, and any significant changes.

#. Increment version number in `setup.py`

    + `python setup.py --version`

#. Commit all those changes with consistent comment

    + `git commit -a -m "Prep for $(python setup.py --version) release"`
    + `git push origin develop`

#. Created release branch

    + `git checkout -b release/$(python setup.py --version) origin/develop`
    + `git push origin release/$(python setup.py --version)` 

#. Branching and Merging

    + Once your branch is complete, i.e. you finished your new feature and are ready to add it to your main branch for a new release, simply merge your feature branch back into the main branch.
    + `git checkout main`
    + `git pull origin main` (update local main branch)
    + `git merge release/$(python setup.py --version)` (merge in your feature branch) or

#. Tagging

    + Once the project is in the state for creating the release, add a git tag with the release number
    + This will be reflected in the "releases" page of your GitHub repository.
    + `git tag -a $(python setup.py --version) -m "Prep for $(python setup.py --version) release"`

#. Push tag to remote

    + `git push origin main` (push main branch to remote repository)
    + `git push origin --tags` (push tags to remote repository)
   
#. Update develop branch

    + `git checkout develop`
    + `git merge release/$(python setup.py --version)`
    + `git push origin develop`

#. Remove release branch

    + `git branch -D release/$(python setup.py --version)`
    + `git push origin :release/$(python setup.py --version)`
    
#. Build locally

    + `rm -rf build`
    + `rm -rf dist`
    + `python3 setup.py sdist bdist_wheel`
    + `twine check dist/*` (report any problems rendering your README)

#. Release testing

    + Make sure you have a correct ~/.pypirc with your credentials from https://pypi.python.org/pypi
    + `twine upload --repository testpypi dist/*` (upload dist to PyPI Test)

#. Test the test release

    + `python3 -m pip install -i https://testpypi.python.org/pypi logsight-sdk-py` (attempt to install from PyPI test server)
    + When download packages from TestPyPI, you can specify --extra-index-url to point to PyPI
    + This is useful when the package you're testing has dependencies
    + `python3 -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ logsight-sdk-py`
    + `python3 -m pip uninstall logsight-sdk-py`

#. Release

    + `twine upload dist/*`
    + `python3 -m pip install logsight-sdk-py`
    

Bash workflow
-------------

.. code-block:: console

    git checkout develop
    git pull origin develop --rebase

    # python -m unittest discover tests`
    # Update `CHANGES.md`
    # Update the version in setup.py

    version=$(python setup.py --version)
    git commit -a -m "Prep for $version release"
    git push origin develop
    git checkout -b release/$version origin/develop
    git push origin release/$version

    git checkout main
    git pull origin main
    git merge release/$version

    git tag -a $version -m "Release $version"
    # git push origin $version
    # git push origin --tags
    git push --atomic origin main $version

    git checkout develop
    git merge release/$version
    git push origin develop

    git branch -D release/$version
    git push origin :release/$version

    rm -rf build
    rm -rf dist
    python3 setup.py sdist bdist_wheel
    twine check dist/*

    twine upload --repository testpypi dist/*
    python3 -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ logsight-sdk-py
    python3 -m pip uninstall logsight-sdk-py

    twine upload dist/*
    python3 -m pip install logsight-sdk-py
