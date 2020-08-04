from setuptools import setup, find_packages


setup(
    name='ngsimple',
    version='0.1.0',
    description='A simple Python wrapper for running Netgen in a container',
    url='https://github.com/kinnala/ngsimple',
    author='Tom Gustafsson',
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Mathematics',
    ],
    packages=find_packages(),
    install_requires=['docker', 'meshio>=4.0.4'],
)
