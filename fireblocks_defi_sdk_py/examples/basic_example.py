import os
import json

from web3 import Web3
from fireblocks_defi_sdk_py import Web3Bridge, Chain
from fireblocks_sdk import FireblocksSDK, TransferPeerPath, TRANSACTION_STATUS_CONFIRMED, TRANSACTION_STATUS_CANCELLED, TRANSACTION_STATUS_REJECTED, TRANSACTION_STATUS_FAILED, VAULT_ACCOUNT,\
    TRANSACTION_MINT, TRANSACTION_BURN, FireblocksApiException, DestinationTransferPeerPath, ONE_TIME_ADDRESS

w3 = Web3(Web3.EthereumTesterProvider())
print(w3.isConnected())
CHAIN = Chain.ROPSTEN
CONTRACT_ADDRESS = Web3.toChecksumAddress("0xcbe74e21b070a979b9d6426b11e876d4cb618daf")
EIP20_ABI = json.loads('[{"constant":false,"inputs":[{"name":"_greeting","type":"string"}],"name":"greet","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getGreeting","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"}]')
GREETING = "Hello web3"


def create_contract_call_transaction(bridge: Web3Bridge, tx_data: dict):
    resp = bridge.send_transaction(tx_data)
    print(resp)
    bridge.check_tx_is_completed(resp["id"])


if __name__ == '__main__':
    api_secret = os.environ.get("FIREBLOCKS_API_SECRET_PATH")
    fb_api_client = FireblocksSDK(api_secret, os.environ.get("FIREBLOCKS_API_KEY"), os.environ.get("FIREBLOCKS_API_BASE_URL"))
    bridge = Web3Bridge(fb_api_client,
                        vault_account_id=os.environ.get("FIREBLOCKS_SOURCE_VAULT_ACCOUNT"),
                        external_wallet_address=os.environ.get("FIREBLOCKS_EXTERNAL_WALLET"),
                        chain=CHAIN)
    contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=EIP20_ABI)
    tx_data = contract.functions.greet(GREETING).buildTransaction()
    create_contract_call_transaction(bridge, tx_data)
