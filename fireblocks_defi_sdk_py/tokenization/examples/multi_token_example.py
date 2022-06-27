# This is an example of interacting with an ERC-1155 contract, using the ERC1155 interface.
import os
from fireblocks_defi_sdk_py import ERC1155, Chain, Web3Bridge
from fireblocks_sdk import FireblocksSDK, TRANSACTION_STATUS_COMPLETED

API_KEY = os.environ['TEST_API_KEY']
API_SECRET = os.environ['SECRET']

SDK = FireblocksSDK(API_SECRET, API_KEY)
VAULT_ID = "0"
CONTRACT = ""
RECEIVER_ADDRESSES = ""
# A list of ints representing the token IDs.
TOKEN_IDS = [1, 2]

if __name__ == "__main__":
    # We start by building a bridge to the Kovan network, including initiating a ERC1155 object.
    kovan_bridge = Web3Bridge(SDK, VAULT_ID, CONTRACT, Chain.KOVAN)
    multi_token_contract_bridge = ERC1155(kovan_bridge)

    # ERC1155 implements all the basic capabilities mentioned in ERC721:
    # https://ethereum.org/en/developers/docs/standards/tokens/erc-1155/
    # This code will show a few examples using the functions mentioned above.

    # We will check the balance of tokens 1, 2 under the vault wallet address, and then use it to send all the tokens to
    # another address.
    tokens_balance = multi_token_contract_bridge.balance_of_batch(TOKEN_IDS)
    if tokens_balance:
        # Once again, the object will by default attempt to send assets from the given wallet address, unless defined
        # otherwise. We can also add a note to the transaction in Fireblocks.
        transfer_tokens = multi_token_contract_bridge.safe_batch_transfer_from(RECEIVER_ADDRESSES, TOKEN_IDS,
                                                                               tokens_balance,
                                                                               note="Transfer to another vault.")
        transfer_result = kovan_bridge.check_tx_is_completed(transfer_tokens['id'])

        if transfer_result == TRANSACTION_STATUS_COMPLETED:
            print(f"{RECEIVER_ADDRESSES} now owns {tokens_balance} of tokens: {TOKEN_IDS}")
        else:
            print("Failed transferring tokens.")
