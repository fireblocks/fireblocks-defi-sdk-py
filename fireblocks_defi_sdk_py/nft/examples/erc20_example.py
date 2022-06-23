# This is an example of interacting with an ERC-20 contract, using the CustomToken interface.
import os
from fireblocks_defi_sdk_py import Chain, CustomToken, Web3Bridge, fetch_abi
from fireblocks_sdk import FireblocksSDK, TRANSACTION_STATUS_COMPLETED

API_KEY = os.environ['TEST_API_KEY']
API_SECRET = os.environ['SECRET']

SDK = FireblocksSDK(API_SECRET, API_KEY)
VAULT_ID = "0"
CONTRACT_ADDRESS = ""
RECEIVER_ADDRESS = ""
TOKEN_AMOUNT = 10

if __name__ == "__main__":
    # We start by building a bridge to the Ropsten network, including initiating a CustomToken object which will
    # represent our ERC20 contract. In order to initiate a CustomToken, we will need a contract ABI. This can be read
    # from another file, passed as a variable declared locally, or fetched from EtherScan using fetch_abi(address). We
    # will use the latter.
    ropsten_bridge = Web3Bridge(SDK, VAULT_ID, CONTRACT_ADDRESS, Chain.ROPSTEN)
    contract_abi = fetch_abi(CONTRACT_ADDRESS)
    erc20_contract_bridge = CustomToken(ropsten_bridge, contract_abi)

    # We build functions through passing the function name exactly as it appears on the ABI, following by its arguments.
    # It's important to differentiate between a read (view) and write function. We will demonstrate both.
    total_supply = erc20_contract_bridge.call_read_function("totalSupply")
    my_balance = erc20_contract_bridge.call_read_function("balanceOf", erc20_contract_bridge.wallet_address)

    # Note how both of the functions above were not submitted to Fireblocks, as there is no need to sign these (read).
    # The below functions will demonstrate a write function, that will afterwards be submitted to Fireblocks.

    # We will mint a token (function receives address & amount) to our own address and then send it to another address.
    # We will also have to add the sender under the building_params in the following format:
    checked_address = erc20_contract_bridge.web_provider.toChecksumAddress(erc20_contract_bridge.wallet_address)
    # Web3 only accepts checkedSum addresses.
    building_params = {"from": checked_address}
    mint_raw_transaction = erc20_contract_bridge.call_write_function("mint", checked_address,
                                                                     TOKEN_AMOUNT,
                                                                     building_params=building_params)
    # We will now submit the transaction to Fireblocks.
    mint_transaction = erc20_contract_bridge.submit_transaction(mint_raw_transaction)
    if ropsten_bridge.check_tx_is_completed(mint_transaction['id']) == TRANSACTION_STATUS_COMPLETED:
        print(f"Successfully minted {TOKEN_AMOUNT} to {erc20_contract_bridge.wallet_address}")
        transfer_raw_transaction = erc20_contract_bridge.call_write_function("transferFrom",
                                                                             checked_address,
                                                                             RECEIVER_ADDRESS, TOKEN_AMOUNT,
                                                                             building_params=building_params)
        transfer_transaction = erc20_contract_bridge.submit_transaction(transfer_raw_transaction,
                                                                        "Transferring 10 minted tokens.")
        if ropsten_bridge.check_tx_is_completed(transfer_transaction['id']):
            print(
                f"Successfully transferred {TOKEN_AMOUNT} from {erc20_contract_bridge.wallet_address} to "
                f"{RECEIVER_ADDRESS}")
        else:
            print("Failed transferring minted tokens.")
    else:
        print("Failed minting new tokens.")
