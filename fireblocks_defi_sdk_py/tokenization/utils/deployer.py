from ..tokens.base_token import *


class Deployer(BaseToken):
    def __init__(self, web3_bridge: Web3Bridge, contract_abi, contract_byte_code):
        super().__init__(web3_bridge)
        self.contract_abi = contract_abi
        self.contract_byte_code = contract_byte_code

    @staticmethod
    def fetch_builders(solidity_file_path: str):
        pass
