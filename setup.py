import re

from setuptools import find_packages
from setuptools import setup


with open('README.md') as readme_file:
    readme = readme_file.read()

with open('standup/__init__.py') as f:
    # Not importing the file in setup.py!
    VERSION = re.search(r"__version__ = '(?P<version>.*?)'", f.read()).group('version')


REQUIREMENTS = [
    'click~=7.0',
    'jinja2~=2.10',
    'pyyaml~=3.13',
    'slackclient~=1.3',
]


setup(
    name='standup',
    version=VERSION,
    description='Write, publish, and keep track of your async standup reports',
    long_description=readme,
    author='Samuel Dion-Girardeau',
    author_email='samuel.diongirardeau@gmail.com',
    maintainer='Samuel Dion-Girardeau',
    maintainer_email='samuel.diongirardeau@gmail.com',
    url='https://github.com/samueldg/async-standups',
    packages=find_packages(
        include=[
            'standup',
            'standup.*',
        ],
    ),
    include_package_data=True,
    install_requires=REQUIREMENTS,
    zip_safe=False,
    keywords='standup',
    python_requires='~=3.6',
    platforms='any',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    license='MIT',
    entry_points={
        'console_scripts': [
            'standup = standup.main:cli',
        ],
    },
)
