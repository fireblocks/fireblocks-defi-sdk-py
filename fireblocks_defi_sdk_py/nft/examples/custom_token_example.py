# This is an example of interacting with a custom contract, using the CustomToken interface.
import os
from fireblocks_defi_sdk_py import Chain, CustomToken, Web3Bridge
from fireblocks_sdk import FireblocksSDK, TRANSACTION_STATUS_COMPLETED

API_KEY = os.environ['TEST_API_KEY']
API_SECRET = os.environ['SECRET']

SDK = FireblocksSDK(API_SECRET, API_KEY)
VAULT_ID, SECONDARY_VAULT_ID = "0", "2"
CONTRACT_ADDRESS = ""
WHITELISTED_CONTRACT_UUID = ""  # This is the Fireblocks UUID of the whitelisted address.

FILE_PATH, MODE = "some/path/to/my/contract", "r"

if __name__ == "__main__":
    # We start by building a bridge to the Ropsten network, including initiating a CustomToken object which will
    # represent our custom contract. In order to initiate a CustomToken, we will need a contract ABI. This can be read
    # from another file, passed as a variable declared locally, or fetched from EtherScan using fetch_abi(address). We
    # will use the first.
    ropsten_bridge = Web3Bridge(SDK, VAULT_ID, CONTRACT_ADDRESS, Chain.ROPSTEN, WHITELISTED_CONTRACT_UUID)
    with open(FILE_PATH, MODE) as file:
        contract_abi = file.read()
    custom_contract_bridge = CustomToken(ropsten_bridge, contract_abi)

    # Let's assume our ABI holds a transferOwnership write function, and a contractOwner function (returning a boolean).
    # We will first validate we own the contract and then transfer it to another vault in our account.
    checked_address = custom_contract_bridge.web_provider.toChecksumAddress(custom_contract_bridge.wallet_address)
    if custom_contract_bridge.call_read_function("contractOwner", checked_address):
        # We will initiate another bridge, as we will need the wallet address, and we will later on transfer it back.
        secondary_ropsten_bridge = Web3Bridge(SDK, SECONDARY_VAULT_ID, CONTRACT_ADDRESS, Chain.ROPSTEN,
                                              WHITELISTED_CONTRACT_UUID)
        secondary_contract_bridge = CustomToken(secondary_ropsten_bridge, contract_abi)
        building_params = {"from": checked_address}
        secondary_address = secondary_contract_bridge.web_provider.toChecksumAddress(
            secondary_contract_bridge.wallet_address)
        transfer_ownership_raw_transaction = custom_contract_bridge. \
            call_write_function("transferOwnership",
                                secondary_address,
                                building_params=building_params)

        transfer_ownership_transaction = custom_contract_bridge.submit_transaction(transfer_ownership_raw_transaction)
        if ropsten_bridge.check_tx_is_completed(transfer_ownership_transaction['id']) == TRANSACTION_STATUS_COMPLETED:
            print("Successfully transferred ownership from first wallet to the second one.")
            # We will now transfer the ownership back to our original wallet.
            building_params['from'] = secondary_address
            ownership_raw_transaction = secondary_contract_bridge. \
                call_write_function("transferOwnership",
                                    checked_address,
                                    building_params=building_params)
            ownership_transaction = secondary_contract_bridge.submit_transaction(ownership_raw_transaction, "Returning")
            if secondary_ropsten_bridge.check_tx_is_completed(ownership_transaction['id']) == \
                    TRANSACTION_STATUS_COMPLETED:
                print("Successfully transferred ownership from second wallet to the first one.")
            else:
                print("Failed transferring ownership from the second wallet to the first.")
        else:
            print("Failed transferring ownership from the first wallet to the second.")
