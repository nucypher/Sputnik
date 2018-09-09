from vyper import compiler
import web3
import web3.auto.gethdev

contract_name = 'hasheater.vy'


def deploy(w3):
    with open(contract_name, 'r') as f:
        contract_code = f.read()

    contract_bytecode = compiler.compile(contract_code).hex()
    contract_abi = compiler.mk_full_signature(contract_code)
    w3.eth.defaultAccount = w3.eth.accounts[0]

    Contract = w3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)
    tx_hash = Contract.constructor().transact()
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    contract = w3.eth.contract(
            address=tx_receipt.contractAddress,
            abi=contract_abi)
    return contract


if __name__ == '__main__':
    w3 = web3.auto.gethdev.w3

    contract = deploy(w3)

    #import hashlib
    #a = hashlib.sha256(b'a').digest()
    #b = hashlib.sha256(b'b').digest()
    #c = hashlib.sha256(b'c').digest()

    #h1 = contract.functions.add(a).transact()
    #h2 = contract.functions.add(b).transact()
    #h3 = contract.functions.add(c).transact()
    #w3.eth.waitForTransactionReceipt(h1)
    #w3.eth.waitForTransactionReceipt(h2)
    #w3.eth.waitForTransactionReceipt(h3)

    #print(contract.functions.read(0).call())
    #print(contract.functions.read(1).call())
    #print(contract.functions.read(2).call())

    #try:
    #    print(contract.functions.read(3).call())
    #except Exception:
    #    print('Rightfully failed')
