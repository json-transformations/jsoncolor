import ast
import json
import re
import sys
from setuptools import setup, find_packages
from setuptools.command.install import install
from pip.req import parse_requirements

# get __version__ from __init__.py
_version_re = re.compile(r'__version__\s+=\s+(.*)')
with open('jsoncolor/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

# load README.rst
if sys.version[0] == '3':
    with open('README.rst', 'r', encoding='utf-8') as f:
        readme = f.read()
else:
    with open('README.rst', 'r') as f:
        readme = f.read()

# load requirements.txt
requirements = parse_requirements('requirements.txt', session=False)
reqs = [str(i.req) for i in requirements]

# load requirements-dev.txt
requirements_dev = parse_requirements('requirements-dev.txt', session=False)
reqs_dev = [str(i.req) for i in requirements_dev]


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

    description="A JSON text coloring and highlighting tool",
    long_description=readme,

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
    install_requires=reqs,
    test_suite='tests',
    test_requires=reqs_dev,
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
