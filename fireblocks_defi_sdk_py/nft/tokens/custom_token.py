from . base_token import *


class CustomToken(BaseToken):
    def __init__(self, web3_bridge: Web3Bridge, custom_abi: str):
        super().__init__(web3_bridge)
        self.abi = custom_abi
        self.contract = self.web_provider.eth.contract(
            address=self.web_provider.toChecksumAddress(self.web3_bridge.external_wallet_address),
            abi=self.abi
        )
