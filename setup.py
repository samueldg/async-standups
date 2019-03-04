from setuptools import find_packages
from setuptools import setup


with open('README.md') as readme_file:
    readme = readme_file.read()


REQUIREMENTS = [
    'click~=7.0',
    'jinja2~=2.10',
    'pyyaml~=3.13',
    'slackclient~=1.3',
]


setup(
    name='standup',
    description='Write, publish, and keep track of your async standup reports',
    long_description=readme,
    author='Samuel Dion-Girardeau',
    author_email='samuel.diongirardeau@gmail.com',
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
    classifiers=[
        # TODO
    ],
    entry_points='''
        [console_scripts]
        standup=standup.main:cli
    ''',
)
