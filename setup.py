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
    'pytest-cov',
]

docs_extras = [
    'Sphinx >= 1.3.1',
]

setup(
    name='alog',
    version='0.9.13',
    description='Python logging for Humans',
    long_description=README + '\n\n' + CHANGES,
    url='https://github.com/keitheis/alog',
    author='Keith Yang',
    author_email='yang@keitheis.org',
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: System :: Logging',
        'Topic :: Software Development',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    keywords='simple basic application logging print',
    packages=['alog'],
    package_data={'': ['LICENSE']},
    zip_safe=False,
    extras_require={
        'testing': testing_extras,
        'docs': docs_extras,
    },
)
