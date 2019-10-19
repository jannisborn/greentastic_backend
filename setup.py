"""Package installer."""
import os
from setuptools import setup
from setuptools import find_packages

LONG_DESCRIPTION = ''
if os.path.exists('README.md'):
    with open('README.md') as fp:
        LONG_DESCRIPTION = fp.read()

REQUIREMENTS = []
if os.path.exists('requirements.txt'):
    with open('requirements.txt') as fp:
        REQUIREMENTS = [
            line.strip()
            for line in fp
        ]

scripts = []

setup(
    name='Greentastic',
    version='0.0.1',
    description='Hackzurich 2019 project: Greentastic - a transportation mode recommendation app',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author='Jannis Born, Nina Wiedemann, Raul Catena',
    author_email='jannis.born@gmx.de, nwiedemann@uos.de',
    license='MIT',
    install_requires=REQUIREMENTS,
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=find_packages(),
    scripts=scripts
)