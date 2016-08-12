import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
try:
    with open(os.path.join(here, 'README.rst')) as f:
        README = f.read()
    with open(os.path.join(here, 'CHANGES.rst')) as f:
        CHANGES = f.read()
except IOError:
    README = CHANGES = ''

testing_extras = [
    'pytest',
    'coverage',
    'pytest-cov',
]

docs_extras = [
    'Sphinx >= 1.3.1',
]

setup(
    name='alog',
    version='0.9.1',
    description='Just alog',
    long_description='',
    url='https://github.org/keitheis/alog',
    author='Keith Yang',
    author_email='yang@keitheis.org',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        "Topic :: System :: Logging",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='simple basic log',
    packages=['alog'],
    zip_safe=True,
    extras_require={
        'testing': testing_extras,
        'docs': docs_extras,
    },
)
