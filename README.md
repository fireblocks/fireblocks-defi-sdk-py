# Fireblocks Python DeFi SDK
[![PyPI version](https://badge.fury.io/py/fireblocks-defi-sdk-py.svg)](https://badge.fury.io/py/fireblocks-defi-sdk-py)

The Fireblocks Python DeFi SDK provides an interoperability layer between Fireblocks Smart Contract API and common DeFi libraries.
For more information on Fireblocks Smart Contract API and automating DeFi workflows on Fireblocks [read here](https://support.fireblocks.io/hc/en-us/articles/360017709160-Fireblocks-Smart-Contract-API).

Please email us at support@fireblocks.com if you have questions or feedback.
# Table Of Contents
- [Features](#Features)
  - [Web3 Bridge](#Bridge)
  - [NFT](#Tokens)
- [Usage](#Usage)
  - [Installation](#Installation)
  - [Requirements](#Requirements)
- [Code Examples](#Examples)
  - [Bridge](#Bridge)
  - [NFT](#NFT)

## Features
### Bridge
Enables sending contract calls through Fireblocks, that were built using Web3.

### Tokens
Full support for interfaces ERC721, ERC1155 and custom ABIs.

## Usage
### Installation
`pip3 install fireblocks-defi-sdk-py`

### Requirements
Python 3.6 or newer

## Examples
### Bridge
* [Basic Example](./fireblocks_defi_sdk_py/examples/basic_example.py)
* [Trading on Uniswap](./fireblocks_defi_sdk_py/examples/uniswap_example.py)

### NFT
* [ERC20 using CustomToken](./fireblocks_defi_sdk_py/nft/examples/erc20_example.py)
* [ERC721](./fireblocks_defi_sdk_py/nft/examples/nft_example.py)
* [ERC1155](./fireblocks_defi_sdk_py/nft/examples/multi_token_example.py)
* [CustomToken](./fireblocks_defi_sdk_py/nft/examples/custom_token_example.py)