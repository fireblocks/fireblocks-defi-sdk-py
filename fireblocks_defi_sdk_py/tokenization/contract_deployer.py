from .. web3_bridge import Web3Bridge
from . utils.helpers import ADDRESS
from web3 import contract
from web3.types import TxParams


class ContractDeployer:
    def __init__(self, web3_bridge: Web3Bridge, contract_abi: list, contract_byte_code: str):
        self.bridge = web3_bridge
        self.abi = contract_abi
        self.bytecode = contract_byte_code
        self.wallet_address = self.bridge.fb_api_client.get_deposit_addresses(self.bridge.source_vault_id,
                                                                              self.bridge.asset)[0][ADDRESS]

    def build_contract(self, *contract_construction_args) -> TxParams:
        """
        :param contract_construction_args: These arguments are the parameters that the contract constructor function
        takes as part of deploying the contract.
        :return: A transaction that can be sent through Fireblocks.
        """
        contract_constructor = self.bridge.web_provider.eth.contract(abi=self.abi, bytecode=self.bytecode)
        built_contract = contract_constructor.constructor(*contract_construction_args).buildTransaction(
            {
                "from": self.wallet_address
            }
        )

        return built_contract

    def publish_contract(self, contract_transaction: dict) -> dict:
        return self.bridge.send_transaction(contract_transaction)
