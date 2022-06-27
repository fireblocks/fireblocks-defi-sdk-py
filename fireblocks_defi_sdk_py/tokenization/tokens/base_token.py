from ... web3_bridge import Web3Bridge, CHAIN_TO_ASSET_ID
from .. utils.helpers import ADDRESS
from web3 import contract


class BaseToken:
    def __init__(self, web3_bridge: Web3Bridge):
        """
        :param web3_bridge: Web3Bridge that holds the SDK, contract address, vault ID and chain (with white listed
        address optional as well).
        """
        self.web3_bridge = web3_bridge
        self.wallet_address = self.web3_bridge.fb_api_client.get_deposit_addresses(self.web3_bridge.source_vault_id,
                                                                                   self.web3_bridge.asset)[0][ADDRESS]
        self.web_provider = web3_bridge.web_provider
        self.abi = None
        self.contract: contract = self.web_provider.eth.contract(
            address=self.web_provider.toChecksumAddress(self.web3_bridge.external_wallet_address)
        )

    def __str__(self):
        return f"Contract [{self.web3_bridge.external_wallet_address}] | Chain [{self.web3_bridge.chain.value}]"

    def call_read_function(self, abi_function: str, *args):
        """
        Use this to execute a function that needs no signing, e.g. supportsInterface. Basically a "read" function.
        :param abi_function:
        :param args:
        :return:
        """
        return self.contract.get_function_by_name(abi_function)(*args).call()

    def call_write_function(self, abi_function: str, *args, building_params: dict = None) -> dict:
        """
        Use this to build a transaction which will then be sent to fireblocks to get signed.
        :param abi_function:
        :param args:
        :param building_params:
        :return:
        """
        if not building_params:
            building_params = {}
        return self.contract.get_function_by_name(abi_function)(*args).buildTransaction(building_params)

    def submit_transaction(self, transaction: dict, note: str = "") -> dict:
        """
        Takes a ready transaction after being built (using web3 buildTransaction()) and transmits it to Fireblocks.
        :param note:
        :param transaction:
        :return:
        """
        return self.web3_bridge.send_transaction(transaction, note)
