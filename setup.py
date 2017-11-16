import ast
import json
import re
import sys
from setuptools import setup, find_packages
from setuptools.command.install import install


# get __version__ from __init__.py
_version_re = re.compile(r'__version__\s+=\s+(.*)')
with open('jsoncolor/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))


# post-installation command
class PostInstallCommand(install):
    """Post-Installation to create configuration file."""
    def run(self):
        from jsoncolor.config import config_profile
        config_profile()
        install.run(self)


setup(
    name="jsoncolor",
    version=version,
    url="https://github.com/json-transformations/jsoncolor",
    keywords=[],

    author="Tim Phillips",
    author_email="phillipstr@gmail.com",

    description="A JSON content terminal coloring tool",

    packages=find_packages(include=['jsoncolor']),
    include_package_data=True,
    zipsafe=False,

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ],

    install_requires=[
        'jsoncut',
        'jsonconfig-tool',
        'click>=6.0',
        'pygments',
    ],

    test_suite='tests',
    test_requires=[
        'pytest-cov',
        'flake8',
        'tox',
    ],

    setup_requires=['pytest-runner'],
    entry_points={
        'console_scripts': [
            'jsoncolor='
            'jsoncolor.cli:main']
    },
    cmdclass={
        'install': PostInstallCommand,
        'develop': PostInstallCommand,
    },
)
