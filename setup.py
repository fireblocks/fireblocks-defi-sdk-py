from distutils.core import setup

setup(
    name='fireblocks_defi_sdk',
    packages=[
        'fireblocks_defi_sdk_py',
        'fireblocks_defi_sdk_py.tokenization',
        'fireblocks_defi_sdk_py.tokenization.tokens',
        'fireblocks_defi_sdk_py.tokenization.utils',
        'fireblocks_defi_sdk_py.tokenization.examples'
    ],
    version='1.0.2',
    license='MIT',
    description='fireblocks_defi_sdk_py',
    long_description="""Fireblocks python SDK""",
    long_description_content_type='text/markdown',
    author='Fireblocks',
    author_email='fireblocks@fireblocks.com',
    url='https://github.com/fireblocks/fireblocks-defi-sdk-py',
    download_url='https://github.com/fireblocks/fireblocks-defi-sdk-py/archive/refs/tags/1.0.2.tar.gz',
    keywords=['FIREBLOCKS', 'DeFi', 'SDK', 'PYTHON'],
    install_requires=[
        'fireblocks_sdk==1.17.3',
        'web3==5.26.0'
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
        'Programming Language :: Python :: 3.11'
    ]
)
