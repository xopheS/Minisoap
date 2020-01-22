from setuptools import setup, find_packages

setup(name='minisoap',
    version='0.1b',
    install_requires=['colorama', 'numpy', 'SoundCard'],
    license='GPL 3',
    author= 'Mohamed H, Christophe Saad, Nizar Ghandri',
    packages=['minisoap'],
    entry_points={'console_scripts': ['minisoap = minisoap.minisoap:wrapper']},
    setup_requires=['wheel']
)
