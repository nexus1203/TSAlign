from setuptools import setup, find_packages

setup(
    name='TSAlign',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A fast library to align two 1D time-series using FFT based convolution.',
    long_description=open('README.md').read(),
    long_description_content_type='',
    url='https://github.com/nexus1203/TSAlign',
    packages=find_packages(),
    
    install_requires=[
        'numpy',
        'scipy'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)