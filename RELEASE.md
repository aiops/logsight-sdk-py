Release workflow
================

Commit Messages
---------------
Commit messages should be tagged to enable a detailed automated
changelog generation:

-   \'chg\' is for refactor, small improvement, cosmetic changes\...
-   \'fix\' is for bug fixes
-   \'new\' is for new features, big improvement

Tags follow Semantic Versioning (<https://semver.org>): Major, Minor,
Patch.

Branch Strategy
---------------
We have two branches: `main` and `develop`.
The `main` branch contains the latest version which can be installed by users.
It is always behind `develop`, until it is merged before a major release.

Release Locations
-----------------
Releases logsight SDK for Python to the following external systems:

- [GitHub](https://github.com/aiops/logsight-sdk-py)
- [Test PyPI](https://test.pypi.org/search/?q=%22logsight-sdk-py%22&o=) and
    [PyPI](https://pypi.org/search/?q=%22logsight-sdk-py%22&o=)


How to release
--------------
We use executable Markdown to execute this RELEASE.md file.
The bash script code below can be executed by running the following command:
+ $ release.sh RELEASE.md

CI/CD workflow
---------------
Once the previous step is executed and the code is pushed to GitHub, the git actions in `.github/workflows/` run.


Bash workflow
-------------

```bash
set -o xtrace
function git_cmd_unsuccessful {
    set +o xtrace
    RED='\033[0;31m'
    echo -e "${RED}The git command failed. You need to manually fix the problem."
    echo -e "${RED}Check commands already executed and execute the remaining commands manually."
    echo -e "${RED}You probably will need to: $ version=<current version> ."
    read -p "Press [Enter] key to exit..."
    exit 1  
} 
function pause_for_changelog {
    set +o xtrace
    NOCOLOR='\033[0m'
    YELLOW='\033[0;33m' 
    echo -e "${YELLOW}Update manually the CHANGLOG.md file."
    echo -e "Press [Enter] key when done...${NOCOLOR}"
    read < /dev/tty
    set -o xtrace
} 
set -e
trap 'git_cmd_unsuccessful' ERR

#. Update your local develop branch in case someone made changes to the remote develop branch
git checkout develop
git pull

# update release version
prev_version=$(python setup.py --version)
echo "Previous release: $prev_version"
version=$(echo $prev_version | perl -pe 's/^((\d+\.)*)(\d+)(.*)$/$1.($3+1).$4/e')
echo "New release: $version"

# In case you need to set the ngitew version manually, do it here
#version='0.2.0'

# Create a branch from the current HEAD (does not touch local changes)
git checkout -b release/$version develop

# Update automatically or manually the version in setup.py and ./logsight_cli/logsight-cli.py
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    sed -i "/^VERSION/s;[^ ]*$;'$version';" setup.py
elif [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i "" "/^VERSION/s;[^ ]*$;'$version';" setup.py
else
    echo "OS is not supported"
fi

# Update the changelog
gitchangelog ^$prev_version HEAD
pause_for_changelog
    
git commit -a -m "Preparation for release $version"

#. Update main branch
git checkout main
git pull
git merge --no-ff release/$version -m "Release $version"
git tag -a $version -m "Release $version"
git push --atomic --tags
git push origin main

#. Update develop branch
git checkout develop
git pull
git merge --no-ff release/$version -m "Release $version"
git push origin develop

#. Remove release branch
git branch -D release/$version

exit 0
# Warning: The following commands are implemented using Github actions
# They should not be executed manually

rm -rf build
rm -rf dist
python3 setup.py sdist bdist_wheel
twine check dist/*

twine upload --repository testpypi dist/*
python3 -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ logsight-cli-py
python3 -m pip uninstall logsight-cli-py

twine upload dist/*
python3 -m pip install logsight-cli-py
}
```
