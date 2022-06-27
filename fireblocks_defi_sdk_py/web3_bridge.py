import time

from fireblocks_sdk import FireblocksSDK, TransferPeerPath, DestinationTransferPeerPath, ONE_TIME_ADDRESS, \
    VAULT_ACCOUNT, EXTERNAL_WALLET, TRANSACTION_STATUS_BLOCKED, TRANSACTION_STATUS_COMPLETED, TRANSACTION_STATUS_FAILED
from fireblocks_sdk.api_types import TRANSACTION_STATUS_CANCELLED
from chain import Chain
from web3 import Web3

SUBMIT_TIMEOUT = 45
STATUS_KEY = "status"


CHAIN_TO_ASSET_ID = {
    Chain.MAINNET: ('ETH', "https://cloudflare-eth.com"),
    Chain.ROPSTEN: ('ETH_TEST', "https://ropsten.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161"),
    Chain.KOVAN: ('ETH_TEST2', "https://kovan.infura.io/v3/bce1459b281d491f8d06dd4f2c3d1a12"),
    Chain.BSC: ('BNB_BSC', "https://bsc-dataseed.binance.org"),
    Chain.BSC_TEST: ('BNB_TEST', "https://data-seed-prebsc-1-s3.binance.org:8545"),
    Chain.POLYGON: ('MATIC_POLYGON', "https://polygon-rpc.com")
}


class Web3Bridge:
    def __init__(self, fb_api_client: FireblocksSDK, vault_account_id: str, external_wallet_address: str, chain: Chain,
                 wl_uuid: str = ""):
        """
        :param fb_api_client: Fireblocks API client.
        :param vault_account_id: The source vault which address will sign messages.
        :param external_wallet_address: The address of the interacted *contract*.
        :param chain: Object of type Chain to represent what network to work with.
        :param wl_uuid: (Optional) If the contract is whitelisted, it can be sent through the co-responding UUID.
        """
        self.fb_api_client = fb_api_client
        self.source_vault_id = vault_account_id
        self.external_wallet_address = external_wallet_address
        self.chain = chain
        self.asset: str = CHAIN_TO_ASSET_ID[self.chain][0]
        self.web_provider = Web3(Web3.HTTPProvider(CHAIN_TO_ASSET_ID[self.chain][1]))
        self.wl_uuid = wl_uuid

    def send_transaction(self, transaction: dict, note="") -> dict:
        """
        Takes a ready transaction after being built (using web3 buildTransaction()) and transmits it to Fireblocks.
        :param transaction: A transaction object (dict) to submit to the blockchain.
        :param note: (Optional) A note to submit with the transaction.
        :return:
        """
        if self.wl_uuid:
            destination = TransferPeerPath(EXTERNAL_WALLET, self.wl_uuid)
        else:
            destination = DestinationTransferPeerPath(ONE_TIME_ADDRESS,
                                                      one_time_address={"address": self.external_wallet_address})
        return self.fb_api_client.create_transaction(
            tx_type="CONTRACT_CALL",
            asset_id=CHAIN_TO_ASSET_ID[self.chain],
            source=TransferPeerPath(VAULT_ACCOUNT, self.source_vault_id),
            amount="0",
            destination=destination,
            note=note,
            extra_parameters={
                "contractCallData": transaction["data"]
            }
        )

    def check_tx_is_completed(self, tx_id) -> dict:
        """
        This function waits for SUBMIT_TIMEOUT*4 (180 by default) seconds to retrieve status of the transaction sent to
        Fireblocks. Will stop upon completion / failure.
        :param tx_id: Transaction ID from FBKS.
        :return: Transaction last status after timeout / completion.
        """
        timeout = 0
        current_status = self.fb_api_client.get_transaction_by_id(tx_id)[STATUS_KEY]
        while current_status not in (
                TRANSACTION_STATUS_COMPLETED, TRANSACTION_STATUS_FAILED, TRANSACTION_STATUS_BLOCKED,
                TRANSACTION_STATUS_CANCELLED) and timeout < SUBMIT_TIMEOUT:
            print(f"TX [{tx_id}] is currently at status - {current_status} {'.' * (timeout % 4)}                ",
                  end="\r")
            time.sleep(4)
            current_status = self.fb_api_client.get_transaction_by_id(tx_id)[STATUS_KEY]
            timeout += 1

        print(f"\nTX [{tx_id}] is currently at status - {current_status}")
        return current_status
