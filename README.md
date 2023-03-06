## Updates
Check out our new SDK [Local-JSON-RPC](https://github.com/fireblocks/fireblocks-json-rpc) for an improved developer experience for using Python to interact with EVM chains using Fireblocks.

# Fireblocks Python DeFi SDK
[![PyPI version](https://badge.fury.io/py/fireblocks-defi-sdk.svg)](https://badge.fury.io/py/fireblocks-defi-sdk)

The Fireblocks Python DeFi SDK provides an interoperability layer between Fireblocks Smart Contract API and common DeFi libraries.
For more information on Fireblocks Smart Contract API and automating DeFi workflows on Fireblocks [read here](https://support.fireblocks.io/hc/en-us/articles/360017709160-Fireblocks-Smart-Contract-API).

Please email us at support@fireblocks.com if you have questions or feedback.
# Table Of Contents
- [Features](#Features)
  - [Web3 Bridge](#Bridge)
  - [Tokens](#Tokens)
- [Usage](#Usage)
  - [Installation](#Installation)
  - [Requirements](#Requirements)
- [Code Examples](#Examples)
  - [Web3Bridge](#Web3Bridge)
  - [Tokenization](#Tokenization)

## Features
### Bridge
Enables sending contract calls through Fireblocks, that were built using Web3.

### Tokens
Full support for interfaces ERC721, ERC1155 and custom ABIs.

## Usage
### Installation
`pip3 install fireblocks-defi-sdk`

### Requirements
Python 3.6 or newer

## Examples
### Web3Bridge
* [Basic Example](fireblocks_defi_sdk_py/examples/basic_example.py)
* [Trading on Uniswap](fireblocks_defi_sdk_py/examples/uniswap_example.py)

### Tokenization
* [ERC20 using CustomToken](fireblocks_defi_sdk_py/tokenization/examples/erc20_example.py)
* [ERC721](fireblocks_defi_sdk_py/tokenization/examples/nft_example.py)
* [ERC1155](fireblocks_defi_sdk_py/tokenization/examples/multi_token_example.py)
* [CustomToken](fireblocks_defi_sdk_py/tokenization/examples/custom_token_example.py)
