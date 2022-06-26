from . base_token import *
from .. utils.helpers import ERC721_ABI


class ERC721(BaseToken):
    def __init__(self, web3_bridge: Web3Bridge):
        super().__init__(web3_bridge)
        self.abi = ERC721_ABI
        self.contract: contract = self.web_provider.eth.contract(
            address=self.web_provider.toChecksumAddress(self.web3_bridge.external_wallet_address),
            abi=self.abi
        )

    # Payables
    def approve(self, to_address: str, token_id: int, approver_address: str = "", note: str = ""):
        """
        Receives an address and a Token ID so the specified address can perform actions on it.
        :param to_address: The receiver of the token.
        :param token_id: The ID of the sent token.
        :param approver_address: The owner of the token.
        :param note: (Optional) Add a note to the transaction.
        :return: None
        """
        checked_app_adr = self.web_provider.toChecksumAddress(to_address)
        if not approver_address:
            approver_address = self.wallet_address
        address_dict = {"from": self.web_provider.toChecksumAddress(approver_address)}
        return self.submit_transaction(self.call_write_function("approve", checked_app_adr, token_id,
                                                                building_params=address_dict), note)

    def safe_transfer_from(self, to_address: str, token_id: int, from_address: str = "", data: bytes = bytearray(),
                           note: str = ""):
        """
        :param from_address: The sender of the token.
        :param to_address: The receiver of the token.
        :param token_id: The ID of the sent token.
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
        if data:
            transaction = self.contract.functions.safeTransferFrom(
                checked_from_adr,
                checked_to_adr,
                token_id,
                data
            ).buildTransaction(address_dict)

        else:
            transaction = self.contract.functions.safeTransferFrom(
                checked_from_adr,
                checked_to_adr,
                token_id
            ).buildTransaction(address_dict)

        return self.submit_transaction(transaction, note)

    def transfer_from(self, to_address: str, token_id: int, from_address: str = "", note: str = ""):
        """
        Do note it's encouraged to use safe_transfer_from instead.
        :param from_address: The sender of the token.
        :param to_address: The receiver of the token.
        :param token_id: The ID of the sent token.
        :param from_address: (Optional) The sender of the token, if it's not the wallet under Fireblocks.
        :param note: (Optional) Add a note to the transaction.
        :return: None
        """
        if not from_address:
            from_address = self.wallet_address
        address_dict = {"from": self.web_provider.toChecksumAddress(from_address)}
        checked_from_adr = self.web_provider.toChecksumAddress(from_address)
        checked_to_adr = self.web_provider.toChecksumAddress(to_address)
        return self.submit_transaction(self.call_write_function("transferFrom",
                                                                checked_from_adr,
                                                                checked_to_adr,
                                                                token_id,
                                                                building_params=address_dict), note)

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

    # Views
    def supports_interface(self, interface_id: str = "0x80ac58cd") -> bool:
        """
        Checks if contract supports a certain interface.
        :param interface_id: The interface id. "0x80ac58cd" is ERC721 interface id. "0xd9b67a26" is ERC1155 interface id
        :return: True if the contract supports the interface, False otherwise
        """
        return self.call_read_function("supportsInterface", interface_id)

    def get_approved(self, token_id: int) -> str:
        """
        Gets the approved address for a token ID, or  the zero address (0x0000000000000000000000000000000000000000)
        if no address is set. Will raise an exception if token ID does not exist.
        :param token_id: a number representing the token ID
        :return: The address approved for the token.
        """
        return self.call_read_function("getApproved", token_id)

    def is_approved_for_all(self, owner_address: str, operator_address: str) -> bool:
        """
        Validates whether an operator has been approved by a stated owner.
        :param owner_address: Address of the owner.
        :param operator_address: Address of the meant to be operator.
        :return: True whether operator is approved, False otherwise
        """
        owner_checked_address = self.web_provider.toChecksumAddress(owner_address)
        operator_checked_address = self.web_provider.toChecksumAddress(operator_address)
        return self.call_read_function("isApprovedForAll", owner_checked_address, operator_checked_address)

    def balance_of(self, owner_address: str = "") -> int:
        """
        Gets the balance of the address provided
        :param owner_address: Address to be checked
        :return: Balance (int)
        """
        if not owner_address:
            owner_address = self.wallet_address
        owner_checked_address = self.web_provider.toChecksumAddress(owner_address)
        return self.call_read_function("balanceOf", owner_checked_address)

    def owner_of(self, token_id: int) -> str:
        """
        Checks who owns the token ID.
        :param token_id: a number representing the token ID
        :return: The address (plain) of the owner
        """
        return self.call_read_function("ownerOf", token_id)

    # Events
