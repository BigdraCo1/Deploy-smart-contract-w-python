# Smart Contract Deployment
# Read .sol file
# Compile
# Deploy

import os
import shutil
from solcx import compile_source, install_solc
from web3 import Web3

# Get the path to the cache directory
cache_dir = os.path.join(os.path.expanduser('~'), '.solcx')

# Check if the cache directory exists
if os.path.exists(cache_dir):
    # Delete the cache directory
    shutil.rmtree(cache_dir)
install_solc('0.8.19', show_progress=True)


def compile_src_file(file_path):
    # read .sol file
    with open(file_path, 'r') as f:
        file = f.read()

    # compile using solcx
    compile_file = compile_source(file)
    return compile_file


def deploy_smart_contract(complied_details):
    # get abi, bytecode
    ABI = complied_details[1]['abi']
    bytecode = complied_details[1]['bin']

    # connect to blockchain
    w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))
    account = w3.eth._accounts()[0]
    contract = w3.eth.contract(bytecode=bytecode, abi=ABI)
    nonce = w3.eth.get_transaction_count(account=account)
    build_contract = contract.constructor().build_transaction({
        "from": account,
        "gas": 6721975,
        "gasPrice": w3.eth.gas_price,
        "nonce": nonce
    })
    signed_txn = w3.eth.account.sign_transaction(build_contract,
                                                 '0x8cf8b931c0b008add3b74ce8c9b4ade59e1aa7e396961967fcd054332e834ee3')
    send_transaction = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    transaction_receipt = w3.eth.wait_for_transaction_receipt(send_transaction)

    contract_address = transaction_receipt['contractAddress']  # deployed contract
    return contract_address


if __name__ == "__main__":
    sol_file_path = 'contract/storage.sol'
    # compile sol file
    sol_complied_file = compile_src_file(sol_file_path)
    sol_complied_details = sol_complied_file.popitem()

    # compilation details (abi, bytecode)
    print('Compilation ID : ', sol_complied_details[0])
    print('ABI : ', sol_complied_details[1]['abi'])
    print('Bytecode : ', sol_complied_details[1]['bin'])

    # deploy smart contract
    deployed_contract_address = deploy_smart_contract(sol_complied_details)
    print('Contract address : ', deployed_contract_address)
