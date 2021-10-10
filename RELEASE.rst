
Release workflow
================

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
    + A commit tagged `without` suffix `-rc\d+` is a stable release (e.g., `0.3.1`)

Tags follow `Semantic Versioning`_: Major, Minor, Patch.
There are no steps necessary to create an unstable release as that happens automatically whenever an untagged commit is pushed to `develop`.
However, the following workflow should be used when tagging a `staged release candidate` or `stable release`.

+ `Major`: incremented when you add breaking changes, e.g. an incompatible API change
+ `Minor`: incremented when you add backward compatible functionality
+ `Patch`: incremented when you add backward compatible bug fixes

.. _Semantic Versioning: https://semver.org

Commit messages should be tagged to enable a detailed automated changelog generation:

+ 'chg' is for refactor, small improvement, cosmetic changes...
+ 'fix' is for bug fixes
+ 'new' is for new features, big improvement


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

#. Update develop branch in case someone made changes

.. code-block:: console

    git checkout develop
    git pull --rebase

#. Created release branch

.. code-block:: console

    version=$(python setup.py --version)
    echo $version

    # update manually release version
    ? version=$version+1

    git checkout -b release/$version develop


#. Ensure unit tests are passing
    + Apply bug fixes (rather than on the develop branch)
    + Adding large new features is not allowed

.. code-block:: console

    python -m unittest discover tests


#. Ensure `CHANGES.md` (or changelog.txt?) is up to date with latest

    + This file is the project's authoritative change log and should reflect new features, fixes, and any significant changes.


#. Commit all those changes with consistent comment

.. code-block:: console

    git commit -a -m "Prep for $(python setup.py --version) release"


#. Update main branch

.. code-block:: console

    git checkout main
    git merge --no-ff release/$version -m "$version release"
    git push origin main
    git tag -a $version -m "Release $version"
    git push --tags


#. Update develop branch

.. code-block:: console

    git checkout develop
    git merge --no-ff release/$version -m "$version release"
    git push origin develop


#. Remove release branch

.. code-block:: console

    git branch -D release/$version


#. Build locally

.. code-block:: console

    rm -rf build
    rm -rf dist
    python3 setup.py sdist bdist_wheel
    twine check dist/* # (report any problems rendering your README)


#. Release testing

    + Make sure you have a correct ~/.pypirc with your credentials from https://pypi.python.org/pypi

.. code-block:: console

    twine upload --repository testpypi dist/* # (upload dist to PyPI Test)


#. Test the test release

    + When download packages from TestPyPI, you can specify --extra-index-url to point to PyPI
    + This is useful when the package you're testing has dependencies

.. code-block:: console

    python3 -m pip install -i https://testpypi.python.org/pypi logsight-sdk-py # (attempt to install from PyPI test server)
    python3 -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ logsight-sdk-py
    python3 -m pip uninstall logsight-sdk-py


#. Release

.. code-block:: console

    twine upload dist/*
    python3 -m pip install logsight-sdk-py



Bash workflow
-------------

.. code-block:: console

    #. Update develop branch in case someone made changes
    git checkout develop
    git pull --rebase
    git push

    #. Created a new release id
    prev_version=$(python setup.py --version)
    echo "Previous release: $prev_version"
    # update release version
    version=$(echo $prev_version | perl -pe 's/^((\d+\.)*)(\d+)(.*)$/$1.($3+1).$4/e')
    echo "New release: $version"

    # Create a branch from the current HEAD (does not touch local changes)
    git checkout -b release/$version develop

    # Warning: The following commands should be executed manually
    # Execute tests
    # $ python -m unittest discover tests`

    # Update the changelog
    # add commit message from HEAD to the previous tag
    # echo -e "$(git log --pretty='- %s' $prev_version..HEAD)\n\n$(cat CHANGELOG.rst)" > CHANGELOG.rst
    # Run gitchangelog to manually add changelog entries
    gitchangelog ^$prev_version HEAD

    # Update the version in setup.py
    # $ vi setup.py or
    sed -i "/^version/s;[^ ]*$;'$version';" setup.py
    # BSD/MacOS: sed -i "" "/^version/s;[^ ]*$;'$version';" setup.py

    # Make the documentation
    # Documentation is at:
    # - https://www.sphinx-doc.org/en/master/tutorial/
    # - https://www.sphinx-doc.org/_/downloads/en/master/pdf/
    cd docs ; make clean ; make html ; cd ..

    # Execute tests
    # tox

    git commit -a -m "Preparation for release $version"

    #. Update main branch
    git checkout main
    git merge --no-ff release/$version -m "Release $version"
    git push origin main
    git tag -a $version -m "Release $version"
    git push --tags

    #. Update develop branch
    git checkout develop
    git merge --no-ff release/$version -m "Release $version"
    git push origin develop

    #. Remove release branch
    git branch -D release/$version

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
