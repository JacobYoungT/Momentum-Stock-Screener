from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='momentum_calculator',
    version='0.1.0',
    description='Momentum calculator for stocks in the S&P 500.',
    author='Jacob Young',
    author_email='jacob.schodt.thomsen@gmail.com',
    packages=find_packages(),
    install_requires=requirements
)