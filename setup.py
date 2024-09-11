# setup.py
from setuptools import setup, find_packages

setup(
    name='pyramid_score',
    version='0.1',
    description='Análise de clientes com RFM Pyramid Score',
    author='Renato Cesar Menendes Cruz',
    author_email='renatomenendes@yahoo.com.br',
    packages=find_packages(),
    install_requires=[
        'pandas>=1.0',
        'numpy>=1.18',
        'matplotlib>=3.0'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ],
)
