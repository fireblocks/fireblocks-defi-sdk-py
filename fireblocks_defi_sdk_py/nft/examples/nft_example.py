# This is an example of interacting with an ERC-721 contract, using the ERC721 interface.
import os
from fireblocks_defi_sdk_py import ERC721, Chain, Web3Bridge
from fireblocks_sdk import FireblocksSDK, TRANSACTION_STATUS_COMPLETED

API_KEY = os.environ['TEST_API_KEY']
API_SECRET = os.environ['SECRET']

SDK = FireblocksSDK(API_SECRET, API_KEY)
VAULT_ID = "0"
CONTRACT_ADDRESS = ""
RECEIVER_ADDRESS = ""
TOKEN_ID = 1

if __name__ == "__main__":
    # We start by building a bridge to the Ropsten network, including initiating a ERC721 object.
    ropsten_bridge = Web3Bridge(SDK, VAULT_ID, CONTRACT_ADDRESS, Chain.ROPSTEN)
    nft_contract_bridge = ERC721(ropsten_bridge)

    # ERC721 implements all the basic capabilities mentioned in ERC721:
    # https://ethereum.org/en/developers/docs/standards/tokens/erc-721/
    # This code will show a few examples including the inherited supportsInterface from ERC165.

    # Each interface has a unique ID. If no parameter is passed onto the function, it checks for the default interface
    # of token, meaning - 721.
    interface_supported = nft_contract_bridge.supports_interface()
    if interface_supported:
        print(f"{nft_contract_bridge} - supports ERC721 interface.")

    # Next, we will validate whether we own a balance of NFT, and attempt to send a Token to another address.
    # We can use the balance_of function, and if we don't pass any arguments to it, it will use the relevant wallet
    # address to the vault ID passed to the Web3Bridge object.
    balance = nft_contract_bridge.balance_of()
    print(f"{nft_contract_bridge.wallet_address} owns {balance} tokens.")

    if balance:
        # We will now verify if the owner of the token is indeed the wallet, and then transfer it to another address.
        token_owner = nft_contract_bridge.owner_of(TOKEN_ID)
        if token_owner == nft_contract_bridge.wallet_address:
            receiver_initial_balance = nft_contract_bridge.balance_of(RECEIVER_ADDRESS)
            # safe_transfer_from returns a dictionary with a status and id.
            transaction = nft_contract_bridge.safe_transfer_from(RECEIVER_ADDRESS, TOKEN_ID)
            transaction_result = ropsten_bridge.check_tx_is_completed(transaction['id'])

            if transaction_result == TRANSACTION_STATUS_COMPLETED:
                # After the transaction has been completed we check whether the balance of the receiver has been updated
                if nft_contract_bridge.balance_of(RECEIVER_ADDRESS) == receiver_initial_balance + 1:
                    print(f"{RECEIVER_ADDRESS} has received the token successfully.")
            else:
                print("Could not post transaction.")
