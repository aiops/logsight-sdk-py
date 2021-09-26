from setuptools import setup

version = '0.0.18'

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='logsight-sdk-py',
    version=version,
    description='Logsight SDK Python',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author='Jorge Cardoso',
    author_email='jorge.cardoso.pt@gmail.com',
    url="https://github.com/aiops/logsight-sdk-py",
    project_urls={
        "Documentation": "http://logsight.readthedocs.io/en/latest/",
        "Source": "https://github.com/aiops/logsight-sdk-py",
        "Tracker": "https://github.com/aiops/logsight-sdk-py/issues",
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
        "requests",
    ],
    zip_safe=False
)
