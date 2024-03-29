from setuptools import find_packages, setup

VERSION = '0.2.7'


with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='logsight-sdk-py',
    version=VERSION,
    description='Logsight SDK Python',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author='logsight.ai',
    author_email='support@logsight.ai',
    url="https://github.com/aiops/logsight-sdk-py",
    project_urls={
        "Documentation": "https://logsight-sdk-py.readthedocs.io/en/latest/",
        "Source": "https://github.com/aiops/logsight-sdk-py",
        "Tracker": "https://github.com/aiops/logsight-sdk-py/issues",
    },
    license='unlicense',
    packages=find_packages(exclude=("test",)),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests",
        "python-dateutil",
    ],
    zip_safe=False
)
