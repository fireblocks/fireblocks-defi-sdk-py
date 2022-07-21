import os
from fireblocks_defi_sdk_py import Chain, Web3Bridge, ContractDeployer
from fireblocks_sdk import FireblocksSDK, TRANSACTION_STATUS_COMPLETED

API_KEY = os.environ['TEST_API_KEY']
API_SECRET = os.environ['SECRET']

SDK = FireblocksSDK(API_SECRET, API_KEY)

# The below are after-compilation results.
CONTRACT_BYTECODE = "608060405234801561001057600080fd5b506040516102b33803806102b3833981810160405281019061003291906100" \
                    "7a565b80600081905550506100a7565b600080fd5b6000819050919050565b61005781610044565b8114610062576000" \
                    "80fd5b50565b6000815190506100748161004e565b92915050565b6000602082840312156100905761008f61003f565b" \
                    "5b600061009e84828501610065565b91505092915050565b6101fd806100b66000396000f3fe60806040523480156100" \
                    "1057600080fd5b50600436106100415760003560e01c80637cf5dab0146100465780638381f58a14610062578063d826" \
                    "f88f14610080575b600080fd5b610060600480360381019061005b91906100eb565b61008a565b005b61006a6100a156" \
                    "5b6040516100779190610127565b60405180910390f35b6100886100a7565b005b806000546100989190610171565b60" \
                    "008190555050565b60005481565b60008081905550565b600080fd5b6000819050919050565b6100c8816100b5565b81" \
                    "146100d357600080fd5b50565b6000813590506100e5816100bf565b92915050565b6000602082840312156101015761" \
                    "01006100b0565b5b600061010f848285016100d6565b91505092915050565b610121816100b5565b82525050565b6000" \
                    "60208201905061013c6000830184610118565b92915050565b7f4e487b71000000000000000000000000000000000000" \
                    "00000000000000000000600052601160045260246000fd5b600061017c826100b5565b9150610187836100b5565b9250" \
                    "827fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff038211156101bc576101bb610142" \
                    "565b5b82820190509291505056fea2646970667358221220506684578fb66545cba61a76a05e502da730b83cfa760f55" \
                    "ce9943ba0814013364736f6c63430008090033"

# Note that the constructor takes a single parameter, _initialNumber which we will pass as an int.
CONTRACT_ABI = [
  {
    'inputs': [
      {
        'internalType': 'uint256',
        'name': '_initialNumber',
        'type': 'uint256'
      }
    ],
    'stateMutability': 'nonpayable',
    'type': 'constructor'
  },
  {
    'inputs': [
      {
        'internalType': 'uint256',
        'name': '_value',
        'type': 'uint256'
      }
    ],
    'name': 'increment',
    'outputs': [],
    'stateMutability': 'nonpayable',
    'type': 'function'
  },
  {
    'inputs': [],
    'name': 'number',
    'outputs': [
      {
        'internalType': 'uint256',
        'name': '',
        'type': 'uint256'
      }
    ],
    'stateMutability': 'view',
    'type': 'function'
  },
  {
    'inputs': [],
    'name': 'reset',
    'outputs': [],
    'stateMutability': 'nonpayable',
    'type': 'function'
  }
]

my_bridge = Web3Bridge(
    fb_api_client=SDK,
    vault_account_id="0",
    chain=Chain.ROPSTEN
)

my_contract = ContractDeployer(web3_bridge=my_bridge, contract_abi=CONTRACT_ABI, contract_byte_code=CONTRACT_BYTECODE)

# Incrementer.sol takes a single parameter, an int, to construct the contract.
constructed_contract = my_contract.build_contract(8)

print(my_contract.publish_contract(contract_transaction=constructed_contract))
