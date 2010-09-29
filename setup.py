from setuptools import setup

setup(
    name='sparkup',
    version='0.2',
    author='Rico Sta. Cruz',
    author_email='rico@ricostacruz.com',
    py_modules=['sparkup'],
    package_dir={'': 'src/sparkup'},
    url='http://github.com/rstacruz/sparkup',
    license='mit-license.txt',
    description='A parser for a condensed HTML format.',
    entry_points={
        'console_scripts': [
            'sparkup = sparkup:main',
        ],
    },
)
