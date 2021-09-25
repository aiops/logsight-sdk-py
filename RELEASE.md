
Release process with GitHub and PyPI
====================================

How to release logsight SDK for Python


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

    + `git checkout develop` (checked out into develop branch)
    + `git pull origin develop --rebase` (update and merge any remote changes of the current branch)

2. Ensure unit tests are passing

    + `python -m unittest discover tests`

3. Ensure `CHANGES.md` (or changelog.txt?) is up to date with latest

    + This file is the project's authoritative change log and should reflect new features, fixes, and any significant changes.

4. Increment version number in `setup.py`

    + `python setup.py --version`

5. Commit all those changes with consistent comment

    + `git commit -a -m "Prep for $(python setup.py --version) release"`
    + `git push origin develop`

6. Created release branch

    + `git checkout -b release/$(python setup.py --version) origin/develop`
    + `git push origin release/$(python setup.py --version)` 

7. Branching and Merging

    + Once your branch is complete, i.e. you finished your new feature and are ready to add it to your main branch for a new release, simply merge your feature branch back into the main branch.
    + `git checkout main`
    + `git pull origin main` (update local main branch)
    + `git merge release/$(python setup.py --version)` (merge in your feature branch) or

8. Tagging
    + Once the project is in the state for creating the release, add a git tag with the release number
    + This will be reflected in the "releases" page of your GitHub repository.
    + `git tag -a $(python setup.py --version) -m "Prep for $(python setup.py --version) release"`

9. Push tag to remote

    + `git push origin main` (push main branch to remote repository)
    + `git push origin --tags` (push tags to remote repository)
   
10. Update develop branch

    + `git checkout develop`
    + `git merge release/$(python setup.py --version)`
    + `git push origin develop`

11. Remove release branch

    + `git branch -D release/$(python setup.py --version)`
    + `git push origin :release/$(python setup.py --version)`
    
13. Build locally

     + `rm -rf build`
     + `rm -rf dist`
     + `python3 setup.py sdist bdist_wheel`
     + `twine check dist/*` (report any problems rendering your README)

14. Release testing

    + Make sure you have a correct ~/.pypirc with your credentials from https://pypi.python.org/pypi
    + `twine upload --repository testpypi dist/*` (upload dist to PyPI Test)

15. Test the test release

    + `python3 -m pip install -i https://testpypi.python.org/pypi logsight` (attempt to install from PyPI test server)
    + When download packages from TestPyPI, you can specify --extra-index-url to point to PyPI
    + This is useful when the package you're testing has dependencies
    + `python3 -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ logsight`
    + `python3 -m pip uninstall logsight`

16. Release

    + `twine upload dist/*`
    + `python3 -m pip install logsight`
    

Consolidated instructions

```console
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

git tag -a $version -m "Prep for $version release"
git push origin main
git push origin --tags
   
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
python3 -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ logsight
python3 -m pip uninstall logsight

twine upload dist/*
python3 -m pip install logsight
```
