from . base_token import *
from .. utils.helpers import ERC1155_ABI


class ERC1155(BaseToken):
    def __init__(self, web3_bridge: Web3Bridge):
        super().__init__(web3_bridge)
        self.abi = ERC1155_ABI
        self.contract: contract = self.web_provider.eth.contract(
            address=self.web_provider.toChecksumAddress(self.web3_bridge.external_wallet_address),
            abi=self.abi
        )

    # Payables
    def set_approval_for_all(self, operator_address: str, is_approved: bool, note: str = ""):
        """
        Provide an operator with approval permission or revoke them
        :param operator_address: Approved operator address
        :param is_approved: True to permit, False to revoke
        :param note: (Optional) Add a note to the transaction.
        :return: None
        """
        checked_op_adr = self.web_provider.toChecksumAddress(operator_address)
        return self.submit_transaction(self.call_write_function("setApprovalForAll", checked_op_adr, is_approved), note)

    def safe_transfer_from(self, to_address: str, token_id: int, amount: int, from_address: str = "",
                           data: bytes = bytearray(), note: str = ""):
        """
        :param to_address: The receiver of the token.
        :param token_id: The ID of the sent token.
        :param amount: Amount of Token ID to send.
        :param from_address: (Optional) The sender of the token, if it's not the wallet under Fireblocks.
        :param data: (Optional) Send additional data (bytes) only if required by contract.
        :param note: (Optional) Add a note to the transaction.
        :return: None
        """
        if not from_address:
            from_address = self.wallet_address
        address_dict = {"from": self.web_provider.toChecksumAddress(from_address)}
        checked_from_adr = self.web_provider.toChecksumAddress(from_address)
        checked_to_adr = self.web_provider.toChecksumAddress(to_address)

        transaction = self.contract.functions.safeTransferFrom(
            checked_from_adr,
            checked_to_adr,
            token_id,
            amount,
            data
        ).buildTransaction(address_dict)

        return self.submit_transaction(transaction, note)

    def safe_batch_transfer_from(self, to_address: str, token_ids: list[int], values: list[int], from_address: str = "",
                                 data: bytes = bytearray(), note: str = ""):
        """
        Length of token_ids and values must match. Moreover, the value of each token (at position x at [values]) to be
        sent must match the same position at [token_ids] (position x). For example:
        token_ids [3, 6, 10] and values [10, 20, 30] will send:
        - 10 tokens of token id 3
        - 20 tokens of token id 6
        - 30 tokens of token id 10
        :param to_address: The receiver of the token.
        :param token_ids: A list of token ids to transfer from sender to receiver.
        :param values: A list of values to transfer of each token.
        :param from_address: (Optional) The sender of the token, if it's not the wallet under Fireblocks.
        :param data: (Optional) Send additional data (bytes) only if required by contract.
        :param note: (Optional) Add a note to the transaction.
        :return: None
        """
        if not from_address:
            from_address = self.wallet_address
        address_dict = {"from": self.web_provider.toChecksumAddress(from_address)}
        checked_from_adr = self.web_provider.toChecksumAddress(from_address)
        checked_to_adr = self.web_provider.toChecksumAddress(to_address)
        if len(token_ids) != len(values):
            raise ValueError("Length of token_ids and values must match!")

        transaction = self.contract.functions.safeBatchTransferFrom(
            checked_from_adr,
            checked_to_adr,
            token_ids,
            values,
            data
        ).buildTransaction(address_dict)

        return self.submit_transaction(transaction, note)

    # Views
    def supports_interface(self, interface_id: str = "0xd9b67a26") -> bool:
        """
        Checks if contract supports a certain interface.
        :param interface_id: (Optional) The interface id. "0x80ac58cd" is ERC721 interface id. "0xd9b67a26" is ERC1155
         interface id. Checks class interface id by default.
        :return: True if the contract supports the interface, False otherwise
        """
        return self.call_read_function("supportsInterface", interface_id)

    def balance_of(self, token_id: int, owner_address: str = "") -> int:
        """
        Gets the balance of the address provided
        :param owner_address: Address to be checked
        :param token_id: ID of the token.
        :return: Balance (int)
        """
        if not owner_address:
            owner_address = self.wallet_address
        return self.call_read_function("balanceOf", owner_address, token_id)

    def balance_of_batch(self, id_list: list[int], owners_list=None) -> list[int]:
        """

        :param owners_list: A list of addresses
        :param id_list: A list of token Ids
        :return:
        """
        if not owners_list:
            owners_list = [self.wallet_address] * len(id_list)
        checked_addresses = [self.web_provider.toChecksumAddress(address) for address in owners_list]
        return self.call_read_function("balanceOfBatch", checked_addresses, id_list)

    def is_approved_for_all(self, operator_address: str, owner_address: str = "") -> bool:
        """
        Validates whether an operator has been approved by a stated owner.
        :param operator_address: Address of the meant to be operator.
        :param owner_address: (Optional) Address of the owner, in case it's not the wallet address.
        :return: True whether operator is approved, False otherwise
        """
        if not owner_address:
            owner_address = self.wallet_address
        owner_checked_address = self.web_provider.toChecksumAddress(owner_address)
        operator_checked_address = self.web_provider.toChecksumAddress(operator_address)
        return self.call_read_function("isApprovedForAll", owner_checked_address, operator_checked_address)

    def uri(self, token_id: int) -> str:
        """
        :param token_id: URI id of a contract
        :return: The JSON metadata
        """
        return self.call_read_function("uri", token_id)

    # Events
