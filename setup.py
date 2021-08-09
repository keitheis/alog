from setuptools import setup

with open("README.rst", "r", encoding="utf-8") as f:
    README = f.read()
with open("CHANGES.rst", "r", encoding="utf-8") as f:
    CHANGES = f.read()

testing_extras = [
    'pytest-cov',
]

docs_extras = [
    'Sphinx >= 1.3.1',
]

setup(
    name='alog',
    version='1.2.0',
    description='Your goto Python logging without panic on context swtich',
    long_description=README + CHANGES,
    long_description_content_type="text/x-rst",
    url='https://github.com/keitheis/alog',
    author='Keith Yang',
    author_email='yang@keitheis.org',
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: System :: Logging',
        'Topic :: Software Development',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
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
