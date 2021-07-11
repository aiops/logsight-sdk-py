from setuptools import setup

version = '0.0.2'


setup(
    name='logsight',
    version=version,
    description='Python logging sender for logsight',
    author='Florian Schmidt',
    author_email='florian.schmidt@tu-berlin.de',
    url="https://github.com/aiops/logsight-python-sdk",
    project_urls={
        "Documentation": "http://logsight.readthedocs.io/en/latest/",
        "Source": "https://github.com/aiops/logsight-python-sdk",
        "Tracker": "https://github.com/aiops/logsight-python-sdk/issues",
    },
    license='unlicense',
    packages=['logsight'],
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
        "requests>=2.25.1",
    ],
    zip_safe=False
)
