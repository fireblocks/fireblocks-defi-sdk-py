# This is an example of interacting with an ERC-1155 contract, using the ERC1155 interface.
import os
from .. import ERC1155
from ... import Chain, Web3Bridge
from fireblocks_sdk import FireblocksSDK

API_KEY = os.environ['TEST_API_KEY']
API_SECRET = os.environ['SECRET']

SDK = FireblocksSDK(API_SECRET, API_KEY)
VAULT_ID = "0"
CONTRACT = ""


if __name__ == "__main__":
    # We start by building a bridge to the Ropsten network, including initiating a ERC721 object.
    ropsten_bridge = Web3Bridge(SDK, VAULT_ID, CONTRACT, Chain.ROPSTEN)



