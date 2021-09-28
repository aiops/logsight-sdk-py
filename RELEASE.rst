
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


Feature Workflow
----------------
The workflow uses two branches:

+ main branch. Stores the production-ready state.
+ develop branch. Contains the complete history of the project with new
  features. Create an empty develop branch locally and push it to the server:

.. code-block:: console

    git branch develop
    git push -u origin develop


#. Create feature branch

+ Feature branches are created off the latest develop branch.

.. code-block:: console

    git checkout develop
    git checkout -b feature_branch
    git push origin feature_branch
    # work happens on feature branch
    # Periodically merge changes on the develop branch to avoid conflicts


#. Include features on develop

+ When the feature is finished, merge the feature_branch into develop.

.. code-block:: console

    git checkout develop
    git merge --no-ff feature_branch
    git branch -d feature_branch
    git push origin develop

The --no-ff flag causes the merge to always create a new commit object,
even if the merge could be performed with a fast-forward.


Release Workflow
----------------

Once several features have been implemented, a release is created by forking a release branch off of develop.
The release branch starts a new release cycle.
Only bug fixes, documentation, and other release-oriented tasks go in the branch.
Once ready, the release branch is merged into main and tagged with a version number.
It is also merged back into develop, since it may have diverged since the release was initiated.


#. Increment version number in `setup.py`

    + `python setup.py --version`

#. Created release branch

    + `version=$(python setup.py --version)`
    + `git checkout -b release/$(python setup.py --version) develop`

#. Ensure unit tests are passing
    + Apply bug fixes (rather than on the develop branch)
    + Adding large new features is not allowed
    + `python -m unittest discover tests`

#. Ensure `CHANGES.md` (or changelog.txt?) is up to date with latest

    + This file is the project's authoritative change log and should reflect new features, fixes, and any significant changes.

#. Commit all those changes with consistent comment

    + `git commit -a -m "Prep for $(python setup.py --version) release"`

#. Tagging

    + Once the project is in the state for creating the release, add a git tag with the release number
    + The tag will be used by github actions to trigger the release
    + This will be reflected in the "releases" page of your GitHub repository.

#. Push tag to remote

    + Push the commits to origin main branch together with tag reference tag-name
    + `git push --atomic origin main $version`

#. Update main branch

    + Tag commit on master for easy future reference to this version
    + `git checkout main`
    + `git merge --no-ff release/$(python setup.py --version)`
    + `git push origin main`
    + `git tag -a $(python setup.py --version) -m "Release $(python setup.py --version)"`
    + `git push --tags`

#. Update develop branch

    + `git checkout develop`
    + `git merge --no-ff release/$(python setup.py --version)`
    + `git push origin develop`

#. Remove release branch

    + `git branch -d release/$(python setup.py --version)`

    
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

    # Warning: The following commands should be executed manually
    # Execute tests python -m unittest discover tests`
    # Update `CHANGES.md`
    # Update the version in setup.py

    # Make the documentation
    # cd docs ; make clean ; make html ; cd ..

    # Execute tests
    # tox

    version=$(python setup.py --version)
    git commit -a -m "Prep for $version release"
    git push origin develop
    git checkout -b release/$version origin/develop
    git push origin release/$version

    git checkout main
    git pull origin main
    git merge release/$version

    git tag -a $version -m "Release $version"
    git push --atomic origin main $version

    git checkout develop
    git merge release/$version
    git push origin develop

    git branch -D release/$version
    git push origin :release/$version

    # Warning: The following commands are implemented using Github actions
    # They should not be executed manually

    rm -rf build
    rm -rf dist
    python3 setup.py sdist bdist_wheel
    twine check dist/*

    twine upload --repository testpypi dist/*
    python3 -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ logsight-sdk-py
    python3 -m pip uninstall logsight-sdk-py

    twine upload dist/*
    python3 -m pip install logsight-sdk-py
