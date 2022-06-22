from distutils.core import setup

setup(
    name='fireblocks_defi_sdk_py',
    packages=['fireblocks_defi_sdk_py'],
    version='1.1',
    license='MIT',
    description='fireblocks_defi_sdk_py',
    author='Fireblocks',
    author_email='fireblocks@fireblocks.com',
    url='https://github.com/fireblocks/fireblocks-defi-sdk-py',
    download_url='https://github.com/fireblocks/fireblocks-defi-sdk-py/archive/refs/tags/1.1.tar.gz',
    keywords=['FIREBLOCKS', 'DeFi', 'SDK', 'PYTHON'],

    install_requires=[
        'fireblocks_sdk',
        'web3',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
